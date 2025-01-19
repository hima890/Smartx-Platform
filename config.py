import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("./.env")


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    DEBUG = os.environ.get('DEBUG')
