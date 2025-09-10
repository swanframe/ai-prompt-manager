from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from config import Config
from core import db, init_app_extensions
import markdown  # New import

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Add Markdown filter to Jinja (new)
    app.jinja_env.filters['markdown'] = lambda text: markdown.markdown(text, extensions=['fenced_code']) if text else ''

    # Initialize extensions
    init_app_extensions(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        return User.get_by_id(int(user_id))
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.project_routes import project_bp
    from routes.prompt_routes import prompt_bp
    from routes.user_routes import user_bp
    from routes.prompt_response_routes import resp_bp
    from routes.attachment_routes import attachment_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(prompt_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(resp_bp)
    app.register_blueprint(attachment_bp)
    
    # Add route for root URL
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('project.dashboard'))
        return redirect(url_for('auth.login'))

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)