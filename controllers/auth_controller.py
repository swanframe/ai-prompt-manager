from flask import flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from core.base_controller import BaseController
from models.user import User

class AuthController(BaseController):
    """Controller for user authentication"""
    
    model_class = User
    
    def login(self, username, password, remember=False):
        """Handle user login"""
        if current_user.is_authenticated:
            return redirect(url_for('project.dashboard'))
        
        user = User.get_by_username(username)
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f'Welcome back, {user.username}!', 'success')
            
            # Redirect to intended page or dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('project.dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return None
    
    def register(self, username, email, password, confirm_password):
        """Handle user registration"""
        if current_user.is_authenticated:
            return redirect(url_for('project.dashboard'))
        
        # Validation (update to include email validation)
        if not self._validate_registration(username, email, password, confirm_password):
            return None
        
        # Check if user already exists
        if User.get_by_username(username):
            flash('Username already exists', 'error')
            return None
        
        # Check if email already exists
        if User.get_by_email(email):
            flash('Email already exists', 'error')
            return None
        
        # Create new user with email
        user = User.create_user(username, email, password)
        if user:
            login_user(user)
            flash(f'Account created successfully! Welcome, {user.username}!', 'success')
            return redirect(url_for('project.dashboard'))
        else:
            flash('Error creating account', 'error')
            return None
    
    def logout(self):
        """Handle user logout"""
        username = current_user.username if current_user.is_authenticated else None
        logout_user()
        
        if username:
            flash(f'Goodbye, {username}!', 'info')
        
        return redirect(url_for('auth.login'))
    
    def _validate_registration(self, username, email, password, confirm_password):
        """Validate registration form data"""
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