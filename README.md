# Flask Backend Server

A simple Flask backend with authentication endpoints for the React frontend.

## Features

- User registration and login
- JWT token authentication
- SQLite database
- CORS enabled for frontend integration
- Protected routes with token validation

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python app.py
```

The server will start on `http://localhost:3001`

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info (requires token)
- `POST /api/auth/logout` - Logout user (requires token)

### Health Check

- `GET /api/health` - Server health check

## Example Usage

### Register a new user:
```bash
curl -X POST http://localhost:3001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123", "name": "John Doe"}'
```

### Login:
```bash
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Get current user (with token):
```bash
curl -X GET http://localhost:3001/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Environment Variables

- `SECRET_KEY` - Secret key for JWT tokens (default: 'your-secret-key-change-this')
- `SQLALCHEMY_DATABASE_URI` - Database URI (default: SQLite)

## Database

The server uses SQLite by default. The database file (`users.db`) will be created automatically when you first run the server. 