# Kanmind Backend

A RESTful backend API for a Kanban-style task management application. Built with Django and Django REST Framework, it supports user authentication, board management, task tracking, and comments.

## Tech Stack

- **Python** / **Django 6**
- **Django REST Framework** — REST API
- **Token Authentication** — stateless auth via DRF tokens
- **SQLite** — default development database

## Project Structure

```
kanmind/
├── core/           # Django project config, settings, root URLs
├── auth_app/       # Registration & login endpoints
├── boards_app/     # Board management endpoints
├── tasks_app/      # Task & comment endpoints
├── manage.py
└── requirements.txt
```

## Setup & Installation

### Prerequisites

- Python 3.12+

### Steps

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd kanmind
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv env
   source env/bin/activate      # macOS / Linux
   env\Scripts\activate         # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Start the development server**

   ```bash
   python manage.py runserver
   ```

   The API is now available at `http://127.0.0.1:8000/`.

---

## API Endpoints

All endpoints are prefixed with `/api/`.

### Auth

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| POST | `/api/registration/` | Register a new user | No |
| POST | `/api/login/` | Log in and receive a token | No |

**Registration request body:**
```json
{
  "username": "Jane Doe",
  "email": "jane@example.com",
  "password": "yourpassword"
}
```

**Login request body:**
```json
{
  "email": "jane@example.com",
  "password": "yourpassword"
}
```

Both return a token and basic user info:
```json
{
  "token": "abc123...",
  "fullname": "Jane Doe",
  "email": "jane@example.com",
  "user_id": 1
}
```

---

### Boards

All board endpoints require a token in the `Authorization` header:
```
Authorization: Token <your-token>
```

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/boards/` | List all boards the user is a member of |
| POST | `/api/boards/` | Create a new board |
| GET | `/api/boards/<id>/` | Retrieve a single board |
| PATCH | `/api/boards/<id>/` | Update a board |
| DELETE | `/api/boards/<id>/` | Delete a board |
| GET | `/api/email-check/` | Check if a user with a given email exists |

---

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tasks/` | Create a new task |
| GET | `/api/tasks/<id>/` | Retrieve a single task |
| PATCH | `/api/tasks/<id>/` | Update a task |
| DELETE | `/api/tasks/<id>/` | Delete a task |
| GET | `/api/tasks/assigned-to-me/` | List tasks assigned to the current user |
| GET | `/api/tasks/reviewing/` | List tasks where the current user is the reviewer |

**Task fields:**

| Field | Type | Values |
|-------|------|--------|
| `title` | string | — |
| `description` | string | optional |
| `status` | string | `to-do`, `in-progress`, `review`, `done` |
| `priority` | string | `low`, `medium`, `high` |
| `assignee` | int (user ID) | optional |
| `reviewer` | int (user ID) | optional |
| `due_date` | date (`YYYY-MM-DD`) | — |
| `board` | int (board ID) | — |

---

### Comments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/<id>/comments/` | List all comments on a task |
| POST | `/api/tasks/<id>/comments/` | Add a comment to a task |
| DELETE | `/api/tasks/<task_id>/comments/<comment_id>/` | Delete a comment |

---

## Authentication

This API uses **token-based authentication**. After registering or logging in, include the token in every request:

```
Authorization: Token <your-token>
```

---

## Development Notes

- `DEBUG = True` and `SECRET_KEY` are hardcoded for development. Do not use these values in production.
- The database is SQLite (`db.sqlite3`) by default — sufficient for local development.
- To access the Django admin panel: create a superuser with `python manage.py createsuperuser`, then visit `http://127.0.0.1:8000/admin/`.
