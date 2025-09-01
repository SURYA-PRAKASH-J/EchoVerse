import os, io, base64, uuid, logging, time, json
from typing import Dict, Tuple
from flask import Flask, render_template, request, redirect, url_for, send_file, session, flash
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") or os.urandom(24)

# Config: Hugging Face (for IBM Granite LLM rewriting)
HF_TOKEN = os.getenv("HF_API_TOKEN")
REWRITE_MODEL = os.getenv("GRANITE_MODEL_ID", "ibm-granite/granite-3.1-8b-instruct")
HF_HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
HF_API_URL = f"https://api-inference.huggingface.co/models/{REWRITE_MODEL}"

# Config: IBM Text-to-Speech (REST API)
IBM_API_KEY = os.getenv("IBM_API_KEY")
IBM_TTS_URL = (os.getenv("IBM_TTS_URL") or "").rstrip("/")
IBM_IAM_URL = "https://iam.cloud.ibm.com/identity/token"

# UI options
TONES: Dict[str, str] = {
    "Neutral": "neutral and clear",
    "Suspenseful": "suspenseful and dramatic",
    "Inspiring": "inspiring and motivational",
}
VOICES: Dict[str, str] = {
    "Allison (en-US)": "en-US_AllisonV3Voice",
    "Lisa (en-US)": "en-US_LisaV3Voice",
    "Michael (en-US)": "en-US_MichaelV3Voice",
    "Kate (en-GB)": "en-GB_KateV3Voice",
}

# Limits
MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", "5000"))

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("echoverse")

# Cache for IBM IAM token
_ibm_iam_token: str | None = None
_ibm_iam_expiry: float = 0.0


def hf_generate(prompt: str) -> str:
    """Call Hugging Face Inference for text rewriting using IBM Granite.
    Returns the generated text or raises an Exception on failure.
    """
    if not HF_TOKEN:
        raise RuntimeError("HF_API_TOKEN is not configured")

    try:
        resp = requests.post(HF_API_URL, headers=HF_HEADERS, json={"inputs": prompt}, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        # Typical text generation response: [{"generated_text": "..."}]
        if isinstance(data, list) and data and isinstance(data[0], dict) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        # Some instruct models may return dict with 'summary_text' or similar; fallback to inputs
        if isinstance(data, dict):
            text = data.get("generated_text") or data.get("summary_text")
            if text:
                return text
        raise RuntimeError(f"Unexpected HF response format: {data!r}")
    except requests.HTTPError as e:
        # If model is loading or rate-limited, HF returns 503/429; surface a friendly message
        logger.exception("HF Inference API error")
        raise RuntimeError(f"Hugging Face API error: {e.response.status_code} {e.response.text[:200]}") from e
    except Exception:
        logger.exception("HF Inference call failed")
        raise


def _refresh_ibm_iam_token() -> Tuple[str, float]:
    """Obtain a fresh IBM IAM token and its expiry epoch timestamp."""
    if not IBM_API_KEY:
        raise RuntimeError("IBM_API_KEY is not configured")

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": IBM_API_KEY,
    }
    resp = requests.post(IBM_IAM_URL, headers=headers, data=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    token = data.get("access_token")
    expires_in = int(data.get("expires_in", 3600))
    if not token:
        raise RuntimeError(f"Failed to obtain IBM IAM token: {data}")
    expiry = time.time() + max(0, expires_in - 60)  # refresh 60s early
    return token, expiry


def _get_ibm_iam_token() -> str:
    global _ibm_iam_token, _ibm_iam_expiry
    now = time.time()
    if not _ibm_iam_token or now >= _ibm_iam_expiry:
        _ibm_iam_token, _ibm_iam_expiry = _refresh_ibm_iam_token()
        logger.info("Refreshed IBM IAM token; expires at %s", _ibm_iam_expiry)
    return _ibm_iam_token  # type: ignore[return-value]


def ibm_tts(text: str, voice_id: str) -> bytes:
    """Synthesize speech using IBM Text-to-Speech REST API. Returns MP3 bytes."""
    if not IBM_TTS_URL:
        raise RuntimeError("IBM_TTS_URL is not configured")

    token = _get_ibm_iam_token()
    synth_url = f"{IBM_TTS_URL}/v1/synthesize?voice={voice_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "audio/mp3",
        "Content-Type": "application/json",
    }
    payload = {"text": text}
    try:
        resp = requests.post(synth_url, headers=headers, data=json.dumps(payload), timeout=120)
        # Watson TTS may return 200 with audio or a JSON error; check content-type
        ct = resp.headers.get("Content-Type", "")
        if resp.status_code >= 400:
            raise RuntimeError(f"IBM TTS error: {resp.status_code} {resp.text[:200]}")
        if "application/json" in ct:
            # Error payload passed through
            raise RuntimeError(f"IBM TTS error payload: {resp.text[:200]}")
        return resp.content
    except requests.HTTPError as e:
        logger.exception("IBM TTS HTTP error")
        raise RuntimeError(f"IBM TTS HTTP error: {e.response.status_code} {e.response.text[:200]}") from e
    except Exception:
        logger.exception("IBM TTS call failed")
        raise


@app.before_request
def init_session():
    session.permanent = True
    session.setdefault("narrations", [])


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get text from file upload or textarea
            file = request.files.get("file_input")
            text = ""
            if file and file.filename and file.filename.lower().endswith(".txt"):
                text = file.read().decode("utf-8", errors="ignore")
            else:
                text = (request.form.get("text_input") or "").strip()

            if not text:
                raise ValueError("Please provide input via file upload or text area.")

            if len(text) > MAX_TEXT_LENGTH:
                text = text[:MAX_TEXT_LENGTH]
                flash(f"Input truncated to {MAX_TEXT_LENGTH} characters due to length limits.", "warning")

            tone_label = request.form.get("tone") or "Neutral"
            if tone_label not in TONES:
                tone_label = "Neutral"

            voice_label = request.form.get("voice") or "Allison (en-US)"
            if voice_label not in VOICES:
                voice_label = "Allison (en-US)"
            voice_id = VOICES[voice_label]

            # Rewrite with Granite via HF Inference
            tone_desc = TONES[tone_label]
            prompt = (
                f"Rewrite the following text while preserving its meaning, style, and structure, "
                f"but adjust it to a {tone_desc} tone. Keep the language clear and natural.\n\n"
                f"Text:\n{text}"
            )
            logger.info("Calling HF Granite model: %s", REWRITE_MODEL)
            rewritten = hf_generate(prompt)

            # Generate TTS audio via IBM Cloud TTS
            logger.info("Synthesizing audio with IBM TTS voice=%s", voice_id)
            audio_bytes = ibm_tts(rewritten, voice_id=voice_id)

            # Store in session
            nid = str(uuid.uuid4())
            session["narrations"].insert(0, {
                "id": nid,
                "orig": text,
                "rew": rewritten,
                "audio_b64": base64.b64encode(audio_bytes).decode(),
                "tone": tone_label,
                "voice": voice_label,
            })
            flash("Audiobook generated!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            logger.exception("Generation failed")
            flash(str(e), "danger")
            return redirect(url_for("index"))

    return render_template(
        "index.html",
        tones=list(TONES.keys()),
        voices=list(VOICES.keys()),
        narrations=session.get("narrations", []),
    )


@app.route("/audio/<nid>")
def serve_audio(nid):
    rec = next((r for r in session.get("narrations", []) if r.get("id") == nid), None)
    if not rec:
        return "Not found", 404
    data = base64.b64decode(rec["audio_b64"]) if rec.get("audio_b64") else b""
    return send_file(io.BytesIO(data), mimetype="audio/mpeg")


@app.route("/download/<nid>")
def download_audio(nid):
    rec = next((r for r in session.get("narrations", []) if r.get("id") == nid), None)
    if not rec:
        return "Not found", 404
    data = base64.b64decode(rec["audio_b64"]) if rec.get("audio_b64") else b""
    return send_file(
        io.BytesIO(data),
        mimetype="audio/mpeg",
        as_attachment=True,
        download_name=f"{nid}.mp3",
    )


# Error pages
@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", error="Page not found"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", error="Internal server error"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)