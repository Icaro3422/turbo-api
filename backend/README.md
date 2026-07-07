# Turbo Note Taker API

A Django REST API for a personal note-taking application with JWT authentication.

## Setup

```bash
cd backend
pipenv install
cp .env.docker.example .env
# Edit .env with your database credentials
python manage.py migrate
python manage.py runserver
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login and get tokens |
| POST | `/api/auth/refresh/` | Refresh access token |

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories/` | List all categories |
| GET | `/api/categories/{id}/` | Get category details |

### Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notes/` | List notes (paginated) |
| POST | `/api/notes/` | Create note |
| GET | `/api/notes/{id}/` | Get note details |
| PUT | `/api/notes/{id}/` | Update note |
| DELETE | `/api/notes/{id}/` | Delete note |

## Authentication

All note endpoints require JWT authentication. Include the access token in the Authorization header:

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

## Development

```bash
# Run tests
python manage.py test

# Run server
python manage.py runserver
```

## API Documentation

Interactive API documentation available at:
- `/api/` - API root with endpoint overview
- `/api/schema/` - OpenAPI schema
