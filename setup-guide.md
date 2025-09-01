# EchoVerse Flask App - Complete Setup Guide

## 📋 Overview
EchoVerse is a professional Flask web application that transforms text into expressive audiobooks using IBM Watson AI technologies. This refactored version includes enterprise-grade features, professional UI design, comprehensive error handling, and responsive user experience.

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.8+ installed
- IBM Cloud account with Watson services
- Git (optional)

### 2. Project Setup

#### Step 1: Create Project Directory
```bash
mkdir echoverse-flask
cd echoverse-flask
```

#### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

#### Step 1: Copy Environment Template
```bash
cp .env.example .env
```

#### Step 2: Configure IBM Watson Services

##### A. IBM Watsonx AI Setup:
1. Go to [IBM Cloud Console](https://cloud.ibm.com/)
2. Create/access Watson Machine Learning service
3. Note down:
   - API Key
   - Project ID
   - Service URL

##### B. IBM Watson Text-to-Speech Setup:
1. Create Text-to-Speech service instance
2. Get service credentials:
   - API Key (same as above if using same instance)
   - Service URL

#### Step 3: Update .env File
```env
FLASK_SECRET_KEY=generate_a_secure_random_key_here
IBM_API_KEY=your_actual_api_key
IBM_PROJECT_ID=your_actual_project_id
IBM_URL=https://us-south.ml.cloud.ibm.com
IBM_TTS_URL=https://api.us-south.text-to-speech.watson.cloud.ibm.com
FLASK_ENV=development
```

### 4. File Structure
```
echoverse-flask/
├── echoverse_flask.py          # Main Flask application
├── templates/
│   ├── index.html              # Main UI template
│   ├── error.html              # Error page template
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── .env                        # Your actual environment (create this)
├── temp_uploads/               # Temporary upload directory (auto-created)
└── README.md                   # This file
```

### 5. Running the Application

#### Development Mode:
```bash
python echoverse_flask.py
```

#### Production Mode:
```bash
# Using Gunicorn (Linux/macOS)
gunicorn -w 4 -b 0.0.0.0:5000 echoverse_flask:app

# Using Waitress (Windows/Cross-platform)
waitress-serve --host=0.0.0.0 --port=5000 echoverse_flask:app
```

Access the application at: `http://localhost:5000`

## 🔧 IBM Watson API Setup Guide

### Step-by-Step IBM Cloud Configuration:

#### 1. Create IBM Cloud Account
- Visit [IBM Cloud](https://cloud.ibm.com/)
- Sign up for free account (includes free tier for Watson services)

#### 2. Set up Watson Machine Learning
1. Navigate to **Catalog > AI/Machine Learning**
2. Select **Watson Machine Learning**
3. Choose **Lite plan** (free)
4. Create service
5. Go to **Manage** tab → **Access (IAM)** 
6. Copy **API Key**
7. Create a project in watsonx.ai and copy **Project ID**

#### 3. Set up Text-to-Speech Service
1. Navigate to **Catalog > AI/Machine Learning**
2. Select **Text to Speech**
3. Choose **Lite plan** (free)
4. Create service
5. Go to **Manage** tab
6. Copy **API Key** and **URL**

#### 4. Configure Authentication
- The same API key can be used for both services if they're in the same account
- Update your `.env` file with the obtained credentials

## 🌟 Key Features

### Core Functionality:
- **Text Input**: Paste text or upload .txt files (up to 200MB)
- **AI Text Rewriting**: Transform tone (Neutral, Suspenseful, Inspiring)
- **Voice Synthesis**: Multiple voice options (Lisa, Michael, Allison, Kate)
- **Audio Generation**: High-quality MP3 output
- **Session Management**: Track multiple generations in one session

### Professional Features:
- **Responsive Design**: Mobile-first, professional UI
- **Real-time Validation**: Form validation with visual feedback
- **Drag & Drop**: File upload with drag-and-drop support
- **Progress Indicators**: Visual feedback during processing
- **Error Handling**: Comprehensive error management
- **Audio Controls**: Built-in audio player with download options
- **History Management**: Session-based narration history
- **Statistics**: File size and generation tracking

### Security & Performance:
- **Environment Variables**: Secure credential management
- **Input Validation**: Text length and file type validation
- **Session Security**: Secure session handling
- **Error Logging**: Comprehensive logging system
- **Rate Limiting**: Built-in request handling
- **File Security**: Secure file upload handling

## 🔧 Advanced Configuration

### Custom Voice Configuration:
```python
VOICES = {
    "Lisa": "en-US_LisaV3Voice",
    "Michael": "en-US_MichaelV3Voice", 
    "Allison": "en-US_AllisonV3Voice",
    "Kate": "en-US_KateV3Voice"
    # Add more voices as needed
}
```

### Tone Customization:
```python
TONES = {
    "Neutral": "neutral and clear",
    "Suspenseful": "suspenseful and dramatic", 
    "Inspiring": "inspiring and motivational"
    # Add custom tones
}
```

### Text Processing Limits:
```python
MAX_TEXT_LENGTH = 5000  # Adjust based on your needs
```

## 🐛 Troubleshooting

### Common Issues:

#### 1. Import Errors:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. Watson API Errors:
- Verify API keys in `.env` file
- Check IBM Cloud service status
- Ensure project ID is correct
- Verify service URLs are correct

#### 3. File Upload Issues:
- Check file size (max 200MB)
- Ensure file is UTF-8 encoded
- Verify file extension is `.txt`

#### 4. Audio Generation Fails:
- Check TTS service quota
- Verify voice names are correct
- Check text length (too long may fail)

### Environment Issues:
```bash
# Check Python version
python --version  # Should be 3.8+

# Check environment variables
python -c "import os; print(os.getenv('IBM_API_KEY'))"

# Test Watson connection
python -c "from ibm_watsonx_ai import Credentials; print('Watson SDK loaded')"
```

## 📊 Performance Optimization

### For Production:
1. **Use Gunicorn/uWSGI**: Better than Flask dev server
2. **Enable Logging**: Configure proper logging levels
3. **Add Caching**: Consider Redis for session storage
4. **Database**: For permanent user data (optional)
5. **CDN**: For static assets
6. **SSL**: Always use HTTPS in production

### Resource Management:
- Limit concurrent audio generations
- Implement request queuing for heavy loads
- Monitor IBM Watson usage quotas
- Set up proper error monitoring

## 🔒 Security Considerations

### Production Security:
1. **Secret Key**: Use strong random secret key
2. **HTTPS**: Always use SSL in production
3. **Input Validation**: All inputs are validated
4. **File Security**: Upload restrictions in place
5. **Session Security**: Secure session configuration
6. **API Keys**: Never commit to version control

### Privacy:
- No persistent user data storage
- Session-only audio storage
- Automatic cleanup of temporary files
- No user tracking implemented

## 📈 Monitoring & Logging

### Application Monitoring:
```python
# Check application status
GET /status
# Returns JSON with service health
```

### Log Files:
- Application logs are printed to console
- Configure file logging for production
- Monitor Watson API usage and errors

## 🚀 Deployment Options

### Local Development:
```bash
python echoverse_flask.py
```

### Google Colab (as requested):
1. Upload all files to Colab
2. Install requirements: `!pip install -r requirements.txt`
3. Set environment variables in Colab secrets
4. Run with ngrok for public access:
```python
!pip install pyngrok
from pyngrok import ngrok
ngrok.set_auth_token("your_token")
public_url = ngrok.connect(5000)
print(f"Public URL: {public_url}")
```

### Cloud Deployment:
- **Heroku**: Add Procfile: `web: gunicorn echoverse_flask:app`
- **Google Cloud Run**: Use Dockerfile
- **AWS Lambda**: With Zappa framework
- **IBM Cloud**: Native Watson integration

## 📞 Support

### Getting Help:
1. Check troubleshooting section
2. Review IBM Watson documentation
3. Check Flask documentation for web framework issues
4. Verify all environment variables are set correctly

### IBM Watson Resources:
- [Watson Machine Learning Docs](https://cloud.ibm.com/docs/watson-machine-learning)
- [Text-to-Speech Docs](https://cloud.ibm.com/docs/text-to-speech)
- [IBM watsonx.ai SDK](https://ibm.github.io/watsonx-python-sdk/)

This setup provides a production-ready, scalable Flask application with professional UI design and comprehensive error handling, perfect for deployment in various environments including Google Colab.