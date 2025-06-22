# Notes Application

A full-stack notes application with React TypeScript frontend and Flask Python backend, featuring user authentication and CRUD operations for notes.


## Project Structure

```
notes_project/
├── client/          # React TypeScript frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API service functions
│   │   ├── types/       # TypeScript interfaces
│   │   └── api/         # Authentication API
│   └── package.json
└── server/          # Flask Python backend
    ├── app.py       # Main Flask application
    ├── models/      # Database models
    ├── requirements.txt
    └── .env         # Environment variables
```

## Prerequisites

- **Node.js** (v14 or higher)
- **Python** (v3.8 or higher)
- **pip** (Python package manager)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd notes_project
```

### 2. Backend Setup (Flask Server)

Navigate to the server directory and set up the Python environment:

```bash
cd server

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from template if available)
# Add your database configuration and JWT secret

Edit the .env file  to include correct data for your database

### 3. Frontend Setup (React Client)

Navigate to the client directory and install dependencies:

```bash
cd ../client

# Install Node.js dependencies
npm install
```

## Running the Application

### Start the Backend Server

```bash
cd server

# Activate virtual environment (if not already activated)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Run the Flask server
python app.py
```

The backend server will start on `http://localhost:3001`

### Start the Frontend Client

Open a new terminal window and navigate to the client directory:

```bash
cd client

# Start the React development server
npm start
```

The frontend application will start on `http://localhost:3000`

## Usage

1. **Access the Application**: Open your browser and go to `http://localhost:3000`
2. **Login**: Before first time login, Manually Input user credentials in User table in databasse
3. **Manage Notes**: 
   - View all your notes on the main page
   - Click "Create Note" to add a new note
   - Click "Edit" on any note to modify it
   - Click "Delete" to remove a note
4. **Logout**: Use the logout button to sign out

## API Endpoints

### Authentication
- `POST /login` - User login
- `POST /logout` - User logout
- `GET /` - Check authentication status

### Notes
- `GET /notes` - Get all notes for authenticated user
- `POST /notes` - Create a new note
- `PUT /notes/<id>` - Update an existing note
- `DELETE /notes/<id>` - Delete a note

## Development

### Available Scripts

In the client directory:

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation)

### Backend Development

The Flask server includes:
- Automatic database table creation on startup
- JWT token management

## Troubleshooting


```

