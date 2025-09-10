from flask import flash, request
from flask_login import current_user
from core.base_controller import BaseController
from models.prompt import Prompt
from models.project import Project

class PromptController(BaseController):
    """Controller for prompt management"""
    
    model_class = Prompt
    
    def get_project_prompts(self, project_id):
        """Get all prompts for a specific project"""
        project = self._get_user_project(project_id)
        if not project:
            return []
        
        return Prompt.get_by_project(project_id)
    
    def get_user_prompt(self, project_id, prompt_id):
        """Get specific prompt belonging to user's project"""
        project = self._get_user_project(project_id)
        if not project:
            return None
        
        return Prompt.get_project_prompt(project_id, prompt_id)
    
    def create_prompt(self, project_id, title, content):
        """Create new prompt in project"""
        project = self._get_user_project(project_id)
        if not project:
            flash('Project not found', 'error')
            return None
        
        # Validation
        if not self._validate_prompt_data(title, content):
            return None
        
        # Create prompt (no result anymore)
        data = {
            'project_id': project_id,
            'title': title.strip(),
            'content': content.strip()
        }
        
        prompt = self.create(data)
        if prompt:
            flash(f'Prompt "{prompt.title}" created successfully!', 'success')
        
        return prompt
    
    def update_prompt(self, project_id, prompt_id, title, content):
        """Update existing prompt"""
        prompt = self.get_user_prompt(project_id, prompt_id)
        if not prompt:
            flash('Prompt not found', 'error')
            return None
        
        # Validation
        if not self._validate_prompt_data(title, content):
            return None
        
        # Update prompt (no result anymore)
        data = {
            'title': title.strip(),
            'content': content.strip()
        }
        
        updated_prompt = self.update(prompt_id, data)
        if updated_prompt:
            flash(f'Prompt "{updated_prompt.title}" updated successfully!', 'success')
        
        return updated_prompt

    def delete_prompt(self, project_id, prompt_id):
        """Delete prompt from project"""
        prompt = self.get_user_prompt(project_id, prompt_id)
        if not prompt:
            flash('Prompt not found', 'error')
            return False
        
        prompt_title = prompt.title
        
        if self.delete(prompt_id):
            flash(f'Prompt "{prompt_title}" deleted successfully!', 'success')
            return True
        
        return False
    
    def search_prompts(self, search_term):
        """Search user's prompts by title or content"""
        if not current_user.is_authenticated:
            return []
        
        if not search_term or len(search_term.strip()) < 2:
            flash('Search term must be at least 2 characters', 'error')
            return []
        
        return Prompt.search_by_user(current_user.id, search_term.strip())
    
    def duplicate_prompt(self, project_id, prompt_id, copy_responses=False):
        """Duplicate a prompt (optionally with responses)"""
        original_prompt = self.get_user_prompt(project_id, prompt_id)
        if not original_prompt:
            return None
        
        duplicate_title = f"{original_prompt.title} (Copy)"
        new_prompt = self.create_prompt(project_id, duplicate_title, original_prompt.content)
        
        if new_prompt and copy_responses:
            from controllers.prompt_response_controller import PromptResponseController
            prc = PromptResponseController()
            prc.duplicate_responses(original_prompt.id, new_prompt.id)
        
        return new_prompt
    
    def _get_user_project(self, project_id):
        """Helper to get user's project"""
        if not current_user.is_authenticated:
            return None
        
        return Project.get_user_project(current_user.id, project_id)
    
    def _validate_prompt_data(self, title, content):
        """Validate prompt form data"""
        if not title or len(title.strip()) < 1:
            flash('Prompt title is required', 'error')
            return False
        
        if len(title.strip()) > 100:
            flash('Prompt title must be less than 100 characters', 'error')
            return False
        
        if not content or len(content.strip()) < 1:
            flash('Prompt content is required', 'error')
            return False
        
        if len(content.strip()) > 10000:
            flash('Prompt content must be less than 10,000 characters', 'error')
            return False
        
        return True