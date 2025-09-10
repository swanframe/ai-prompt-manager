# routes/prompt_response_routes.py
from flask import Blueprint, request, jsonify
from flask_login import login_required
from controllers.prompt_response_controller import PromptResponseController

resp_bp = Blueprint('prompt_response', __name__, url_prefix='/responses')
controller = PromptResponseController()

@resp_bp.route('/project/<int:project_id>/prompt/<int:prompt_id>', methods=['GET'])
@login_required
def list_responses(project_id, prompt_id):
    resps = controller.get_prompt_responses(project_id, prompt_id)
    return jsonify([
        {
            'id': r.id,
            'role': r.role,
            'content': r.content,
            'metadata': r.extra_metadata,           # use extra_metadata here
            'created_at': r.created_at.isoformat()
        } for r in resps
    ])

@resp_bp.route('/project/<int:project_id>/prompt/<int:prompt_id>', methods=['POST'])
@login_required
def create_response(project_id, prompt_id):
    data = request.get_json() or {}
    role = data.get('role', 'assistant')
    content = data.get('content', '')
    extra = data.get('metadata') if 'metadata' in data else data.get('extra_metadata')
    resp = controller.add_response(project_id, prompt_id, role, content, extra)  # controller maps to extra_metadata
    if not resp:
        return jsonify({'error': 'Failed to save'}), 400
    return jsonify({'id': resp.id, 'created_at': resp.created_at.isoformat()})