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
- Make sure ports 8000 and 5432 are available on your system

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

## That's it!

Complete each task thoroughly, commit your work following the branch-and-merge structure, and make sure your README.md clearly explains how to install, run, and test everything.

Thank you!