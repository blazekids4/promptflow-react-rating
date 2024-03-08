import React, { useState } from 'react';
import axios from 'axios';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (input.trim()) {
      const newMessage = { text: input, sender: 'user' };
      setMessages([...messages, newMessage]);
      console.log(messages);
      const response = await axios.post('http://127.0.0.1:5000/api/chat', { prompt: input, chat_history: messages });

      const botResponse = { text: response.data.response, sender: 'bot' };
      setMessages([...messages, newMessage, botResponse]);
      setInput('');
    }
  };

  return (
    <div id="chat-container" className="chat-container">
      <div className="messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            {message.text}
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type a message..."
        />
        <button onClick={sendMessage}>SEND</button>
      </div>
    </div>
  );
};

export default Chat;
