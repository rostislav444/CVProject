# DTEAM - Django Developer Practical Test

Welcome! This test will help us see how you structure a Django project, work with various tools, and 
handle common tasks in web development. Follow the instructions step by step. Good luck!

## Requirements:

Follow PEP 8 and other style guidelines, use clear and concise commit messages and docstrings 
where needed, structure your project for readability and maintainability, optimize database access 
using Django's built-in methods, and provide enough details in your README.

## Version Control System

1. Create a public GitHub repository for this practical test, for example: DTEAM-django-practical-test.
2. Put the text of this test (all instructions) into README.md.
3. For each task, create a separate branch (for example, tasks/task-1, tasks/task-2, etc.).
4. When you finish each task, merge that branch back into main but do not delete the original 
task branch.

## Python Virtual Environment

1. Use pyenv to manage the Python version. Create a file named .python-version in your 
repository to store the exact Python version.
2. Use Poetry to manage and store project dependencies. This will create a pyproject.toml file.
3. Update your README.md with clear instructions on how to set up and use pyenv and Poetry for 
this project.

## Project Setup Instructions

### Setting up Python environment with pyenv

1. Install pyenv (if not already installed):
   ```bash
   # For macOS
   brew install pyenv
   
   # For Ubuntu/Debian
   curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
   ```

2. Configure your shell (add to your .bashrc, .zshrc, or equivalent):
   ```bash
   export PATH="$HOME/.pyenv/bin:$PATH"
   eval "$(pyenv init --path)"
   eval "$(pyenv init -)"
   ```

3. Install Python 3.11.4 (or choose another appropriate version):
   ```bash
   pyenv install 3.11.4
   ```

4. Navigate to the project directory and set local Python version:
   ```bash
   cd DTEAM-django-practical-test
   pyenv local 3.11.4
   ```
   This will create a `.python-version` file automatically.

### Setting up Poetry for dependency management

1. Install Poetry (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Configure Poetry to create virtual environments in the project directory:
   ```bash
   poetry config virtualenvs.in-project true
   ```

3. Initialize a new Poetry project:
   ```bash
   poetry init
   ```

4. Add Django and other dependencies:
   ```bash
   poetry add django
   poetry add djangorestframework
   ```

5. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Tasks

### Task 1: Django Fundamentals

1. Create a New Django Project
   - Name it something like CVProject.
   - Use the Python version set up in Task 2 and the latest stable Django release.
   - Use SQLite as your database for now.

2. Create an App and Model
   - Create a Django app (for example, main).
   - Define a CV model with fields like firstname, lastname, skills, projects, bio, and contacts.
   - Organize the data in a way that feels efficient and logical.

3. Load Initial Data with Fixtures
   - Create a fixture that contains at least one sample CV instance.
   - Include instructions in README.md on how to load the fixture.

4. List Page View and Template
   - Implement a view for the main page (e.g., /) to display a list of CV entries.
   - Use any CSS library to style them nicely.
   - Ensure the data is retrieved from the database efficiently.

5. Detail Page View
   - Implement a detail view (e.g., /cv/<id>/) to show all data for a single CV.
   - Style it nicely and ensure efficient data retrieval.

6. Tests
   - Add basic tests for the list and detail views.
   - Update README.md with instructions on how to run these tests.

### Task 2: PDF Generation Basics

1. Choose and install any HTML-to-PDF generating library or tool.
2. Add a 'Download PDF' button on the CV detail page that allows users to download the CV as a PDF.

### Task 3: REST API Fundamentals

1. Install Django REST Framework (DRF).
2. Create CRUD endpoints for the CV model (create, retrieve, update, delete).
3. Add tests to verify that each CRUD action works correctly.

### Task 4: Middleware & Request Logging

1. Create a RequestLog Model
   - You can put this in the existing app or a new app (e.g., audit).
   - Include fields such as timestamp, HTTP method, path, and optionally other details like query string, remote IP, or logged-in user.

2. Implement Logging Middleware
   - Write a custom Django middleware class that intercepts each incoming request.
   - Create a RequestLog record in the database with the relevant request data.
   - Keep it efficient.

3. Recent Requests Page
   - Create a view (e.g., /logs/) showing the 10 most recent logged requests, sorted by timestamp descending.
   - Include a template that loops through these entries and displays their timestamp, method, and path.

4. Test Logging
   - Ensure your tests verify the logging functionality.

### Task 5: Template Context Processors

1. Create settings_context
   - Create a context processor that injects your entire Django settings into all templates.

2. Settings Page
   - Create a view (e.g., /settings/) that displays DEBUG and other settings values made available by the context processor.

### Task 6: Docker Basics

1. Use Docker Compose to containerize your project.
2. Switch the database from SQLite to PostgreSQL in Docker Compose.
3. Store all necessary environment variables (database credentials, etc.) in a .env file.

### Task 7: Celery Basics

1. Install and configure Celery, using Redis or RabbitMQ as the broker.
2. Add a Celery worker to your Docker Compose configuration.
3. On the CV detail page, add an email input field and a 'Send PDF to Email' button to trigger a Celery task that emails the PDF.

### Task 8: OpenAI Basics

1. On the CV detail page, add a 'Translate' button and a language selector.
2. Include these languages: Cornish, Manx, Breton, Inuktitut, Kalaallisut, Romani, Occitan, Ladino, Northern Sami, Upper Sorbian, Kashubian, Zazaki, Chuvash, Livonian, Tsakonian, Saramaccan, Bislama.
3. Hook this up to an OpenAI translation API or any other translation mechanism you prefer. The idea is to translate the CV content into the selected language.

### Task 9: Deployment

Deploy this project to DigitalOcean or any other VPS. (If you do not have a DigitalOcean account, you can use this referral link to create account with $200 on balance: https://m.do.co/c/967939ea1e74)

## Loading Fixtures

To load the sample CV data from fixtures:

```bash
python manage.py loaddata apps/main/fixtures/sample_cvs.json
```

## Running Tests

To run the tests for this project:

```bash
python manage.py test apps.main.tests.CVListViewTests
python manage.py test apps.main.api.tests.CVAPITests
```

## Docker Setup (Task 6)

This project can be run using Docker and Docker Compose, which handles setting up the PostgreSQL database and Django application in isolated containers.

### Prerequisites

- Docker and Docker Compose installed on your machine
- Make sure ports 8000, 5432, 5672 (RabbitMQ) and 15672 (RabbitMQ management) are available on your system

### Running with Docker

1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

2. Access the application at http://localhost:8000

3. To run commands inside the container:
   ```bash
   docker-compose exec web python manage.py <command>
   ```

4. To run tests inside the container:
   ```bash
   docker-compose exec web python manage.py test
   ```

5. To stop the containers:
   ```bash
   docker-compose down
   ```

### Environment Variables

The project uses environment variables stored in a `.env` file for configuration. The main variables include:

- `DB_NAME`: PostgreSQL database name
- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: PostgreSQL password
- `DB_HOST`: PostgreSQL host (set to 'db' for Docker setup)
- `DB_PORT`: PostgreSQL port (default: 5432)

## Celery Setup (Task 7)

This project uses Celery for background task processing, such as sending emails with PDF attachments.

### Components

- **Celery Worker**: Processes background tasks like PDF generation and email sending
- **RabbitMQ**: Acts as the message broker between Django and Celery
- **Email Configuration**: Configured to use console backend in development

### Usage

When running with Docker Compose, the Celery worker is automatically started. To test the email functionality:

1. Visit a CV detail page
2. Click on the "Email PDF" button
3. Enter an email address in the form
4. Submit the form

The email task will be processed in the background by Celery, and you'll see the output in the console of the Celery worker container.

### Environment Variables for Celery

- `CELERY_BROKER_URL`: RabbitMQ connection string (default: amqp://user:password@rabbitmq:5672//)
- `CELERY_RESULT_BACKEND`: Celery result backend (default: rpc://)

### Environment Variables for Email

- `EMAIL_BACKEND`: Email backend class (default: console backend)
- `EMAIL_HOST`: SMTP host (e.g., smtp.gmail.com)
- `EMAIL_PORT`: SMTP port (default: 587)
- `EMAIL_USE_TLS`: Whether to use TLS (default: True)
- `EMAIL_HOST_USER`: SMTP username
- `EMAIL_HOST_PASSWORD`: SMTP password
- `DEFAULT_FROM_EMAIL`: Default sender email address

## Translation Setup (Task 8)

This project includes AI-powered translation for CV content into rare languages.

### Features

- Translation button on the CV detail page
- Language selector with 17 rare languages (Cornish, Manx, Breton, etc.)
- Support for either OpenAI or Anthropic Claude as translation providers

### Configuration

To enable translations, set up the following environment variables in your `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key (optional, will fall back to OpenAI if not provided)

### How It Works

1. The translation service extracts text content from the CV
2. Content is sent to the AI service (Anthropic Claude preferred, OpenAI as fallback)
3. The AI model translates the content to the selected language
4. Translated content is displayed in a format that preserves the original structure

### Supported Languages

The system supports translation to these languages:
- Cornish
- Manx
- Breton
- Inuktitut
- Kalaallisut
- Romani
- Occitan
- Ladino
- Northern Sami
- Upper Sorbian
- Kashubian
- Zazaki
- Chuvash
- Livonian
- Tsakonian
- Saramaccan
- Bislama

## That's it!

Complete each task thoroughly, commit your work following the branch-and-merge structure, and make sure your README.md clearly explains how to install, run, and test everything.

Thank you!