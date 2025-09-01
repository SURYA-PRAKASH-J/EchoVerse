# Google Colab Setup for EchoVerse Flask App

## 🚀 Quick Google Colab Deployment

### Step 1: Install Dependencies
```python
# Install required packages
!pip install flask python-dotenv ibm-watsonx-ai requests pyngrok

# Install ngrok for public URL access
!pip install pyngrok
```

### Step 2: Set Environment Variables
```python
import os

# Set environment variables (replace with your actual values)
os.environ['FLASK_SECRET_KEY'] = 'your_super_secret_key_here'
os.environ['IBM_API_KEY'] = 'your_ibm_watson_api_key'
os.environ['IBM_PROJECT_ID'] = 'your_ibm_project_id'
os.environ['IBM_URL'] = 'https://us-south.ml.cloud.ibm.com'
os.environ['IBM_TTS_URL'] = 'https://api.us-south.text-to-speech.watson.cloud.ibm.com'
```

### Step 3: Create Template Directory
```python
# Create templates directory
!mkdir -p templates
```

### Step 4: Upload Files
Upload the following files to your Colab session:
- `echoverse_flask.py` - Main Flask application
- `templates/index.html` - Main UI template  
- `templates/error.html` - Error page template

### Step 5: Set up ngrok for Public Access
```python
from pyngrok import ngrok
import threading
import time

# Set your ngrok auth token (get from https://ngrok.com/)
ngrok.set_auth_token("326o6R0nYR95F7KuL5H9ZKAtOP6_29nVVdvM2TjzUiVFKwjSi")

# Function to run Flask app
def run_flask():
    from echoverse_flask import app
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# Start Flask in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Wait for Flask to start
time.sleep(5)

# Create public tunnel
public_url = ngrok.connect(5000)
print(f"🚀 EchoVerse is now running at: {public_url}")
print(f"📱 Access your app from anywhere using this URL!")
```

### Step 6: Alternative Direct Run (if ngrok not needed)
```python
# If you only need local access within Colab
from echoverse_flask import app

# This will run on Colab's local network
app.run(host='0.0.0.0', port=5000, debug=True)
```

## 📝 Complete Colab Notebook Code

```python
# Cell 1: Install Dependencies
!pip install flask python-dotenv ibm-watsonx-ai requests pyngrok

# Cell 2: Set Environment Variables
import os

# ⚠️ IMPORTANT: Replace these with your actual IBM Watson credentials
os.environ['FLASK_SECRET_KEY'] = 'your_flask_secret_key_replace_this'
os.environ['IBM_API_KEY'] = 'your_ibm_api_key_replace_this'
os.environ['IBM_PROJECT_ID'] = 'your_project_id_replace_this'
os.environ['IBM_URL'] = 'https://us-south.ml.cloud.ibm.com'
os.environ['IBM_TTS_URL'] = 'https://api.us-south.text-to-speech.watson.cloud.ibm.com'

print("✅ Environment variables set!")

# Cell 3: Create Project Structure
!mkdir -p templates
!mkdir -p temp_uploads

print("✅ Directory structure created!")

# Cell 4: Create Flask App (paste the echoverse_flask.py content here)
%%writefile echoverse_flask.py
# [Paste the complete echoverse_flask.py code here]

# Cell 5: Create Main Template (paste the index.html content here)
%%writefile templates/index.html
# [Paste the complete index.html code here]

# Cell 6: Create Error Template (paste the error.html content here)
%%writefile templates/error.html
# [Paste the complete error.html code here]

# Cell 7: Run the Application with ngrok
from pyngrok import ngrok
import threading
import time

# Set ngrok auth token (get free token from https://ngrok.com/)
ngrok.set_auth_token("your_ngrok_token_here")  # Replace with actual token

def run_flask():
    import sys
    sys.path.append('/content')
    from echoverse_flask import app
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# Start Flask app in background
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Wait for app to start
time.sleep(8)

# Create public tunnel
try:
    public_url = ngrok.connect(5000)
    print("🎉 SUCCESS! EchoVerse is now live!")
    print(f"🌐 Public URL: {public_url}")
    print("📱 You can access this URL from any device, anywhere!")
    print("🔊 Start creating audiobooks with AI!")
except Exception as e:
    print(f"❌ Error setting up ngrok: {e}")
    print("💡 Try running without ngrok for local access only")
```

## 🔑 Getting IBM Watson Credentials

### Step 1: IBM Cloud Account
1. Go to [IBM Cloud](https://cloud.ibm.com/)
2. Sign up for free account (no credit card required for Lite plan)

### Step 2: Watson Machine Learning Service
1. Navigate to **Catalog** → **AI/Machine Learning**
2. Select **Watson Machine Learning**
3. Choose **Lite plan** (free tier)
4. Click **Create**
5. Go to **Manage** tab
6. Copy **API Key**

### Step 3: Create watsonx.ai Project
1. Go to [watsonx.ai](https://dataplatform.cloud.ibm.com/wx)
2. Create new project
3. Copy **Project ID** from project settings

### Step 4: Text-to-Speech Service
1. Go back to **IBM Cloud Catalog**
2. Select **Text to Speech**
3. Choose **Lite plan** (free tier)
4. Click **Create**
5. Copy service **URL** from credentials

### Step 5: Get ngrok Token (Optional)
1. Go to [ngrok.com](https://ngrok.com/)
2. Sign up for free account
3. Go to **Your Authtoken** page
4. Copy the token for public URL access

## 🚀 Quick Test Commands

```python
# Test IBM Watson connection
import os
from ibm_watsonx_ai import Credentials

try:
    credentials = Credentials(
        url=os.getenv('IBM_URL'),
        api_key=os.getenv('IBM_API_KEY')
    )
    print("✅ IBM Watson credentials are valid!")
except Exception as e:
    print(f"❌ Watson connection failed: {e}")

# Test Flask app locally
from echoverse_flask import app
print("✅ Flask app loaded successfully!")

# Check if all templates exist
import os
templates = ['templates/index.html', 'templates/error.html']
for template in templates:
    if os.path.exists(template):
        print(f"✅ {template} found")
    else:
        print(f"❌ {template} missing")
```

## 🎯 Usage Instructions

1. **Run all cells** in order
2. **Replace placeholder credentials** with your actual IBM Watson credentials
3. **Get ngrok token** for public access (optional)
4. **Access the generated URL** to use EchoVerse
5. **Upload text files** or paste text directly
6. **Select tone and voice** for your audiobook
7. **Generate and download** your AI-powered audiobook!

## 🔧 Troubleshooting

### Common Issues:
- **Import errors**: Run `!pip install` commands again
- **Credential errors**: Double-check IBM Watson API key and project ID
- **ngrok errors**: Make sure you have a valid auth token
- **Template errors**: Ensure all HTML files are created properly

### Alternative without ngrok:
```python
# Simple local run (Colab internal access only)
from echoverse_flask import app
app.run(port=5000, debug=True)
```

This setup gives you a fully functional EchoVerse installation in Google Colab with public URL access!