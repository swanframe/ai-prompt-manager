from flask import flash, redirect, url_for, request, jsonify
from flask_login import current_user

class BaseController:
    """Base controller with common functionality"""
    
    model_class = None
    
    def __init__(self):
        if not self.model_class:
            raise NotImplementedError("model_class must be defined")
    
    def get_all(self):
        """Get all records"""
        return self.model_class.get_all()
    
    def get_by_id(self, id):
        """Get record by ID"""
        return self.model_class.get_by_id(id)
    
    def create(self, data):
        """Create new record"""
        try:
            instance = self.model_class(**data)
            instance.save()
            return instance
        except Exception as e:
            flash(f'Error creating record: {str(e)}', 'error')
            return None
    
    def update(self, id, data):
        """Update existing record"""
        try:
            instance = self.get_by_id(id)
            if not instance:
                flash('Record not found', 'error')
                return None
            
            for key, value in data.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            instance.save()
            return instance
        except Exception as e:
            flash(f'Error updating record: {str(e)}', 'error')
            return None
    
    def delete(self, id):
        """Delete record"""
        try:
            instance = self.get_by_id(id)
            if not instance:
                flash('Record not found', 'error')
                return False
            
            instance.delete()
            flash('Record deleted successfully', 'success')
            return True
        except Exception as e:
            flash(f'Error deleting record: {str(e)}', 'error')
            return False
    
    def check_ownership(self, instance, user_field='user_id'):
        """Check if current user owns the record"""
        if not current_user.is_authenticated:
            return False
        
        if hasattr(instance, user_field):
            return getattr(instance, user_field) == current_user.id
        
        return False
    
    def get_form_data(self, fields):
        """Extract form data for specified fields"""
        data = {}
        for field in fields:
            value = request.form.get(field)
            if value:
                data[field] = value.strip()
        return data
    
    def validate_required_fields(self, data, required_fields):
        """Validate that required fields are present"""
        missing_fields = []
        for field in required_fields:
            if not data.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            flash(f'Required fields missing: {", ".join(missing_fields)}', 'error')
            return False
        
        return True