from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import os
from functools import wraps
from dotenv import load_dotenv
from models.user import db, User
from models.note import Note

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'False')

# Initialize extensions
db.init_app(app)
CORS(app)

# Token decorator for protected routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            # Decode token to get user_id
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return jsonify({'message': 'User not found'}), 401
            
            # Validate token using the model method
            if not current_user.validate_token(token, app.config['SECRET_KEY']):
                return jsonify({'message': 'Token is invalid or expired'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# Home route with token validation
@app.route('/', methods=['GET'])
def home():
    token = None
    
    # Check for token in Authorization header
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(" ")[1]
    
    # If no token provided, redirect to login
    if not token:
        return jsonify({
            'success': False,
            'message': 'No token provided',
            'redirect': 'login',
            'authenticated': False
        }), 401
    
    try:
        # Decode token to get user_id
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = User.query.get(data['user_id'])
        
        if not current_user:
            return jsonify({
                'success': False,
                'message': 'User not found',
                'redirect': 'login',
                'authenticated': False
            }), 401
        
        # Validate token using the model method
        if not current_user.validate_token(token, app.config['SECRET_KEY']):
            return jsonify({
                'success': False,
                'message': 'Token is invalid or expired',
                'redirect': 'login',
                'authenticated': False
            }), 401
        
        # Token is valid, return user data
        return jsonify({
            'success': True,
            'message': 'Welcome to the home page',
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'email': current_user.email
            }
        })
        
    except jwt.ExpiredSignatureError:
        return jsonify({
            'success': False,
            'message': 'Token has expired',
            'redirect': 'login',
            'authenticated': False
        }), 401
    except jwt.InvalidTokenError:
        return jsonify({
            'success': False,
            'message': 'Token is invalid',
            'redirect': 'login',
            'authenticated': False
        }), 401

# Authentication endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or user.password != data['password']:
        return jsonify({'message': 'Invalid email or password'}), 401
    
    # Generate token using the model method
    token = user.generate_token(app.config['SECRET_KEY'])
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email
        }
    })

@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    # Revoke the user's token
    current_user.revoke_token()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

# Notes endpoints
@app.route('/notes', methods=['GET'])
@token_required
def get_notes(current_user):
    """GET /notes: Retrieves a list of notes for the current user"""
    try:
        notes = Note.query.filter_by(user_id=current_user.id).all()
        return jsonify({
            'success': True,
            'notes': [note.to_dict() for note in notes]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/notes', methods=['POST'])
@token_required
def create_note(current_user):
    """POST /notes: Creates a new note"""
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'message': 'Title and content are required'}), 400
    
    try:
        new_note = Note(
            title=data['title'],
            content=data['content'],
            user_id=current_user.id
        )
        
        db.session.add(new_note)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Note created successfully',
            'note': new_note.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/notes/<int:note_id>', methods=['PUT'])
@token_required
def update_note(current_user, note_id):
    """PUT /notes/{id}: Updates an existing note"""
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'message': 'Title and content are required'}), 400
    
    try:
        note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
        
        if not note:
            return jsonify({'message': 'Note not found'}), 404
        
        note.title = data['title']
        note.content = data['content']
        note.updated_at = datetime.datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Note updated successfully',
            'note': note.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/notes/<int:note_id>', methods=['DELETE'])
@token_required
def delete_note(current_user, note_id):
    """DELETE /notes/{id}: Deletes a note"""
    try:
        note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
        
        if not note:
            return jsonify({'message': 'Note not found'}), 404
        
        db.session.delete(note)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Note deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        try:
            print("Creating database tables...")
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")
            print("Make sure your MySQL database is running and the connection string is correct.")
    
    # Get host and port from environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 3001))
    
    print(f"Starting Flask server on {host}:{port}")
    app.run(debug=True, host=host, port=port) 