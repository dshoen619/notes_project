import React from 'react';
import { HomePageProps } from '../types';
import './HomePage.css';

const HomePage: React.FC<HomePageProps> = ({ user, onLogout }) => {
  return (
    <div className="home-container">
      <div className="home-header">
        <h1>Welcome to Your Dashboard</h1>
        <button onClick={onLogout} className="logout-button">
          Logout
        </button>
      </div>
      
      <div className="home-content">
        <div className="user-info">
          <h2>User Information</h2>
          <div className="info-item">
            <strong>ID:</strong> {user.id}
          </div>
          <div className="info-item">
            <strong>Email:</strong> {user.email}
          </div>
        </div>
        
        <div className="welcome-message">
          <p>You have successfully logged in and are viewing the protected home page.</p>
          <p>This page is only accessible with a valid JWT token.</p>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 