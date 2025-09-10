from flask import flash
from flask_login import current_user
from core.base_controller import BaseController
from models.prompt import Prompt
from models.attachment import Attachment
from config import Config

ALLOWED_TEXT_MIME = {'text/plain', 'text/markdown', 'application/json'}

class AttachmentController(BaseController):
    model_class = Attachment

    def _get_user_prompt(self, project_id, prompt_id):
        prompt = Prompt.get_project_prompt(project_id, prompt_id)
        if not prompt or prompt.project.user_id != current_user.id:
            return None
        return prompt

    def list_for_prompt(self, project_id, prompt_id):
        prompt = self._get_user_prompt(project_id, prompt_id)
        if not prompt:
            return []
        return Attachment.query.filter_by(prompt_id=prompt_id)\
               .order_by(Attachment.created_at).all()

    def create_attachment(self, project_id, prompt_id, filename, content, mime_type='text/plain'):
        prompt = self._get_user_prompt(project_id, prompt_id)
        if not prompt:
            flash('Prompt not found or permission denied', 'error')
            return None

        if not filename or len(filename.strip()) == 0:
            flash('Filename is required', 'error'); return None

        mime = (mime_type or 'text/plain').strip()
        if not (mime.startswith('text/') or mime in {'application/json'}):
            flash('Only text attachments are allowed', 'error'); return None

        if not content or len(content) == 0:
            flash('Attachment content is required', 'error'); return None

        if hasattr(Config, 'MAX_ATTACHMENT_SIZE') and len(content.encode('utf-8')) > Config.MAX_ATTACHMENT_SIZE:
            flash('Attachment too large', 'error'); return None

        # optional: cap number of attachments per prompt
        if hasattr(Config, 'MAX_ATTACHMENTS_PER_PROMPT'):
            count = Attachment.query.filter_by(prompt_id=prompt_id).count()
            if count >= Config.MAX_ATTACHMENTS_PER_PROMPT:
                flash('Attachment limit reached for this prompt', 'error'); return None

        data = {
            'prompt_id': prompt_id,
            'filename': filename.strip()[:255],
            'mime_type': mime,
            'content': content
        }
        att = self.create(data)
        if att: flash('Attachment created', 'success')
        return att

    def update_attachment(self, project_id, prompt_id, attachment_id, filename, content, mime_type='text/plain'):
        prompt = self._get_user_prompt(project_id, prompt_id)
        att = Attachment.get_by_id(attachment_id)
        if not prompt or not att or att.prompt_id != prompt.id:
            flash('Attachment not found or permission denied', 'error')
            return None
        return self.create_attachment(project_id, prompt_id, filename, content, mime_type) \
            if False else self.update(attachment_id, {
                'filename': filename.strip()[:255],
                'mime_type': (mime_type or 'text/plain').strip(),
                'content': content
            })

    def delete_attachment(self, project_id, prompt_id, attachment_id):
        prompt = self._get_user_prompt(project_id, prompt_id)
        att = Attachment.get_by_id(attachment_id)
        if not prompt or not att or att.prompt_id != prompt.id:
            flash('Attachment not found or permission denied', 'error')
            return False
        return self.delete(attachment_id)