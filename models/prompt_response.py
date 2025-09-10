# models/prompt_response.py
from core import db
from core.base_model import BaseModel

class PromptResponse(BaseModel):
    """Individual messages/replies for a Prompt (system/user/assistant)"""
    __tablename__ = 'prompt_responses'

    # relation to prompts.id
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompts.id', ondelete='CASCADE'), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'system','user','assistant'
    content = db.Column(db.Text, nullable=False)
    extra_metadata = db.Column(db.JSON, nullable=True)  # renamed from 'metadata'

    def __init__(self, prompt_id, role, content, extra_metadata=None):
        self.prompt_id = prompt_id
        self.role = role
        self.content = content
        self.extra_metadata = extra_metadata