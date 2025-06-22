import axios from 'axios';
import { 
  LoginCredentials, 
  User, 
  Note, 
  LoginResponse, 
  HomeResponse, 
  NotesResponse, 
  NoteResponse 
} from '../types';

const API_BASE_URL = 'http://localhost:3001';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API functions
export const login = async (credentials: LoginCredentials): Promise<LoginResponse> => {
  const response = await api.post<LoginResponse>('/login', credentials);
  return response.data;
};

export const checkAuth = async (): Promise<HomeResponse> => {
  const response = await api.get<HomeResponse>('/');
  return response.data;
};

export const logout = async (): Promise<void> => {
  await api.post('/logout');
  localStorage.removeItem('authToken');
};

// Notes API functions
export const getNotes = async (): Promise<NotesResponse> => {
  const response = await api.get<NotesResponse>('/notes');
  return response.data;
};

export const createNote = async (noteData: { title: string; content: string }): Promise<NoteResponse> => {
  const response = await api.post<NoteResponse>('/notes', noteData);
  return response.data;
};

export const updateNote = async (noteId: number, noteData: { title: string; content: string }): Promise<NoteResponse> => {
  const response = await api.put<NoteResponse>(`/notes/${noteId}`, noteData);
  return response.data;
};

export const deleteNote = async (noteId: number): Promise<{ success: boolean; message: string }> => {
  const response = await api.delete(`/notes/${noteId}`);
  return response.data;
};

export default api; 