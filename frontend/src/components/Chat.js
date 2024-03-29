import React, { useState } from "react";
import axios from "axios";
import "./Chat.css";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [rating, setRating] = useState(null); // New state variable for the rating
  const [context, setContext] = useState("context1");

  const startNewSession = async () => {
    setMessages([]); // Clear existing messages
    setSessionId(null); // Reset the session ID

    // Call API endpoint to start a new session
    try {
      const sessionResponse = await axios.post(
        "http://127.0.0.1:5000/api/chat/session"
      );
      setSessionId(sessionResponse.data.session_id);
    } catch (error) {
      console.error("Error starting a new session:", error);
    }
  };
  const sendMessage = async () => {
    if (input.trim()) {
      if (!sessionId) {
        // If there's no session ID, create a new session
        const sessionResponse = await axios.post(
          "http://127.0.0.1:5000/api/chat/session"
        );
        setSessionId(sessionResponse.data.session_id);
      }

      const newMessage = { text: input, sender: "user" };
      setMessages([...messages, newMessage]);

      const response = await axios.post("http://127.0.0.1:5000/api/chat", {
        prompt: input,
        session_id: sessionId, // Include the session ID in the request
        context: context, // Include the selected context in the request
      });

      const botResponse = { text: response.data.response, sender: "bot" };
      setMessages([...messages, newMessage, botResponse]);
      setInput("");
    }
  };

  const rateResponse = async (thumbsUp) => {
    console.log("Rating response:", thumbsUp);
    if (sessionId) {
      try {
        await axios.post("http://127.0.0.1:5000/api/chat/rate", {
          session_id: sessionId,
          thumbs_up: thumbsUp,
        });
        console.log(`You have given a thumbs ${thumbsUp ? "up" : "down"}`);
        alert(`You have given a thumbs ${thumbsUp ? "up" : "down"}`);
        setRating(thumbsUp ? "up" : "down"); // Update the rating state
      } catch (error) {
        console.error("Error rating the response:", error);
      }
    } else {
      console.log("No session ID available to rate the response");
    }
  };

  return (
    <div id="master-container" className="master-container">
      <div id="chat-container" className="chat-container">
        <div className="messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              {message.text}
            </div>
          ))}
        </div>
        <div className="input-area">
          <select onChange={(e) => setContext(e.target.value)}>
            <option value="context1">Context 1</option>
            <option value="context2">Context 2</option>
            {/* Add more options as needed */}
          </select>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Type a message..."
          />
          <button onClick={sendMessage}>SEND</button>
          <button onClick={() => rateResponse(true)}>👍</button>
          <button onClick={() => rateResponse(false)}>👎</button>
          <button onClick={startNewSession}>RESET</button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
