from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from controllers.project_controller import ProjectController
from controllers.prompt_controller import PromptController

# Create blueprint
project_bp = Blueprint('project', __name__, url_prefix='/projects')

# Initialize controllers
project_controller = ProjectController()
prompt_controller = PromptController()

@project_bp.route('/')
@login_required
def dashboard():
    """Main dashboard showing user's projects and statistics"""
    dashboard_data = project_controller.get_dashboard_data()
    return render_template('dashboard.html', data=dashboard_data)

@project_bp.route('/list')
@login_required
def list_projects():
    """List all user projects"""
    projects = project_controller.get_user_projects()
    return render_template('projects.html', projects=projects)

@project_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    """Create new project"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        project = project_controller.create_project(name, description)
        if project:
            return redirect(url_for('project.view_project', project_id=project.id))
    
    return render_template('project_form.html', action='create')

@project_bp.route('/<int:project_id>')
@login_required
def view_project(project_id):
    """View specific project and its prompts"""
    project = project_controller.get_user_project(project_id)
    if not project:
        return redirect(url_for('project.dashboard'))
    
    prompts = prompt_controller.get_project_prompts(project_id)
    
    return render_template('project_detail.html', 
                         project=project, 
                         prompts=prompts)

@project_bp.route('/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """Edit existing project"""
    project = project_controller.get_user_project(project_id)
    if not project:
        return redirect(url_for('project.dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        updated_project = project_controller.update_project(project_id, name, description)
        if updated_project:
            return redirect(url_for('project.view_project', project_id=project_id))
    
    return render_template('project_form.html', 
                         action='edit', 
                         project=project)

@project_bp.route('/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    """Delete project"""
    if project_controller.delete_project(project_id):
        return redirect(url_for('project.dashboard'))
    
    return redirect(url_for('project.view_project', project_id=project_id))

@project_bp.route('/search')
@login_required
def search():
    """Search across all user's prompts"""
    search_term = request.args.get('q', '').strip()
    results = []
    
    if search_term:
        results = prompt_controller.search_prompts(search_term)
    
    return render_template('search_results.html', 
                         results=results, 
                         search_term=search_term)

# API endpoints for AJAX requests
@project_bp.route('/api/<int:project_id>/stats')
@login_required
def api_project_stats(project_id):
    """Get project statistics as JSON"""
    project = project_controller.get_user_project(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    
    return jsonify({
        'id': project.id,
        'name': project.name,
        'prompts_count': project.get_prompts_count(),
        'created_at': project.created_at.isoformat()
    })