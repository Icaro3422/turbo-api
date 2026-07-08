# Turbo Note Taker API

A RESTful API backend for organizing personal notes with color-coded categories, built with Django REST Framework and PostgreSQL.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Django 5.x |
| API | Django REST Framework 3.14 |
| Database | PostgreSQL |
| Auth | JWT (SimpleJWT) |
| Filtering | django-filter |
| CORS | django-cors-headers |
| Env Mgmt | python-dotenv |
| DB URL | dj-database-url |
| Python | 3.13 |
| Deps Mgmt | pipenv |

## Data Model

```
┌─────────────────────┐       ┌─────────────────────┐
│      CustomUser     │       │      Category       │
├─────────────────────┤       ├─────────────────────┤
│ id         (PK)     │       │ id         (PK)     │
│ email      (unique) │       │ title      (str)    │
│ password   (hashed) │       │ color      (hex)    │
│ is_active  (bool)   │       └──────────┬──────────┘
│ is_staff   (bool)   │                  │
│ created_at (auto)   │                  │ 1:N
└──────────┬──────────┘                  │
           │                             │
           │ 1:N                         │
           │                             │
           ▼                             ▼
       ┌─────────────────────────────────────┐
       │               Note                  │
       ├─────────────────────────────────────┤
       │ id            (PK)                  │
       │ title         (str, max 200)        │
       │ description   (text, optional)      │
       │ last_update   (auto)                │
       │ category_id   (FK → Category)       │
       │ user_id       (FK → CustomUser)     │
       └─────────────────────────────────────┘
```

### Predefined Categories

| Title | Color |
|-------|-------|
| Random Thoughts | `#EF9C66` |
| School | `#FCDC94` |
| Personal | `#78ABA8` |

Seeded automatically via migration `0002_seed_categories`.

## API Endpoints

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/register/` | No | Create account (email + password) |
| POST | `/api/auth/login/` | No | Login, returns JWT access + refresh tokens |
| POST | `/api/auth/refresh/` | No | Refresh expired access token |

### Notes

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/notes/` | Yes | List user's notes (paginated, filterable) |
| POST | `/api/notes/` | Yes | Create a note |
| GET | `/api/notes/{id}/` | Yes | Retrieve a note |
| PUT | `/api/notes/{id}/` | Yes | Update a note |
| DELETE | `/api/notes/{id}/` | Yes | Delete a note |

**Query params:** `?category=<id>` to filter by category.

### Categories

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/categories/` | No | List all categories with note count |
| GET | `/api/categories/{id}/` | No | Retrieve a category |

### Other

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/` | API root with endpoint listing |
| GET | `/api/schema/` | OpenAPI schema |
| GET | `/admin/` | Django admin |

## Environment Variables

Create a `.env` file in this directory:

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# PostgreSQL
POSTGRES_DB=turbo_notes
POSTGRES_USER=turbo_user
POSTGRES_PASSWORD=your-password-here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### Vercel Deployment Variables

When deploying to Vercel, set these in the Vercel dashboard under **Settings > Environment Variables**:

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.vercel.app
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

> **Note:** For Vercel, you need a managed PostgreSQL provider (Neon, Supabase, Railway, etc.) since Vercel doesn't host databases. Replace the individual `POSTGRES_*` vars with a single `DATABASE_URL` in production.

## Setup

### Option A: Docker (Recommended)

Docker handles PostgreSQL and all dependencies automatically.

**Prerequisites:** Docker + Docker Compose

```bash
# Start containers (PostgreSQL + API)
docker compose up --build

# In a new terminal, run migrations
docker compose exec api pipenv run python manage.py migrate

# Create superuser (optional)
docker compose exec api pipenv run python manage.py createsuperuser
```

API available at `http://localhost:8000/api/`

**Useful commands:**

```bash
# Run tests
docker compose exec api pipenv run python manage.py test

# Access Django shell
docker compose exec api pipenv run python manage.py shell

# View logs
docker compose logs -f api

# Stop containers
docker compose down

# Stop and wipe database
docker compose down -v
```

### Option B: Local (Manual)

**Prerequisites:** Python 3.13+, PostgreSQL, pipenv

```bash
# Install dependencies
pipenv install

# Create .env from example
cp .env.docker.example .env
# Edit .env with your local PostgreSQL credentials

# Run migrations
pipenv run python manage.py migrate

# Create superuser (optional)
pipenv run python manage.py createsuperuser

# Start dev server
pipenv run python manage.py runserver
```

API available at `http://localhost:8000/api/`

### Running Tests

```bash
# Docker
docker compose exec api pipenv run python manage.py test

# Local
pipenv run python manage.py test
```

## Project Structure

```
├── README.md
├── Pipfile                    # Dependencies
├── Pipfile.lock               # Locked dependencies
├── manage.py                  # Django CLI
├── Dockerfile                 # Container image
├── docker-compose.yml         # Local dev services
├── vercel.json                # Vercel deployment config
├── requirements.txt           # Pip deps (for Vercel)
├── .env                       # Environment vars (git-ignored)
├── .env.docker.example        # Docker env template
├── .env.docker                # Docker-specific env
├── turbo_base/                # Django project config
│   ├── __init__.py
│   ├── settings.py            # Main settings
│   ├── urls.py                # Root URL routing
│   ├── wsgi.py                # WSGI entry point
│   └── asgi.py                # ASGI entry point
└── note_taker/                # Main app
    ├── __init__.py
    ├── apps.py
    ├── models.py              # CustomUser, Category, Note
    ├── serializers.py         # DRF serializers
    ├── views.py               # API views + viewsets
    ├── urls.py                # App URL routing
    ├── admin.py               # Admin registration
    ├── pagination.py          # Page size config
    ├── migrations/            # DB migrations
    └── tests/                 # Test suite
        ├── __init__.py
        ├── test_models.py
        ├── test_auth.py
        ├── test_categories.py
        └── test_notes.py
```

## Deployment

### GitHub

1. Create a new repository on GitHub
2. Push the code:
   ```bash
   git remote add origin <github-repo-url>
   git push -u origin main
   ```

## JWT Authentication

- **Access token lifetime:** 60 minutes
- **Refresh token lifetime:** 7 days
- **Token type:** Bearer

Include the access token in requests:
```
Authorization: Bearer <access_token>
```

## API Usage Examples

### Register

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepassword123"}'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepassword123"}'
```

### Create Note

```bash
curl -X POST http://localhost:8000/api/notes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"title":"My Note","description":"Note content","category_id":1}'
```

### List Notes

```bash
curl http://localhost:8000/api/notes/ \
  -H "Authorization: Bearer <access_token>"
```

### Filter by Category

```bash
curl "http://localhost:8000/api/notes/?category=1" \
  -H "Authorization: Bearer <access_token>"
```

## License

MIT
