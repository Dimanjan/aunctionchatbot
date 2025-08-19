# 🤖 Chatbot Setup Guide

## Overview
The AuctionVistas chatbot is an AI-powered assistant that helps users with auction-related questions, bidding guidance, and platform navigation. It uses OpenAI's GPT-3.5-turbo model with a comprehensive fallback system.

## Features
- **AI-Powered Responses**: Uses OpenAI GPT-3.5-turbo for intelligent responses
- **Fallback System**: Comprehensive FAQ-based responses when AI is unavailable
- **Context Awareness**: Understands user's current page and authentication status
- **Real-time Chat**: Live chat widget with typing indicators
- **Admin Analytics**: Chat session monitoring and analytics dashboard
- **Mobile Responsive**: Works seamlessly on all devices

## Setup Instructions

### 1. Environment Variables
Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

Or add it to your `.env` file:
```
OPENAI_API_KEY=your-openai-api-key-here
```

### 2. Database Setup
Run migrations to create chatbot tables:
```bash
python manage.py migrate
```

### 3. Populate Sample Data
Load sample FAQ data and chatbot configuration:
```bash
python manage.py populate_faq
```

### 4. Start the Server
```bash
python manage.py runserver 8001
```

## Usage

### For Users
- The chatbot widget appears as a floating button on all pages
- Click the chat button to start a conversation
- Ask questions about bidding, payments, auctions, etc.
- The chatbot provides context-aware responses

### For Administrators
- Access chatbot analytics at `/chatbot/analytics/`
- Manage FAQ entries in Django admin
- Configure chatbot settings in Django admin
- Monitor chat sessions and user interactions

## API Endpoints

- `POST /chatbot/api/start/` - Start a new chat session
- `POST /chatbot/api/send/` - Send a message and get response
- `GET /chatbot/api/history/<session_id>/` - Get chat history
- `POST /chatbot/api/end/` - End a chat session

## Configuration

### Chatbot Settings (Django Admin)
- **Welcome Message**: Customizable welcome message
- **System Prompt**: AI system prompt for context
- **Max Tokens**: Maximum response length
- **Temperature**: Response creativity (0.0-1.0)

### FAQ Management
- Add/edit FAQ entries in Django admin
- Categorize questions for better organization
- Enable/disable specific FAQ entries

## Security Features
- No hardcoded API keys in code
- Environment variable-based configuration
- CSRF protection on all endpoints
- Session-based chat tracking
- Rate limiting ready

## Fallback System
When OpenAI API is unavailable or not configured:
- Uses FAQ database for responses
- Keyword-based response matching
- Graceful degradation without errors
- Maintains user experience

## Customization
- Modify `chatbot/services.py` for custom response logic
- Update `chatbot/templates/chatbot/widget.html` for UI changes
- Add new FAQ categories in Django admin
- Extend analytics in `chatbot/views.py`

## Troubleshooting

### Common Issues
1. **"No OpenAI API key configured"** - Set the OPENAI_API_KEY environment variable
2. **Chatbot not responding** - Check server logs for API errors
3. **Widget not appearing** - Ensure chatbot app is in INSTALLED_APPS
4. **Database errors** - Run `python manage.py migrate`

### Debug Mode
Enable Django debug mode to see detailed error messages:
```python
DEBUG = True  # in settings.py
```

## Performance
- Response time: < 2 seconds (with API)
- Fallback response time: < 100ms
- Supports concurrent users
- Efficient database queries

## Future Enhancements
- WebSocket support for real-time chat
- Voice chat integration
- Multi-language support
- Advanced analytics dashboard
- Custom chatbot personalities 