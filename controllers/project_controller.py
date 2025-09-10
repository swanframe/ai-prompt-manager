from flask import flash, redirect, url_for
from flask_login import current_user
from core.base_controller import BaseController
from models.project import Project
from models.prompt import Prompt

class ProjectController(BaseController):
    """Controller for project management"""
    
    model_class = Project
    
    def get_user_projects(self):
        """Get all projects for current user"""
        if not current_user.is_authenticated:
            return []
        
        return Project.get_by_user(current_user.id)
    
    def get_user_project(self, project_id):
        """Get specific project belonging to current user"""
        if not current_user.is_authenticated:
            return None
        
        return Project.get_user_project(current_user.id, project_id)
    
    def create_project(self, name, description=None):
        """Create new project for current user"""
        if not current_user.is_authenticated:
            flash('Please log in to create projects', 'error')
            return None
        
        # Validation
        if not name or len(name.strip()) < 1:
            flash('Project name is required', 'error')
            return None
        
        if len(name.strip()) > 100:
            flash('Project name must be less than 100 characters', 'error')
            return None
        
        # Create project
        data = {
            'user_id': current_user.id,
            'name': name.strip(),
            'description': description.strip() if description else None
        }
        
        project = self.create(data)
        if project:
            flash(f'Project "{project.name}" created successfully!', 'success')
        
        return project
    
    def update_project(self, project_id, name, description=None):
        """Update existing project"""
        project = self.get_user_project(project_id)
        
        if not project:
            flash('Project not found', 'error')
            return None
        
        # Validation
        if not name or len(name.strip()) < 1:
            flash('Project name is required', 'error')
            return None
        
        if len(name.strip()) > 100:
            flash('Project name must be less than 100 characters', 'error')
            return None
        
        # Update project
        data = {
            'name': name.strip(),
            'description': description.strip() if description else None
        }
        
        updated_project = self.update(project_id, data)
        if updated_project:
            flash(f'Project "{updated_project.name}" updated successfully!', 'success')
        
        return updated_project
    
    def delete_project(self, project_id):
        """Delete project and all its prompts"""
        project = self.get_user_project(project_id)
        
        if not project:
            flash('Project not found', 'error')
            return False
        
        project_name = project.name
        
        if self.delete(project_id):
            flash(f'Project "{project_name}" deleted successfully!', 'success')
            return True
        
        return False
    
    def get_dashboard_data(self):
        """Get dashboard data for current user"""
        if not current_user.is_authenticated:
            return None
        
        projects = self.get_user_projects()
        
        # Calculate statistics
        total_projects = len(projects)
        total_prompts = sum(project.get_prompts_count() for project in projects)
        
        # Get recent projects (last 5)
        recent_projects = projects[:5]
        
        return {
            'total_projects': total_projects,
            'total_prompts': total_prompts,
            'recent_projects': recent_projects,
            'all_projects': projects
        }