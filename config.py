import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database settings
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'ai_prompt_manager')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '04040404')
    
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

    MAX_ATTACHMENT_SIZE = int(os.environ.get('MAX_ATTACHMENT_SIZE', 512 * 1024))  # 512 KB
    MAX_ATTACHMENTS_PER_PROMPT = int(os.environ.get('MAX_ATTACHMENTS_PER_PROMPT', 20))