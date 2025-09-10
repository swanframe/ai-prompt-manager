# create_dummy_data.py
from app import create_app
from core import db
from models.user import User
from models.project import Project
from models.prompt import Prompt
from models.prompt_response import PromptResponse

def main():
    app = create_app()
    with app.app_context():
        # ensure tables exist (SQLAlchemy models)
        db.create_all()

        # Create admin user
        if not User.get_by_username('admin'):
            admin = User.create_user('admin', 'admin@example.com', 'adminpass', is_admin=True)
            print(f'Created admin: admin / adminpass (id={admin.id})')
        else:
            print('admin already exists')

        # Create regular user
        if not User.get_by_username('alice'):
            alice = User.create_user('alice', 'alice@example.com', 'alicepass', is_admin=False)
            print(f'Created user: alice / alicepass (id={alice.id})')
        else:
            alice = User.get_by_username('alice')
            print('alice already exists')

        # Create sample project, prompt, and conversation for alice
        if alice and len(alice.projects) == 0:
            project = Project(user_id=alice.id, name='Demo Project', description='A sample project created for testing')
            project.save()

            prompt = Prompt(project_id=project.id, title='Hello prompt', content='Say hello to the world')
            prompt.save()

            # Add initial conversation
            resp = PromptResponse(
                prompt_id=prompt.id,
                role='assistant',
                content='Hello!'
            )
            resp.save()

            print('Sample project, prompt, and conversation created for alice')

        print('Done.')

if __name__ == '__main__':
    main()