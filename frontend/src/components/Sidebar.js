import React from 'react';

function Sidebar({ conversations, currentConversation, setCurrentConversation }) {
  return (
    <div className="sidebar">
      <h2>Conversations</h2>
      <ul className="conversation-list">
        {conversations.map((conv, index) => (
          <li
            key={index}
            className={`conversation-item ${currentConversation === index ? 'active' : ''}`}
            onClick={() => setCurrentConversation(index)}
          >
            {conv.title}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Sidebar;

