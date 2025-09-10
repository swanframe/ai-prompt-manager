-- Database schema for AI Prompt Manager
-- This file creates all necessary tables and relationships

DROP TABLE IF EXISTS prompt_responses;
DROP TABLE IF EXISTS prompts;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS attachments;

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Projects table
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_project_user
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE
);

-- Prompts table (no more `result` column)
CREATE TABLE prompts (
    id SERIAL PRIMARY KEY,
    project_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_prompt_project
        FOREIGN KEY (project_id) REFERENCES projects (id)
        ON DELETE CASCADE
);

-- Prompt Responses table (conversation history)
CREATE TABLE prompt_responses (
    id SERIAL PRIMARY KEY,
    prompt_id INT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    extra_metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_response_prompt
        FOREIGN KEY (prompt_id) REFERENCES prompts (id)
        ON DELETE CASCADE
);

CREATE TABLE attachments (
    id SERIAL PRIMARY KEY,
    prompt_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    mime_type VARCHAR(100) NOT NULL DEFAULT 'text/plain',
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_attachment_prompt
        FOREIGN KEY (prompt_id) REFERENCES prompts (id)
        ON DELETE CASCADE
);

-- Indexes for better performance
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_prompts_project_id ON prompts(project_id);
CREATE INDEX idx_prompts_created_at ON prompts(created_at);
CREATE INDEX idx_responses_prompt_id ON prompt_responses(prompt_id);
CREATE INDEX idx_responses_created_at ON prompt_responses(created_at);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_attachments_prompt_id ON attachments(prompt_id);
CREATE INDEX idx_attachments_created_at ON attachments(created_at);