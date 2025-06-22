// User related types
export interface User {
  id: number;
  email: string;
}

// Authentication types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface LoginResponse {
  success: boolean;
  message: string;
  token: string;
  user: User;
}

export interface HomeResponse {
  success: boolean;
  message: string;
  authenticated: boolean;
  user: User;
}

// Note related types
export interface Note {
  id: number;
  title: string;
  content: string;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface NotesResponse {
  success: boolean;
  notes: Note[];
}

export interface NoteResponse {
  success: boolean;
  message: string;
  note: Note;
}

// Component prop types
export interface LoginPageProps {
  onLoginSuccess: (user: User) => void;
}

export interface HomePageProps {
  user: User;
  onLogout: () => void;
}

export interface NotesPageProps {
  user: User;
  onLogout: () => void;
}

export interface NoteModalProps {
  note?: Note | null;
  onSave: (noteData: { title: string; content: string }) => void;
  onClose: () => void;
} 