from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required
from controllers.prompt_controller import PromptController
from controllers.project_controller import ProjectController

# Create blueprint
prompt_bp = Blueprint('prompt', __name__, url_prefix='/prompts')

# Initialize controllers
prompt_controller = PromptController()
project_controller = ProjectController()

@prompt_bp.route('/project/<int:project_id>')
@login_required
def list_prompts(project_id):
    """List all prompts in a project"""
    project = project_controller.get_user_project(project_id)
    if not project:
        return redirect(url_for('project.dashboard'))
    
    prompts = prompt_controller.get_project_prompts(project_id)
    return render_template('prompts.html', 
                         project=project, 
                         prompts=prompts)

@prompt_bp.route('/project/<int:project_id>/create', methods=['GET', 'POST'])
@login_required
def create_prompt(project_id):
    """Create new prompt in project"""
    project = project_controller.get_user_project(project_id)
    if not project:
        return redirect(url_for('project.dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        prompt = prompt_controller.create_prompt(project_id, title, content)
        if prompt:
            return redirect(url_for('prompt.view_prompt', 
                                  project_id=project_id, 
                                  prompt_id=prompt.id))
    
    return render_template('prompt_form.html', 
                         action='create', 
                         project=project)

@prompt_bp.route('/project/<int:project_id>/<int:prompt_id>')
@login_required
def view_prompt(project_id, prompt_id):
    """View specific prompt"""
    prompt = prompt_controller.get_user_prompt(project_id, prompt_id)
    if not prompt:
        return redirect(url_for('project.view_project', project_id=project_id))
    
    project = project_controller.get_user_project(project_id)
    
    return render_template('prompt_detail.html', 
                         project=project, 
                         prompt=prompt)

@prompt_bp.route('/project/<int:project_id>/<int:prompt_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_prompt(project_id, prompt_id):
    """Edit existing prompt"""
    prompt = prompt_controller.get_user_prompt(project_id, prompt_id)
    if not prompt:
        return redirect(url_for('project.view_project', project_id=project_id))
    
    project = project_controller.get_user_project(project_id)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        
        updated_prompt = prompt_controller.update_prompt(project_id, prompt_id, title, content)
        if updated_prompt:
            return redirect(url_for('prompt.view_prompt', 
                                  project_id=project_id, 
                                  prompt_id=prompt_id))
    
    return render_template('prompt_form.html', 
                         action='edit', 
                         project=project, 
                         prompt=prompt)

@prompt_bp.route('/project/<int:project_id>/<int:prompt_id>/delete', methods=['POST'])
@login_required
def delete_prompt(project_id, prompt_id):
    """Delete prompt"""
    if prompt_controller.delete_prompt(project_id, prompt_id):
        return redirect(url_for('project.view_project', project_id=project_id))
    
    return redirect(url_for('prompt.view_prompt', 
                          project_id=project_id, 
                          prompt_id=prompt_id))

@prompt_bp.route('/project/<int:project_id>/<int:prompt_id>/duplicate', methods=['POST'])
@login_required
def duplicate_prompt(project_id, prompt_id):
    """Create a duplicate of existing prompt"""
    duplicate = prompt_controller.duplicate_prompt(project_id, prompt_id)
    if duplicate:
        return redirect(url_for('prompt.view_prompt', 
                              project_id=project_id, 
                              prompt_id=duplicate.id))
    
    return redirect(url_for('prompt.view_prompt', 
                          project_id=project_id, 
                          prompt_id=prompt_id))

# API endpoints for AJAX requests
@prompt_bp.route('/api/project/<int:project_id>/<int:prompt_id>')
@login_required
def api_get_prompt(project_id, prompt_id):
    """Get prompt data as JSON"""
    prompt = prompt_controller.get_user_prompt(project_id, prompt_id)
    if not prompt:
        return jsonify({'error': 'Prompt not found'}), 404
    
    return jsonify({
        'id': prompt.id,
        'title': prompt.title,
        'content': prompt.content,
        'project_id': prompt.project_id,
        'created_at': prompt.created_at.isoformat(),
        'preview': prompt.get_content_preview(150)
    })

@prompt_bp.route('/api/project/<int:project_id>/<int:prompt_id>/update', methods=['PUT'])
@login_required
def api_update_prompt(project_id, prompt_id):
    """Update prompt via API"""
    data = request.get_json()
    
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    updated_prompt = prompt_controller.update_prompt(
        project_id, 
        prompt_id, 
        data['title'], 
        data['content']
    )
    
    if updated_prompt:
        return jsonify({
            'success': True,
            'prompt': {
                'id': updated_prompt.id,
                'title': updated_prompt.title,
                'content': updated_prompt.content,
                'preview': updated_prompt.get_content_preview(150)
            }
        })
    
    return jsonify({'error': 'Failed to update prompt'}), 400

@prompt_bp.route('/api/search')
@login_required
def api_search_prompts():
    """Search prompts via API"""
    search_term = request.args.get('q', '').strip()
    
    if not search_term:
        return jsonify({'results': []})
    
    results = prompt_controller.search_prompts(search_term)
    
    return jsonify({
        'results': [
            {
                'id': prompt.id,
                'title': prompt.title,
                'preview': prompt.get_content_preview(100),
                'project_id': prompt.project_id,
                'project_name': prompt.project.name,
                'created_at': prompt.created_at.isoformat()
            }
            for prompt in results
        ],
        'count': len(results)
    })