from datetime import datetime
from core import db

class BaseModel(db.Model):
    """Base model with common fields and methods"""
    
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def save(self):
        """Save instance to database"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Delete instance from database"""
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_by_id(cls, id):
        """Get instance by ID"""
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls):
        """Get all instances"""
        return cls.query.all()
    
    @classmethod
    def get_paginated(cls, page=1, per_page=20):
        """Get paginated results"""
        return cls.query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
    
    def to_dict(self):
        """Convert instance to dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }