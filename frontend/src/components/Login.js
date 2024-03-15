import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/login', {
        username,
        password
      });
      if (response.status === 200) {
        onLoginSuccess();
      }
    } catch (err) {
      console.log(err);
      console.log(err.response);
      setError('Invalid credentials');
    }
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/signup', {
        username,
        password,
        email,
        name
      });
      if (response.status === 200) {
        onLoginSuccess();
      }
    } catch (err) {
      console.log(err);
      console.log(err.response);
      setError('Error creating account');
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleLogin}>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={e => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Login</button>
      </form>
      <h2>Create Account</h2>
      <form onSubmit={handleSignup}>
        <div>
          <label htmlFor="new-username">Username:</label>
          <input
            type="text"
            id="new-username"
            value={username}
            onChange={e => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="new-password">Password:</label>
          <input
            type="password"
            id="new-password"
            value={password}
            onChange={e => setPassword(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={e => setName(e.target.value)}
          />
        </div>
        <button type="submit">Create Account</button>
      </form>
    </div>
  );
};

export default Login;
