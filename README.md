# AI Prompt Manager

AI Prompt Manager is a web-based application designed to help users organize, manage, and collaborate on AI prompts. It allows users to create projects, store prompts with associated responses (like conversation history), attach text-based files, and perform searches across their content. The app supports user authentication, role-based access (admin and standard users), and a clean dashboard for overview.

## Key Features

- **User Authentication**: Secure login, registration, and logout with password hashing.
- **Project Management**: Create, edit, delete, and view projects to organize prompts.
- **Prompt Management**: Add, update, delete, duplicate prompts within projects; includes content preview and validation.
- **Conversation History**: Store and manage responses (user, assistant, system roles) for each prompt.
- **Attachments**: Upload and manage text-based attachments (e.g., plain text, Markdown, JSON) for prompts, with size and count limits.
- **Search Functionality**: Search prompts by title or content across user-owned projects.
- **Dashboard and Statistics**: Overview of projects, prompts, and counts; admin users can manage other users.
- **Admin Tools**: Admins can create, edit, delete users and change roles.
- **Markdown Support**: Render prompt content with Markdown formatting.
- **Security**: Ownership checks, validation, and session management.

## Technologies Used

- **Languages**: Python 3
- **Frameworks**: Flask (web framework), Flask-SQLAlchemy (ORM), Flask-Login (authentication)
- **Databases**: PostgreSQL
- **Tools and Libraries**:
  - Werkzeug for security utilities
  - python-dotenv for environment variables
  - psycopg2-binary for PostgreSQL driver
  - Markdown for rendering text
  - Bootstrap (via templates) for frontend styling
  - JavaScript for client-side interactions (e.g., auto-save, counters, notifications)
- **Other**: HTML/Jinja2 templates, CSS for custom styling, localStorage for form drafts.

## Project Structure

The project follows a modular MVC-like structure for better organization:

```
ai-prompt-manager/
├── app.py                       # Main application entry point
├── config.py                    # Configuration settings (e.g., database URI)
├── create_dummy_data.py         # Script to generate sample data
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (e.g., database credentials)
├── core/                        # Core utilities
│   ├── __init__.py
│   ├── base_model.py            # Base class for database models
│   └── base_controller.py       # Base class for controllers
├── models/                      # Database models
│   ├── __init__.py
│   ├── user.py                  # User model
│   ├── project.py               # Project model
│   ├── prompt.py                # Prompt model
│   ├── prompt_response.py       # Prompt response model
│   └── attachment.py            # Attachment model
├── controllers/                 # Business logic controllers
│   ├── __init__.py
│   ├── auth_controller.py       # Authentication logic
│   ├── project_controller.py    # Project management logic
│   ├── prompt_controller.py     # Prompt management logic
│   ├── prompt_response_controller.py  # Response management logic
│   ├── user_controller.py       # User management logic
│   └── attachment_controller.py # Attachment management logic
├── routes/                      # Flask routes/blueprints
│   ├── __init__.py
│   ├── auth_routes.py           # Auth-related routes
│   ├── project_routes.py        # Project routes
│   ├── prompt_routes.py         # Prompt routes
│   ├── prompt_response_routes.py  # Response routes
│   ├── user_routes.py           # User routes
│   └── attachment_routes.py     # Attachment routes
├── templates/                   # HTML templates (Jinja2)
│   ├── base.html                # Base layout
│   ├── login.html               # Login page
│   ├── register.html            # Registration page
│   ├── dashboard.html           # User dashboard
│   ├── projects.html            # Project list
│   ├── project_detail.html      # Project details
│   ├── project_form.html        # Project form
│   ├── prompts.html             # Prompt list
│   ├── prompt_detail.html       # Prompt details
│   ├── prompt_form.html         # Prompt form
│   ├── users.html               # User list (admin)
│   ├── user_detail.html         # User details
│   ├── user_form.html           # User form
│   ├── user_password.html       # Password change form
│   ├── attachment_form.html     # Attachment form
│   └── search_results.html      # Search results
├── static/                      # Static assets
│   ├── css/
│   │   └── style.css            # Custom CSS
│   └── js/
│       └── app.js               # Custom JavaScript
└── database/
    └── schema.sql                # SQL schema for database setup
```

## Installation Guide

Follow these steps to set up the project locally. Assumptions: You have Python 3.12+ and PostgreSQL installed. If not, install them first.

1. **Clone the Repository**:
   ```
   git clone https://github.com/swanframe/ai-prompt-manager.git
   cd ai-prompt-manager
   ```

2. **Create a Virtual Environment** (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Copy the example `.env` file (or create one) and update it with your details:
     ```
     SECRET_KEY=your-super-secret-key-change-this-in-production
     FLASK_ENV=development
     DB_HOST=localhost
     DB_PORT=5432
     DB_NAME=ai_prompt_manager
     DB_USER=postgres
     DB_PASSWORD=your-database-password
     MAX_ATTACHMENT_SIZE=524288  # 512 KB (optional)
     MAX_ATTACHMENTS_PER_PROMPT=20  # Optional
     ```

5. **Set Up the Database** (see Database Setup section below).

6. **Run the Application**:
   ```
   python app.py
   ```
   The app will run at `http://localhost:5000` in debug mode.

7. **(Optional) Generate Dummy Data**:
   ```
   python create_dummy_data.py
   ```
   This creates an admin user (username: admin, password: adminpass) and a sample user (alice/alicepass) with demo content.

## Database Setup

1. **Create the PostgreSQL Database**:
   - Log in to PostgreSQL (e.g., via `psql` or pgAdmin):
     ```
     CREATE DATABASE ai_prompt_manager;
     ```

2. **Apply the Schema**:
   - Run the provided SQL script:
     ```
     psql -U postgres -d ai_prompt_manager -f database/schema.sql
     ```
     (Adjust username and database as needed.)

3. **Automatic Table Creation**:
   - The app uses SQLAlchemy to create tables if they don't exist (via `db.create_all()` in `app.py`). However, running `schema.sql` ensures indexes and constraints are set up correctly.

Note: If you encounter connection issues, verify your `.env` credentials and ensure PostgreSQL is running.

## User Manual

### Running the Application
- Start the server: `python app.py`
- Open a browser and navigate to `http://localhost:5000`
- Register a new account or log in (default admin: admin/adminpass after running dummy data).

### Usage
- **Dashboard**: View your projects, total prompts, and recent activity.
- **Projects**: Create/edit/delete projects via the dashboard. Each project contains prompts.
- **Prompts**: Within a project, add prompts with titles and content. Edit, delete, or duplicate them. Add responses (e.g., AI outputs) to build conversation history.
- **Attachments**: Add text files to prompts (limited to text/plain, text/markdown, application/json).
- **Search**: Use the search bar to find prompts by title or content.
- **Admin Features**: If logged in as admin, access `/users` to manage users (create, edit, delete, change passwords/roles).
- **Logout**: Available in the navigation bar.
- **Tips**: Use Markdown in prompt content for formatting. Attachments are stored as text in the database.

For production, configure a WSGI server (e.g., Gunicorn) and set `FLASK_ENV=production`. Secure your secret key and database credentials.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or contributions, contact the maintainer at [211110108@student.mercubuana-yogya.ac.id] or open an issue on GitHub.