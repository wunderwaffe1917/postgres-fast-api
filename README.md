# FastAPI PostgreSQL Service

A FastAPI service that connects to a PostgreSQL database with permanent JWT authentication and Swagger documentation.

## Features

- FastAPI framework for high-performance API development
- PostgreSQL database integration
- Permanent JWT authentication (non-expiring tokens)
- Swagger UI documentation
- Docker deployment
- Environment variable configuration

## Prerequisites

- Docker and Docker Compose
- PostgreSQL database (remote)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/wunderwaffe1917/postgres-fast-api.git
   cd postgres-fast-api
   ```

2. Create a `.env` file in the `app` directory based on the `.env.example` file:
   ```bash
   cp app/.env.example app/.env
   ```

3. Update the `.env` file with your PostgreSQL credentials and other settings:
   ```
   # Database settings
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_HOST=your_db_host
   POSTGRES_PORT=5432
   POSTGRES_DB=your_db_name

   # JWT settings
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ```

## Running with Docker

Build and start the Docker container:

```bash
docker-compose up -d
```

The API will be available at http://localhost:8000.

## API Documentation

Swagger UI documentation is available at http://localhost:8000/docs.

## Authentication

To authenticate, use the `/api/v1/login` endpoint with your username and password. The default admin credentials are:

- Username: admin
- Password: admin

The API will return a permanent JWT token (non-expiring) that you can use for subsequent requests.

## API Endpoints

- `POST /api/v1/login` - Get permanent JWT token
- `GET /api/v1/users/me` - Get current user
- `GET /api/v1/users` - List users (admin only)
- `POST /api/v1/users` - Create user (admin only)
- `GET /api/v1/items` - List items
- `POST /api/v1/items` - Create item
- `GET /api/v1/items/{item_id}` - Get item
- `PUT /api/v1/items/{item_id}` - Update item
- `DELETE /api/v1/items/{item_id}` - Delete item