from flask import flash, request
from flask_login import current_user, login_required
from core.base_controller import BaseController
from models.user import User

class UserController(BaseController):
    """Controller for user management"""
    
    model_class = User
    
    def get_all_users(self):
        """Get all users (admin only)"""
        if not current_user.is_authenticated or not current_user.is_admin:
            return []
        
        return self.model_class.get_all()
    
    def get_user(self, user_id):
        """Get specific user"""
        if not current_user.is_authenticated:
            return None
        
        # Users can view their own profile, admins can view any
        user = self.get_by_id(user_id)
        if user and (current_user.is_admin or current_user.id == user_id):
            return user
        
        return None
    
    def create_user(self, username, email, password, confirm_password, is_admin=False):
        """Create new user (admin only)"""
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Administrator access required', 'error')
            return None
        
        # Validation
        if not self._validate_user_data(username, email, password, confirm_password):
            return None
        
        # Check if username or email already exists
        if User.get_by_username(username):
            flash('Username already exists', 'error')
            return None
        
        if User.get_by_email(email):
            flash('Email already exists', 'error')
            return None
        
        # Create user
        user = User.create_user(username, email, password, is_admin)
        if user:
            flash(f'User "{user.username}" created successfully!', 'success')
        
        return user
    
    def update_user(self, user_id, username, email, is_admin=None):
        """Update existing user"""
        user = self.get_user(user_id)
        if not user:
            flash('User not found', 'error')
            return None
        
        # Only admins or the user themselves can update
        if not (current_user.is_admin or current_user.id == user_id):
            flash('Permission denied', 'error')
            return None
        
        # Validation
        if not username or len(username.strip()) < 3:
            flash('Username must be at least 3 characters long', 'error')
            return None
        
        if not email or '@' not in email:
            flash('Valid email is required', 'error')
            return None
        
        # Check for unique username and email
        existing_user = User.get_by_username(username)
        if existing_user and existing_user.id != user_id:
            flash('Username already taken', 'error')
            return None
        
        existing_email = User.get_by_email(email)
        if existing_email and existing_email.id != user_id:
            flash('Email already registered', 'error')
            return None
        
        # Update user
        data = {
            'username': username.strip(),
            'email': email.strip()
        }
        
        # Only admins can change admin status
        if is_admin is not None and current_user.is_admin:
            data['is_admin'] = is_admin
        
        updated_user = self.update(user_id, data)
        if updated_user:
            flash(f'User "{updated_user.username}" updated successfully!', 'success')
        
        return updated_user
    
    def update_password(self, user_id, current_password, new_password, confirm_password):
        """Update user password"""
        user = self.get_user(user_id)
        if not user:
            flash('User not found', 'error')
            return False
        
        # Users can only change their own password, admins can change any
        if not (current_user.is_admin or current_user.id == user_id):
            flash('Permission denied', 'error')
            return False
        
        # Verify current password for non-admin requests
        if not current_user.is_admin and not user.check_password(current_password):
            flash('Current password is incorrect', 'error')
            return False
        
        # Validate new password
        if not new_password or len(new_password) < 6:
            flash('New password must be at least 6 characters long', 'error')
            return False
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return False
        
        # Update password
        user.set_password(new_password)
        user.save()
        flash('Password updated successfully!', 'success')
        return True
    
    def delete_user(self, user_id):
        """Delete user (admin only)"""
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Administrator access required', 'error')
            return False
        
        user = self.get_by_id(user_id)
        if not user:
            flash('User not found', 'error')
            return False
        
        # Prevent self-deletion
        if user.id == current_user.id:
            flash('You cannot delete your own account', 'error')
            return False
        
        username = user.username
        
        if self.delete(user_id):
            flash(f'User "{username}" deleted successfully!', 'success')
            return True
        
        return False
    
    def _validate_user_data(self, username, email, password, confirm_password):
        """Validate user form data"""
        if not username or len(username.strip()) < 3:
            flash('Username must be at least 3 characters long', 'error')
            return False
        
        if not email or '@' not in email:
            flash('Valid email is required', 'error')
            return False
        
        if not password or len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return False
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return False
        
        # Check for valid username characters
        if not username.replace('_', '').replace('-', '').isalnum():
            flash('Username can only contain letters, numbers, hyphens, and underscores', 'error')
            return False
        
        return True