import React, { useState, useEffect } from 'react';
import { getNotes, createNote, updateNote, deleteNote } from '../services/api';
import { Note, NotesPageProps } from '../types';
import NoteModal from './NoteModal';
import './NotesPage.css';

const NotesPage: React.FC<NotesPageProps> = ({ user, onLogout }) => {
  const [notes, setNotes] = useState<Note[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingNote, setEditingNote] = useState<Note | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchNotes();
  }, []);

  const fetchNotes = async () => {
    try {
      setIsLoading(true);
      const response = await getNotes();
      if (response.success) {
        setNotes(response.notes);
      }
    } catch (error: any) {
      setError('Failed to load notes');
      console.error('Error fetching notes:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateNote = () => {
    setEditingNote(null);
    setShowModal(true);
  };

  const handleEditNote = (note: Note) => {
    setEditingNote(note);
    setShowModal(true);
  };

  const handleDeleteNote = async (noteId: number) => {
    if (window.confirm('Are you sure you want to delete this note?')) {
      try {
        const response = await deleteNote(noteId);
        if (response.success) {
          setNotes(notes.filter(note => note.id !== noteId));
        }
      } catch (error: any) {
        setError('Failed to delete note');
        console.error('Error deleting note:', error);
      }
    }
  };

  const handleSaveNote = async (noteData: { title: string; content: string }) => {
    try {
      if (editingNote) {
        // Update existing note
        const response = await updateNote(editingNote.id, noteData);
        if (response.success) {
          setNotes(notes.map(note => 
            note.id === editingNote.id ? response.note : note
          ));
        }
      } else {
        // Create new note
        const response = await createNote(noteData);
        if (response.success) {
          setNotes([...notes, response.note]);
        }
      }
      setShowModal(false);
      setEditingNote(null);
    } catch (error: any) {
      setError('Failed to save note');
      console.error('Error saving note:', error);
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingNote(null);
  };

  if (isLoading) {
    return (
      <div className="notes-loading">
        <div className="loading-spinner"></div>
        <p>Loading notes...</p>
      </div>
    );
  }

  return (
    <div className="notes-container">
      <div className="notes-header">
        <h1>My Notes</h1>
        <div className="header-actions">
          <button onClick={handleCreateNote} className="create-note-btn">
            Create Note
          </button>
          <button onClick={onLogout} className="logout-button">
            Logout
          </button>
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <div className="notes-grid">
        {notes.length === 0 ? (
          <div className="no-notes">
            <p>No notes yet. Create your first note!</p>
          </div>
        ) : (
          notes.map(note => (
            <div key={note.id} className="note-card">
              <div className="note-header">
                <h3>{note.title}</h3>
                <div className="note-actions">
                  <button 
                    onClick={() => handleEditNote(note)}
                    className="edit-btn"
                  >
                    Edit
                  </button>
                  <button 
                    onClick={() => handleDeleteNote(note.id)}
                    className="delete-btn"
                  >
                    Delete
                  </button>
                </div>
              </div>
              <div className="note-content">
                {note.content}
              </div>
              <div className="note-footer">
                <small>Updated: {new Date(note.updated_at).toLocaleDateString()}</small>
              </div>
            </div>
          ))
        )}
      </div>

      {showModal && (
        <NoteModal
          note={editingNote}
          onSave={handleSaveNote}
          onClose={handleCloseModal}
        />
      )}
    </div>
  );
};

export default NotesPage; 