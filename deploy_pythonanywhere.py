#!/usr/bin/env python3
"""
Deployment script for PythonAnywhere.
This script helps set up the aliaunction project on PythonAnywhere.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories."""
    directories = ['logs', 'cache', 'media']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_environment():
    """Set up environment variables."""
    env_file = Path('.env')
    if not env_file.exists():
        env_content = """# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False

# Email Settings (optional)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# OpenAI API Key for Chatbot
OPENAI_API_KEY=your-openai-api-key-here

# Default Email
DEFAULT_FROM_EMAIL=no-reply@aliaunction.com
"""
        env_file.write_text(env_content)
        print("✅ Created .env file template")
        print("⚠️  Please update the .env file with your actual values")

def main():
    """Main deployment function."""
    print("🚀 Starting PythonAnywhere Deployment Setup")
    print("=" * 50)
    
    # Create necessary directories
    create_directories()
    
    # Set up environment
    setup_environment()
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        return False
    
    # Run migrations
    if not run_command("python manage.py migrate", "Running database migrations"):
        return False
    
    # Create superuser (optional)
    print("\n🤔 Would you like to create a superuser? (y/n): ", end="")
    create_superuser = input().lower().strip()
    if create_superuser == 'y':
        run_command("python manage.py createsuperuser", "Creating superuser")
    
    # Populate FAQ data
    if not run_command("python manage.py populate_faq", "Populating FAQ data"):
        print("⚠️  FAQ population failed, but continuing...")
    
    print("\n" + "=" * 50)
    print("✅ Deployment setup completed!")
    print("\n📋 Next steps:")
    print("1. Update your .env file with actual values")
    print("2. Configure your PythonAnywhere web app:")
    print("   - Source code: /home/aliaunction/aliaunction_clean")
    print("   - WSGI file: /home/aliaunction/aliaunction_clean/aliaunction/wsgi_production.py")
    print("3. Set up static files in PythonAnywhere:")
    print("   - URL: /static/")
    print("   - Directory: /home/aliaunction/aliaunction_clean/staticfiles")
    print("4. Set up media files in PythonAnywhere:")
    print("   - URL: /media/")
    print("   - Directory: /home/aliaunction/aliaunction_clean/media")
    print("5. Reload your web app")
    print("\n🌐 Your site will be available at: https://aliaunction.pythonanywhere.com")

if __name__ == "__main__":
    main() 