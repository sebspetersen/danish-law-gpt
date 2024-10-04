import React from 'react';
import MessageItem from './MessageItem';
import ChatInput from './ChatInput';

function ChatWindow({ currentConversation, conversations, sendMessage }) {
  return (
    <div className="chat-window">
      <div className="chat-header">
        <h1>Danish Law Expert</h1>
      </div>
      <div className="chat-box">
        {conversations[currentConversation].messages.map((message, index) => (
          <MessageItem key={index} message={message} />
        ))}
      </div>
      <ChatInput sendMessage={sendMessage} />
    </div>
  );
}

export default ChatWindow;

