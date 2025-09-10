from core import db
from core.base_model import BaseModel

class Prompt(BaseModel):
    """Prompt model for storing AI prompts"""
    
    __tablename__ = 'prompts'
    
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Relationship to multiple responses
    responses = db.relationship(
        'PromptResponse',
        backref='prompt',
        lazy=True,
        cascade='all, delete-orphan',
        order_by='PromptResponse.created_at'
    )

    attachments = db.relationship(
        'Attachment',
        backref='prompt',
        lazy=True,
        cascade='all, delete-orphan',
        order_by='Attachment.created_at'
    )

    def __init__(self, project_id, title, content):
        self.project_id = project_id
        self.title = title
        self.content = content
    
    @classmethod
    def get_by_project(cls, project_id):
        """Get all prompts for a specific project"""
        return cls.query.filter_by(project_id=project_id).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_project_prompt(cls, project_id, prompt_id):
        """Get specific prompt belonging to project"""
        return cls.query.filter_by(id=prompt_id, project_id=project_id).first()
    
    @classmethod
    def search_by_user(cls, user_id, search_term):
        """Search prompts by title or content for specific user"""
        from models.project import Project
        
        return cls.query.join(Project).filter(
            Project.user_id == user_id,
            db.or_(
                cls.title.ilike(f'%{search_term}%'),
                cls.content.ilike(f'%{search_term}%')
            )
        ).order_by(cls.created_at.desc()).all()
    
    def get_content_preview(self, length=100):
        """Get truncated content for preview"""
        if len(self.content) <= length:
            return self.content
        return self.content[:length] + '...'
    
    def is_owned_by_user(self, user_id):
        """Check if prompt belongs to specific user through project"""
        return self.project.user_id == user_id
    
    def __repr__(self):
        return f'<Prompt {self.title}>'