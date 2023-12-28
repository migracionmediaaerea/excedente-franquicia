import os
import sys

from pathlib import Path
from dotenv import load_dotenv
from django.core.asgi import get_asgi_application

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(BASE_DIR, "comun"))
sys.path.append(os.path.join(BASE_DIR, "lineascomun"))
load_dotenv(os.path.join(BASE_DIR, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproject.settings')

application = get_asgi_application()
