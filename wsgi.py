#!/usr/bin/env python3
"""
WSGI configuration for Flask Gemini Bot.

This module contains the WSGI callable for production deployment.
It can be used with WSGI servers like Gunicorn, uWSGI, or mod_wsgi.

Usage examples:
    gunicorn wsgi:application
    gunicorn -w 4 -b 0.0.0.0:5000 wsgi:application
    uwsgi --http :5000 --wsgi-file wsgi.py --callable application
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask application
from app import app

# WSGI callable
application = app

if __name__ == "__main__":
    # This allows the script to be run directly for testing
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port, debug=False)