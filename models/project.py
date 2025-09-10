from core import db
from core.base_model import BaseModel

class Project(BaseModel):
    """Project model for organizing prompts"""
    
    __tablename__ = 'projects'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Relationship with prompts
    prompts = db.relationship('Prompt', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, user_id, name, description=None):
        self.user_id = user_id
        self.name = name
        self.description = description
    
    @classmethod
    def get_by_user(cls, user_id):
        """Get all projects for a specific user"""
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_user_project(cls, user_id, project_id):
        """Get specific project belonging to user"""
        return cls.query.filter_by(id=project_id, user_id=user_id).first()
    
    def get_prompts_count(self):
        """Get count of prompts in this project"""
        return len(self.prompts)
    
    def get_latest_prompts(self, limit=5):
        """Get latest prompts in this project"""
        return [prompt for prompt in self.prompts[:limit]]
    
    def is_owned_by(self, user_id):
        """Check if project is owned by specific user"""
        return self.user_id == user_id
    
    def __repr__(self):
        return f'<Project {self.name}>'