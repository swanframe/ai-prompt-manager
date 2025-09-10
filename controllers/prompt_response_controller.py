from flask import flash
from flask_login import current_user
from core.base_controller import BaseController
from models.prompt_response import PromptResponse
from models.prompt import Prompt
from models.project import Project

class PromptResponseController(BaseController):
    model_class = PromptResponse

    def get_prompt_responses(self, project_id, prompt_id):
        # check ownership using prompt->project
        prompt = Prompt.get_project_prompt(project_id, prompt_id)
        if not prompt or prompt.project.user_id != current_user.id:
            return []
        return PromptResponse.query.filter_by(prompt_id=prompt_id).order_by(PromptResponse.created_at).all()

    def add_response(self, project_id, prompt_id, role, content, metadata=None):
        prompt = Prompt.get_project_prompt(project_id, prompt_id)
        if not prompt or prompt.project.user_id != current_user.id:
            flash('Prompt not found or permission denied', 'error')
            return None

        if not content or len(content.strip()) == 0:
            flash('Response content is required', 'error')
            return None

        data = {
            'prompt_id': prompt_id,
            'role': role,
            'content': content.strip(),
            'extra_metadata': metadata   # use correct field name
        }
        resp = self.create(data)

        if resp:
            flash('Response saved', 'success')
        return resp

    def duplicate_responses(self, src_prompt_id, dst_prompt_id):
        src = self.model_class.query.filter_by(prompt_id=src_prompt_id).order_by(self.model_class.created_at).all()
        copied = []
        for r in src:
            new = PromptResponse(
                prompt_id=dst_prompt_id,
                role=r.role,
                content=r.content,
                extra_metadata=r.extra_metadata
            )
            new.save()
            copied.append(new)
        return copied