import React, { useState } from 'react';
import axios from 'axios';

import styled from 'styled-components';

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin-bottom: 100px;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.1);
`;

const Input = styled.input`
  margin: 10px 0;
  padding: 10px;
  width: 200px;
`;

const Button = styled.button`
  margin: 10px 0;
  padding: 10px;
  width: 220px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
`;

const Error = styled.div`
  color: red;
`;

const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [isSignup, setIsSignup] = useState(false);


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
    <><div>
      Login to Chatbot
    </div><Container>
        <Form onSubmit={isSignup ? handleSignup : handleLogin}>
          <Input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
          <Input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
          {isSignup && (
            <>
              <Input type="text" placeholder="Name" value={name} onChange={e => setName(e.target.value)} required />
              <Input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
            </>
          )}
          <Button type="submit">{isSignup ? 'Sign Up' : 'Log In'}</Button>
          <Button type="button" onClick={() => setIsSignup(!isSignup)}>{isSignup ? 'Log In Instead' : 'Sign Up Instead'}</Button>
          {error && <Error>{error}</Error>}
        </Form>
      </Container></>
  );
};

export default Login;