#!/bin/bash

# PythonAnywhere Setup Script for Aliaunction
# Run this script in your PythonAnywhere bash console

echo "🚀 Setting up Aliaunction on PythonAnywhere..."

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs cache media staticfiles

# Set up virtual environment
echo "🐍 Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating .env file template..."
    cat > .env << EOF
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False

# Email Settings (optional)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# OpenAI API Key for Chatbot
OPENAI_API_KEY=your-openai-api-key-here

# Default Email
DEFAULT_FROM_EMAIL=no-reply@aliaunction.com
EOF
    echo "⚠️  Please update the .env file with your actual values"
fi

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Collect static files
echo "📄 Collecting static files..."
python manage.py collectstatic --noinput

# Populate FAQ data
echo "🤖 Populating FAQ data for chatbot..."
python manage.py populate_faq

echo ""
echo "✅ Setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Update your .env file with actual values"
echo "2. Configure your PythonAnywhere web app:"
echo "   - Source code: /home/aliaunction/aliaunction_clean"
echo "   - WSGI file: /home/aliaunction/aliaunction_clean/aliaunction/wsgi_production.py"
echo "3. Set up static files:"
echo "   - URL: /static/"
echo "   - Directory: /home/aliaunction/aliaunction_clean/staticfiles"
echo "4. Set up media files:"
echo "   - URL: /media/"
echo "   - Directory: /home/aliaunction/aliaunction_clean/media"
echo "5. Reload your web app"
echo ""
echo "🌐 Your site will be available at: https://aliaunction.pythonanywhere.com" 