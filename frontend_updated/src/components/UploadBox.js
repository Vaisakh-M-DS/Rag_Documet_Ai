import React, { useState } from "react";
import axios from "axios";

const backend = "http://localhost:5000";

function UploadBox() {
  const [file, setFile] = useState(null);
  const [msg, setMsg] = useState("");

  const upload = async () => {
    if (!file) return alert("Select a file first!");

    const form = new FormData();
    form.append("file", file);

    const res = await axios.post(`${backend}/upload`, form);
    setMsg(res.data.message);
  };

  return (
    <div>
      <h3>Upload a PDF (up to 50 MB)</h3>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button style={{ marginLeft: "15px" }} onClick={upload}>
        Upload
      </button>

      {msg && <p style={{ marginTop: "10px", color: "green" }}>{msg}</p>}
    </div>
  );
}

export default UploadBox;