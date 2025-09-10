from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from controllers.user_controller import UserController

# Create blueprint
user_bp = Blueprint('user', __name__, url_prefix='/users')

# Initialize controller
user_controller = UserController()

@user_bp.route('/')
@login_required
def list_users():
    """List all users (admin only)"""
    if not current_user.is_admin:
        return redirect(url_for('project.dashboard'))
    
    users = user_controller.get_all_users()
    return render_template('users.html', users=users)

@user_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_user():
    """Create new user (admin only)"""
    if not current_user.is_admin:
        return redirect(url_for('project.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        is_admin = bool(request.form.get('is_admin'))
        
        user = user_controller.create_user(username, email, password, confirm_password, is_admin)
        if user:
            return redirect(url_for('user.list_users'))
    
    return render_template('user_form.html', action='create')

@user_bp.route('/<int:user_id>')
@login_required
def view_user(user_id):
    """View specific user"""
    user = user_controller.get_user(user_id)
    if not user:
        return redirect(url_for('user.list_users'))
    
    return render_template('user_detail.html', user=user)

@user_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Edit existing user"""
    user = user_controller.get_user(user_id)
    if not user:
        return redirect(url_for('user.list_users'))
    
    # Only admins or the user themselves can edit
    if not (current_user.is_admin or current_user.id == user_id):
        return redirect(url_for('user.view_user', user_id=user_id))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        is_admin = bool(request.form.get('is_admin')) if current_user.is_admin else None
        
        updated_user = user_controller.update_user(user_id, username, email, is_admin)
        if updated_user:
            return redirect(url_for('user.view_user', user_id=user_id))
    
    return render_template('user_form.html', action='edit', user=user)

@user_bp.route('/<int:user_id>/password', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    """Change user password"""
    user = user_controller.get_user(user_id)
    if not user:
        return redirect(url_for('user.list_users'))
    
    # Only admins or the user themselves can change password
    if not (current_user.is_admin or current_user.id == user_id):
        return redirect(url_for('user.view_user', user_id=user_id))
    
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if user_controller.update_password(user_id, current_password, new_password, confirm_password):
            return redirect(url_for('user.view_user', user_id=user_id))
    
    return render_template('user_password.html', user=user)

@user_bp.route('/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete user (admin only)"""
    if user_controller.delete_user(user_id):
        return redirect(url_for('user.list_users'))
    
    return redirect(url_for('user.view_user', user_id=user_id))