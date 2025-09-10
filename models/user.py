from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from core import db
from core.base_model import BaseModel

class User(BaseModel, UserMixin):
    """User model for authentication and user management"""
    
    __tablename__ = 'users'
    
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationship with projects
    projects = db.relationship('Project', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.is_admin = is_admin
        self.set_password(password)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches stored hash"""
        return check_password_hash(self.password, password)
    
    @classmethod
    def get_by_username(cls, username):
        """Get user by username"""
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def get_by_email(cls, email):
        """Get user by email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def create_user(cls, username, email, password, is_admin=False):
        """Create new user with validation"""
        if cls.get_by_username(username):
            return None  # Username already exists
        if cls.get_by_email(email):
            return None  # Email already exists
        
        user = cls(username=username, email=email, password=password, is_admin=is_admin)
        return user.save()
    
    def get_projects_count(self):
        """Get count of user's projects"""
        return len(self.projects)
    
    def to_dict(self):
        """Convert to dictionary, excluding password"""
        data = super().to_dict()
        data.pop('password', None)
        return data
    
    def __repr__(self):
        return f'<User {self.username}>'