# Notes Project

A full-stack notes application with React frontend and Flask backend, featuring user authentication and note management capabilities.

## Project Overview

This is a complete notes application that allows users to:
- **Authentication**: Register, login, and logout with JWT token-based authentication
- **Note Management**: Create, read, update, and delete personal notes
- **User Isolation**: Each user can only access their own notes
- **Real-time Updates**: Notes are immediately reflected in the UI after changes

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
- **CORS**: Enabled for frontend-backend communication

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

## Features

### Authentication System
- User registration and login
- JWT token-based authentication with 24-hour expiration
- Token validation and revocation
- Protected routes requiring authentication

### Notes Management
- Create new notes with title and content
- View all user's notes
- Edit existing notes
- Delete notes
- Automatic timestamps for creation and updates

### Security Features
- Password-based authentication
- JWT token storage and validation
- User-specific data isolation
- CORS protection for API endpoints

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

4. Set up environment variables (optional):
```bash
# Create a .env file in the server directory
SECRET_KEY=your-secret-key-change-this
SQLALCHEMY_DATABASE_URI=sqlite:///users.db
SQLALCHEMY_TRACK_MODIFICATIONS=False
```

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

Since the application doesn't include a registration endpoint, users must be added manually to the database. Here are several methods:

### Method 1: Using Python Shell

1. Navigate to the server directory and activate your virtual environment
2. Start Python shell:
```bash
python
```

3. Add a user programmatically:
```python
from app import app, db
from models.user import User

with app.app_context():
    # Create database tables
    db.create_all()
    
    # Create a new user
    new_user = User(
        email='user@example.com',
        password='password123'
    )
    
    # Add to database
    db.session.add(new_user)
    db.session.commit()
    
    print(f"User created: {new_user.email}")
```

### Method 2: Using SQLite Browser

1. Install a SQLite browser (like DB Browser for SQLite)
2. Open the database file: `server/instance/users.db`
3. Navigate to the "Browse Data" tab
4. Select the "users" table
5. Click "New Record" and add:
   - `email`: user's email address
   - `password`: user's password (plain text)
   - `token`: leave NULL
   - `token_expires_at`: leave NULL

### Method 3: Direct SQL Commands

1. Navigate to the server directory
2. Open SQLite shell:
```bash
sqlite3 instance/users.db
```

3. Insert a user:
```sql
INSERT INTO users (email, password) VALUES ('user@example.com', 'password123');
```

4. Verify the user was added:
```sql
SELECT * FROM users;
```

5. Exit SQLite:
```sql
.quit
```

### Method 4: Create a Management Script

Create a file `server/create_user.py`:

```python
from app import app, db
from models.user import User

def create_user(email, password):
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"User {email} already exists!")
            return
        
        # Create new user
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        print(f"User {email} created successfully!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python create_user.py <email> <password>")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2]
    create_user(email, password)
```

Then run:
```bash
python create_user.py user@example.com password123
```

## Database Schema

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

## Security Notes

⚠️ **Important Security Considerations:**

1. **Password Storage**: Passwords are currently stored as plain text. In production, use password hashing (bcrypt, Argon2, etc.)
2. **Secret Key**: Change the default secret key in production
3. **HTTPS**: Use HTTPS in production for secure communication
4. **Input Validation**: Add proper input validation and sanitization
5. **Rate Limiting**: Implement rate limiting for authentication endpoints

## Development

### Adding New Features
- Backend: Add new routes in `server/app.py`
- Frontend: Create new components in `client/src/components/`
- Database: Create new models in `server/models/`

### Testing
- Backend: Use tools like Postman or curl to test API endpoints
- Frontend: Run `npm test` in the client directory

## Troubleshooting

### Common Issues

1. **Database not found**: Run the Python shell method to create tables
2. **CORS errors**: Ensure the backend is running on port 3001
3. **Authentication fails**: Check that users exist in the database
4. **Port conflicts**: Change ports in the respective configuration files

### Logs
- Backend logs appear in the terminal where `python app.py` is running
- Frontend logs appear in the browser console and terminal

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License. 