import React, { useState, useEffect, useRef } from 'react';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  const [userId] = useState(() => {
    // Generate or retrieve user ID from localStorage
    let id = localStorage.getItem('userId');
    if (!id) {
      id = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('userId', id);
    }
    return id;
  });

  return (
    <div className="App">
      <ChatInterface userId={userId} />
    </div>
  );
}

export default App;

