import React, { useState } from "react";
import axios from "axios";

const backend = "http://localhost:5000";

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);

    const res = await axios.post(`${backend}/ask`, {
      query: input,
    });

    const botMsg = { sender: "bot", text: res.data.answer };
    setMessages((prev) => [...prev, botMsg]);

    setInput("");
  };

  return (
    <>
      <div className="chat-box">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>

      <div className="input-row">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something from the PDF…"
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </>
  );
}

export default ChatBox;