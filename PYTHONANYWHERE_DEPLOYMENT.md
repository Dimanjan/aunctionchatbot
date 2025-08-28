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
4. Select **Python 3.12** (or the latest available)
5. Set the following configurations:

### Source Code
- **Source code**: `/home/aliaunction/aliaunction_clean`

### WSGI Configuration
- **WSGI configuration file**: `/home/aliaunction/aliaunction_clean/aliaunction/wsgi_production.py`

### Static Files
- **URL**: `/static/`
- **Directory**: `/home/aliaunction/aliaunction_clean/staticfiles`

### Media Files
- **URL**: `/media/`
- **Directory**: `/home/aliaunction/aliaunction_clean/media`

## Step 7: Update WSGI File

1. Open the WSGI file in the PythonAnywhere file editor:
   ```
   /home/aliaunction/aliaunction_clean/aliaunction/wsgi_production.py
   ```

2. Make sure the path is correct for your username:
   ```python
   path = '/home/aliaunction/aliaunction_clean'  # Update with your username
   ```

## Step 8: Set Environment Variables

1. Go to the **Files** tab in PythonAnywhere
2. Navigate to your project directory
3. Create a `.env` file with your environment variables
4. In your WSGI file, add code to load environment variables:

```python
import os
from pathlib import Path

# Load environment variables from .env file
env_path = Path('/home/aliaunction/aliaunction_clean/.env')
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Rest of your WSGI configuration...
```

## Step 9: Reload Web App

1. Go back to the **Web** tab
2. Click **Reload** button
3. Check the error logs if there are any issues

## Step 10: Test Your Application

1. Visit your site: `https://aliaunction.pythonanywhere.com`
2. Test the chatbot functionality
3. Verify all features are working

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed in your virtual environment
2. **Static Files Not Loading**: Verify the static files configuration and run `collectstatic` again
3. **Database Errors**: Check that migrations have been applied
4. **Environment Variables**: Ensure your `.env` file is properly formatted and loaded

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