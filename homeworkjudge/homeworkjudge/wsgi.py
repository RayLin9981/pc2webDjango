"""
WSGI config for homeworkjudge project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys
sys.path.append('/var/www/homeworkjudge/1092homeworkjudge/.venv/lib/python3.8/site-packages')
sys.path.insert(0,'/var/www/homeworkjudge/1092homeworkjudge/.venv/lib/python3.8/site-packages')
sys.path.append('/var/www/homeworkjudge/1092homeworkjudge/homeworkjudge')
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homeworkjudge.settings')

application = get_wsgi_application()
