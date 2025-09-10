from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()

def init_app_extensions(app):
    """Initialize Flask extensions"""
    db.init_app(app)