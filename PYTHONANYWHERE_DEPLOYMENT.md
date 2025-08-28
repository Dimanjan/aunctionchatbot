# PythonAnywhere Deployment Guide

This guide will help you deploy the Aliaunction auction website with chatbot functionality on PythonAnywhere.

## Prerequisites

1. A PythonAnywhere account (Beginner plan is sufficient)
2. Your OpenAI API key for the chatbot functionality
3. Git access to your repository

## Step 1: Clone the Repository

1. Open a PythonAnywhere Bash console
2. Navigate to your home directory:
   ```bash
   cd ~
   ```
3. Clone your repository:
   ```bash
   git clone https://github.com/Dimanjan/aunctionchatbot.git aliaunction_clean
   cd aliaunction_clean
   ```

## Step 2: Set Up Python Environment

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Step 3: Configure Environment Variables

**Option A: Using .env file (Recommended)**
1. Create a `.env` file in your project root:
   ```bash
   nano .env
   ```

2. Add the following content (replace with your actual values):
   ```env
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
   ```

3. Save and exit (Ctrl+X, Y, Enter)

**Option B: Direct environment variables in WSGI file**
Use the simplified WSGI file: `aliaunction/wsgi_production_simple.py`

## Step 4: Set Up Database

1. Run migrations:
   ```bash
   python manage.py migrate
   ```

2. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

3. Populate FAQ data for the chatbot:
   ```bash
   python manage.py populate_faq
   ```

## Step 5: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Step 6: Configure Web App

1. Go to the **Web** tab in your PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.12**

## Step 7: Configure Virtual Environment

1. In the **Virtualenv** section, enter:
   ```
   aliaunction-virtualenv
   ```
2. Click **OK**

## Step 8: Set Source Code Path

1. In the **Code** section, set:
   - **Source code**: `/home/aliaunction/aliaunction_clean`
   - **Working directory**: `/home/aliaunction/aliaunction_clean`

## Step 9: Configure WSGI File

1. Click on the **WSGI configuration file** link in the Code section
2. **Choose one of the following options:**

### Option A: Using .env file (Recommended)
Replace the entire content with:
```python
# +++++++++++ DJANGO +++++++++++
import os
import sys

# Add the project directory to the Python path
path = '/home/aliaunction/aliaunction_clean'
if path not in sys.path:
    sys.path.append(path)

# Load environment variables from .env file
env_path = '/home/aliaunction/aliaunction_clean/.env'
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith('#'):
                try:
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
                except ValueError:
                    # Skip lines that don't have proper key=value format
                    continue

# Set the Django settings module for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aliaunction.settings_production')

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Option B: Direct environment variables
Replace the entire content with:
```python
# +++++++++++ DJANGO +++++++++++
import os
import sys

# Add the project directory to the Python path
path = '/home/aliaunction/aliaunction_clean'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables directly (replace with your actual values)
os.environ['SECRET_KEY'] = 'your-secret-key-here'  # Replace with actual secret key
os.environ['DEBUG'] = 'False'
os.environ['OPENAI_API_KEY'] = 'your-openai-api-key-here'  # Replace with actual API key
os.environ['EMAIL_HOST_USER'] = 'your-email@gmail.com'  # Optional
os.environ['EMAIL_HOST_PASSWORD'] = 'your-app-password'  # Optional
os.environ['DEFAULT_FROM_EMAIL'] = 'no-reply@aliaunction.com'

# Set the Django settings module for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aliaunction.settings_production')

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

3. **Save** the file

## Step 10: Configure Static Files

1. In the **Static files** section, add:
   - **URL**: `/static/`
   - **Directory**: `/home/aliaunction/aliaunction_clean/staticfiles`

## Step 11: Configure Media Files

1. In the **Static files** section, add another entry:
   - **URL**: `/media/`
   - **Directory**: `/home/aliaunction/aliaunction_clean/media`

## Step 12: Reload Your Web App

1. Go back to the **Web** tab
2. Click the **Reload** button (green button at the top)

## Step 13: Test Your Site

1. Visit your site: `https://aliaunction.pythonanywhere.com`
2. Test the chatbot functionality
3. Verify all features are working

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed in your virtual environment
2. **Static Files Not Loading**: Verify the static files configuration and run `collectstatic` again
3. **Database Errors**: Check that migrations have been applied
4. **Environment Variables**: Ensure your `.env` file is properly formatted and loaded

### WSGI File Errors

If you see errors like "ValueError: not enough values to unpack", it means there's an issue with the environment variable loading. Use Option B (direct environment variables) instead of Option A.

### Error Logs

Check the error logs in the **Web** tab of your PythonAnywhere dashboard for specific error messages.

### File Permissions

Make sure your files have the correct permissions:
```bash
chmod 755 /home/aliaunction/aliaunction_clean
chmod 644 /home/aliaunction/aliaunction_clean/.env
```

## Security Considerations

1. **Secret Key**: Use a strong, unique secret key
2. **Environment Variables**: Never commit sensitive information to version control
3. **HTTPS**: PythonAnywhere provides HTTPS by default
4. **Debug Mode**: Ensure DEBUG is set to False in production

## Performance Optimization

1. **Static Files**: Use a CDN for better performance
2. **Database**: Consider using PostgreSQL for better performance with larger datasets
3. **Caching**: The application includes file-based caching for PythonAnywhere

## Monitoring

1. **Logs**: Check the logs directory for application logs
2. **PythonAnywhere Stats**: Monitor your resource usage in the dashboard
3. **Error Tracking**: Set up error tracking for production monitoring

## Backup Strategy

1. **Database**: Regularly backup your SQLite database
2. **Code**: Your code is already in version control
3. **Media Files**: Backup uploaded files regularly

## Support

If you encounter issues:
1. Check the PythonAnywhere documentation
2. Review Django deployment best practices
3. Check the error logs in your PythonAnywhere dashboard

## Next Steps

After successful deployment:
1. Set up a custom domain (if desired)
2. Configure email settings for user notifications
3. Set up monitoring and logging
4. Consider upgrading to a paid plan for better performance

---

**Note**: This guide assumes you're using the username `aliaunction` on PythonAnywhere. Replace it with your actual username in all paths and configurations. 