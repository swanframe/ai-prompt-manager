from flask import Blueprint, render_template, request, redirect, url_for, make_response
from flask_login import login_required
from controllers.attachment_controller import AttachmentController
from controllers.project_controller import ProjectController
from controllers.prompt_controller import PromptController

attachment_bp = Blueprint('attachment', __name__, url_prefix='/attachments')
controller = AttachmentController()
project_controller = ProjectController()
prompt_controller = PromptController()

@attachment_bp.route('/project/<int:project_id>/prompt/<int:prompt_id>/create', methods=['GET','POST'])
@login_required
def create_attachment(project_id, prompt_id):
    prompt = prompt_controller.get_user_prompt(project_id, prompt_id)
    if not prompt:
        return redirect(url_for('project.view_project', project_id=project_id))
    if request.method == 'POST':
        filename = request.form.get('filename','')
        mime_type = request.form.get('mime_type','text/plain')
        content  = request.form.get('content','')
        att = controller.create_attachment(project_id, prompt_id, filename, content, mime_type)
        if att:
            return redirect(url_for('prompt.view_prompt', project_id=project_id, prompt_id=prompt_id))
    project = project_controller.get_user_project(project_id)
    return render_template('attachment_form.html', action='create', project=project, prompt=prompt)

@attachment_bp.route('/project/<int:project_id>/prompt/<int:prompt_id>/<int:attachment_id>/edit', methods=['GET','POST'])
@login_required
def edit_attachment(project_id, prompt_id, attachment_id):
    prompt = prompt_controller.get_user_prompt(project_id, prompt_id)
    if not prompt:
        return redirect(url_for('project.view_project', project_id=project_id))
    att = controller.get_by_id(attachment_id)
    if request.method == 'POST':
        filename = request.form.get('filename','')
        mime_type = request.form.get('mime_type','text/plain')
        content  = request.form.get('content','')
        updated = controller.update_attachment(project_id, prompt_id, attachment_id, filename, content, mime_type)
        if updated:
            return redirect(url_for('prompt.view_prompt', project_id=project_id, prompt_id=prompt_id))
    project = project_controller.get_user_project(project_id)
    return render_template('attachment_form.html', action='edit', project=project, prompt=prompt, attachment=att)

@attachment_bp.route('/project/<int:project_id>/prompt/<int:prompt_id>/<int:attachment_id>/delete', methods=['POST'])
@login_required
def delete_attachment(project_id, prompt_id, attachment_id):
    controller.delete_attachment(project_id, prompt_id, attachment_id)
    return redirect(url_for('prompt.view_prompt', project_id=project_id, prompt_id=prompt_id))

@attachment_bp.route('/project/<int:project_id>/prompt/<int:prompt_id>/<int:attachment_id>/download', methods=['GET'])
@login_required
def download_attachment(project_id, prompt_id, attachment_id):
    att = controller.get_by_id(attachment_id)
    # ownership is enforced indirectly by accessing the prompt in the detail page/links;
    # you can also re-check here if desired.
    resp = make_response(att.content)
    resp.headers['Content-Type'] = f"{att.mime_type}; charset=utf-8"
    resp.headers['Content-Disposition'] = f'attachment; filename="{att.filename}"'
    return resp