import React, { useState } from "react";
import axios from "axios";
import { getAiRecipe } from "../api"; // Import API function
import "./AiSuggestion.css"; // Import the CSS for styling

const AiSuggestion = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input) return;
  
    // Add the user's message to the chat
    setMessages((prevMessages) => [
      ...prevMessages,
      { type: "user", text: input },
    ]);
  
    setLoading(true);
  
    try {
      const ingredients = input.split(",").map((i) => i.trim());
      const response = await axios.post("http://127.0.0.1:5000/ai_recipe_suggestion", {
        ingredients: ingredients,
      });
  
      if (response.data && response.data.recipe_text) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { type: "ai", text: response.data.recipe_text },
        ]);
      } else {
        setMessages((prevMessages) => [
          ...prevMessages,
          { type: "ai", text: "No response from AI." },
        ]);
      }
    } catch (error) {
      console.error("AI recipe generation failed", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { type: "ai", text: "An error occurred while generating recipe." },
      ]);
    } finally {
      setLoading(false);
    }
  
    setInput(""); // Reset input after sending
  };
  
  

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.type === "user" ? "user-msg" : "ai-msg"}`}
          >
            <p>{msg.text}</p>
          </div>
        ))}
        {loading && (
          <div className="message ai-msg">
            <p>Generating recipe...</p>
          </div>
        )}
      </div>

      <div className="input-container">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter ingredients (e.g., chicken, garlic, onion)"
          className="input-box"
        />
        <button onClick={handleSend} className="send-btn">
          Send
        </button>
      </div>
    </div>
  );
};

export default AiSuggestion;
