# ePaisa

This is a working Flask project structure built for a payment-style app. The repository is organized so a developer can see how the project connects from configuration and routes to templates, static assets, and controllers.

## Project structure

- `run.py` - Application entry point. Starts the Flask app.
- `config.py` - App configuration settings such as secret key and database URI.
- `requirements.txt` - Python dependencies needed to run the app.
- `.gitignore` - Files and folders that should not be stored in Git.
- `app/` - Main Flask package:
  - `app/__init__.py` - Flask application factory and setup.
  - `app/extensions.py` - Shared Flask extensions (SQLAlchemy, etc.).
  - `app/routes/` - Route blueprints for each section of the app.
  - `app/controllers/` - Controller functions that render templates.
  - `app/errors/` - Error handlers and custom exception definitions.
  - `app/forms/` - Simple request form objects.
  - `app/models/` - Database model classes.
  - `app/services/` - Business logic helper services.
  - `app/middlewares/` - Request middleware helpers.
  - `app/templates/` - HTML templates for each page.
  - `app/static/css/` - CSS files named by page or section.
  - `app/static/js/` - JavaScript files named by page or section.

## Project flow

1. A user opens `run.py` to start the Flask application.
2. `run.py` imports `create_app()` from `app/__init__.py`.
3. `app/__init__.py` creates the Flask app and loads configuration from `config.py`.
4. The app initializes extensions like SQLAlchemy and registers blueprints from `app/routes/`.
5. Each blueprint points to a controller in `app/controllers/`.
6. Controllers render HTML templates inside `app/templates/`.
7. Templates extend `base.html` and load section-specific CSS and JS from `app/static/`.
8. Error handlers in `app/errors/` render friendly error pages if something goes wrong.

## How to run the app

Activate the virtual environment and install dependencies, then run the server:

```powershell
cd C:\Users\Admin\Desktop\ePaisa
.\venv\Scripts\Activate
python -m pip install -r requirements.txt
python run.py
```

Open the app at:

```text
http://127.0.0.1:5000
```

## Notes for contributors

- Keep the app package organized by feature area.
- Add new route blueprints in `app/routes/` and register them in `app/routes/__init__.py`.
- Add corresponding controller functions in `app/controllers/`.
- Add matching templates in `app/templates/` and static assets in `app/static/css/` or `app/static/js/`.
