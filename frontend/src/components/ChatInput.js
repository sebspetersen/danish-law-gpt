import React, { useState } from 'react';

function ChatInput({ sendMessage }) {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      sendMessage(input);
      setInput('');
    }
  };

  return (
    <div className="chat-input-container">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your legal question..."
        rows="2"
      />
      <button onClick={handleSend}><i className="fas fa-paper-plane"></i></button>
    </div>
  );
}

export default ChatInput;

