import React, { useState } from 'react';
import Chat from './components/Chat';
import Login from './components/Login';

import './App.css';

function App() {
  const [user, setUser] = useState(null);

  const handleLoginSuccess = () => {
    setUser(true);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h3>Chat</h3>
      </header>
      {user ? (  // Check if user is logged in
        <Chat />
      ) : (
        <Login onLoginSuccess={handleLoginSuccess} />
      )}
    </div>
  );
}

export default App;