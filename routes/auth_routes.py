from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from controllers.auth_controller import AuthController

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Initialize controller
auth_controller = AuthController()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and form handling"""
    if current_user.is_authenticated:
        return redirect(url_for('project.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))
        
        result = auth_controller.login(username, password, remember)
        if result:
            return result
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page and form handling"""
    if current_user.is_authenticated:
        return redirect(url_for('project.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()  # Get email from form
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        result = auth_controller.register(username, email, password, confirm_password)  # Pass email
        if result:
            return result
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout current user"""
    return auth_controller.logout()

# Root redirect to login
@auth_bp.route('/')
def index():
    """Redirect root to login"""
    if current_user.is_authenticated:
        return redirect(url_for('project.dashboard'))
    return redirect(url_for('auth.login'))