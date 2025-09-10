from core import db
from core.base_model import BaseModel

class Attachment(BaseModel):
    __tablename__ = 'attachments'

    prompt_id = db.Column(
        db.Integer,
        db.ForeignKey('prompts.id', ondelete='CASCADE'),
        nullable=False
    )
    filename = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False, default='text/plain')
    content = db.Column(db.Text, nullable=False)