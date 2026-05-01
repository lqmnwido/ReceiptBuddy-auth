# ReceiptBuddy Auth Service

Authentication and user management microservice.

## Responsibilities

- User registration and login
- JWT token generation and validation
- User profile management
- RBAC (role-based access control)

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/register` | No | Create new user account |
| POST | `/api/auth/login` | No | Login, returns JWT token |
| GET | `/api/auth/me` | JWT | Get current user profile |
| PUT | `/api/auth/me` | JWT | Update own profile |
| GET | `/api/auth/users` | Admin | List all users |
| GET | `/api/auth/users/{id}` | Admin | Get user by ID |
| PUT | `/api/auth/users/{id}` | Admin | Update any user |
| DELETE | `/api/auth/users/{id}` | Admin | Delete user |

## Tech Stack

- **Framework**: FastAPI (Python 3.12)
- **Database**: PostgreSQL via SQLAlchemy 2.0
- **Auth**: JWT (python-jose) + bcrypt password hashing
- **Cache**: Redis

## Quick Start

```bash
# Build
docker build -t receiptbuddy-auth .

# Run (requires PostgreSQL + Redis)
docker run -p 8001:8001 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/receiptbuddy \
  -e SECRET_KEY=your-secret \
  receiptbuddy-auth
```

Or with Docker Compose (from superproject):

```bash
docker compose up -d auth
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | — | PostgreSQL connection string |
| `SECRET_KEY` | Yes | — | JWT signing secret |
| `REDIS_URL` | No | `redis://localhost:6379` | Redis connection |
| `ALGORITHM` | No | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `1440` | Token expiry (24h) |

## Dependencies

- `receiptbuddy-common` — shared library (installed from GitHub)
- PostgreSQL 16+ — primary database
- Redis 7+ — token blacklist / caching
