# Notes Project

A full-stack notes application with React frontend and Flask backend, featuring user authentication and note management capabilities.

## Project Overview

This is a complete notes application that allows users to:
- **Authentication**: Register, login, and logout with JWT token-based authentication
- **Note Management**: Create, read, update, and delete personal notes

## Screenshots

### Login Page
![Login Page](screenshots/Screen%20Shot%202025-06-22%20at%2011.22.30%20PM.png)

### Notes List
![Notes List](screenshots/Screen%20Shot%202025-06-22%20at%2011.23.05%20PM.png)

### Create/Edit Note
![Create/Edit Note](screenshots/Screen%20Shot%202025-06-22%20at%2011.23.28%20PM.png)

## Architecture

- **Frontend**: React with TypeScript, using React Router for navigation
- **Backend**: Flask REST API with SQLAlchemy ORM
- **Database**: SQLite (default) with support for other databases
- **Authentication**: JWT tokens with 24-hour expiration

## Project Structure

```
notes_project/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API service functions
│   │   ├── types/          # TypeScript type definitions
│   │   └── App.tsx         # Main application component
│   ├── package.json        # Frontend dependencies
│   └── README.md           # Frontend-specific documentation
├── server/                 # Flask backend
│   ├── app.py              # Main Flask application
│   ├── models/             # Database models
│   │   ├── user.py         # User model with authentication
│   │   └── note.py         # Note model
│   ├── requirements.txt    # Python dependencies
│   └── instance/           # Database files (auto-generated)
└── README.md               # This file
```


## Setup Instructions

### Prerequisites
- Node.js (v14 or higher)
- Python (v3.7 or higher)
- pip (Python package manager)

### Backend Setup

1. Navigate to the server directory:
```bash
cd server
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Update the .env file with your local database credentials

5. Run the Flask server:
```bash
python app.py
```

The backend will start on `http://localhost:3001`

### Frontend Setup

1. Navigate to the client directory:
```bash
cd client
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will start on `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /logout` - User logout (requires token)
- `GET /` - Home route with token validation

### Notes Management
- `GET /notes` - Get all notes for authenticated user
- `POST /notes` - Create a new note
- `PUT /notes/<id>` - Update an existing note
- `DELETE /notes/<id>` - Delete a note

## Manual User Database Management

Since the application doesn't include a registration endpoint, users must be added manually to the database.


### Users Table
- `id` (Integer, Primary Key) - Unique user identifier
- `email` (String, Unique) - User's email address
- `password` (String) - User's password (stored as plain text)
- `token` (String, Nullable) - Current JWT token
- `token_expires_at` (DateTime, Nullable) - Token expiration time

### Notes Table
- `id` (Integer, Primary Key) - Unique note identifier
- `title` (String) - Note title
- `content` (Text) - Note content
- `user_id` (Integer, Foreign Key) - Reference to user who owns the note
- `created_at` (DateTime) - Note creation timestamp
- `updated_at` (DateTime) - Note last update timestamp



