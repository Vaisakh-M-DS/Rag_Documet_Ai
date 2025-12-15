import React, { useState, useRef, useEffect } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const chatRef = useRef(null);

  // Auto scroll chat down
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  // Upload PDF
  const handleUpload = async () => {
    if (!file) return alert("Please select a PDF");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      alert(data.message || "Uploaded!");
    } catch (err) {
      alert("Upload failed");
      console.error(err);
    }
  };

  // Send chat message
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);

    const queryToSend = input;
    setInput("");

    try {
      const res = await fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: queryToSend }),
      });

      const data = await res.json();

      const botMsg = {
        sender: "bot",
        text: data.answer || "No answer returned.",
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error(err);
      const errorMsg = { sender: "bot", text: "Backend error." };
      setMessages((prev) => [...prev, errorMsg]);
    }
  };

  return (
    <div>
      <div className="header">VaisakhAI</div>

      <div className="main-box">

        {/* Upload Section */}
        <div className="upload-section">
          <h3>Upload</h3>

          <div className="upload-controls">
            <input
              type="file"
              accept="application/pdf"
              onChange={(e) => setFile(e.target.files[0])}
            />
            <button className="upload-btn" onClick={handleUpload}>
              Upload
            </button>
          </div>
        </div>

        <hr />

        {/* Chat Section */}
        <div className="chat-section">
          <h3>Answer AI</h3>

          <div className="chat-box" ref={chatRef}>
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`message ${msg.sender === "user" ? "user" : "bot"}`}
              >
                {msg.text}
              </div>
            ))}
          </div>

          <div className="input-row">
            <input
              className="input-field"
              placeholder="Ask something about your PDF..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            />

            <button className="send-btn" onClick={sendMessage}>
              Send
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;

