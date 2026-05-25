# HR IT Platform — Django

A people & company management system for IT HR teams.  
Built with Django 5, PostgreSQL, Nginx, Docker Compose.

## Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Backend    | Django 5.0, Python 3.12             |
| Database   | PostgreSQL 16                       |
| Web server | Nginx 1.25 + Gunicorn               |
| Frontend   | Vanilla JS + CSS (no build step)    |
| Auth       | Django built-in auth + permissions  |
| Container  | Docker Compose                      |

## Project layout

```
hr_django/
├── apps/
│   ├── accounts/        # Custom User model, auth views
│   ├── companies/       # Company CRUD
│   ├── core/            # Dashboard, middleware, context processors
│   └── people/          # Person, Education, Work CRUD
├── hr_project/          # Django settings, root URLs, wsgi
├── nginx/               # Nginx config
├── static/
│   ├── css/
│   │   ├── base.css     # Design tokens, typography, resets
│   │   ├── layout.css   # Sidebar, topbar, main content shell
│   │   ├── components.css  # Cards, tables, badges, buttons, avatars
│   │   └── forms.css    # Form controls, validation states
│   └── js/
│       ├── sidebar.js   # Mobile toggle, active link highlighting
│       ├── ui.js        # Alerts, tabs, confirmations, tooltips
│       ├── tables.js    # Column sort, row navigation, live search
│       └── forms.js     # Image preview, dependent fields, guards
└── templates/
    ├── base/base.html   # Main layout shell
    ├── accounts/        # Login, profile, user list
    ├── companies/       # List, detail, form, delete
    ├── core/            # Dashboard
    └── people/          # List, detail, form, delete
```

## Quick start

```bash
# 1. Clone and enter the project
git clone <repo-url> Sivilio_ATS
cd Sivilio_ATS

# 2. Copy env file and adjust if needed
cp .env.example .env

# 2.a. 
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
add it to .env SECRET_KEY=

# 3. Start everything
docker compose run --rm web python manage.py makemigrations
docker compose up --build -d

# 4. Open in browser
open http://localhost

cloudflared-windows-amd64.exe tunnel --url http://localhost:8000

```

Default credentials: **admin / admin123** — change immediately after first login.

## Development (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create a local .env with DEBUG=True and a local DB URL
cp .env.example .env
# Edit .env: set DB_HOST=localhost and create a local Postgres DB

python manage.py migrate
python manage.py create_initial_data
python manage.py runserver
```

## Permissions model

The app uses Django's built-in permission system.  
Key permissions (auto-created by migrations):

| Permission                  | Description                    |
|-----------------------------|--------------------------------|
| `people.add_person`         | Create person records          |
| `people.change_person`      | Edit person records            |
| `people.delete_person`      | Delete person records          |
| `people.add_education`      | Add education entries          |
| `people.add_work`           | Add work experience entries    |
| `companies.add_company`     | Create company records         |
| `companies.change_company`  | Edit company records           |
| `companies.delete_company`  | Delete company records         |
| `accounts.view_user`        | View the users list            |
| `accounts.change_user`      | Edit user accounts             |

Assign these to Groups in Django Admin, then assign users to Groups.

## Environment variables

| Variable          | Default       | Description                    |
|-------------------|---------------|--------------------------------|
| `SECRET_KEY`      | —             | Django secret key (required)   |
| `DEBUG`           | `False`       | Enable debug mode              |
| `ALLOWED_HOSTS`   | `localhost`   | Comma-separated hostnames      |
| `POSTGRES_DB`     | `hrdb`        | Database name                  |
| `POSTGRES_USER`   | `hruser`      | Database user                  |
| `POSTGRES_PASSWORD` | `hrpassword` | Database password             |
| `DB_HOST`         | `db`          | Database host (Docker service) |
