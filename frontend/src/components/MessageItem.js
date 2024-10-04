import React from 'react';

function MessageItem({ message }) {
  const { sender, content } = message;

  return (
    <div className={`message ${sender}`}>
      <span>{content}</span>
    </div>
  );
}

export default MessageItem;

