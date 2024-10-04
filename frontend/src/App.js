import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import axios from 'axios';
import './styles.css';

function App() {
  const [conversations, setConversations] = useState([
    { title: 'Property Rights', messages: [{ sender: 'bot', content: 'How can I help you with property rights?' }] },
    { title: 'Contract Law', messages: [{ sender: 'bot', content: 'Let\'s discuss contract law.' }] },
  ]);
  const [currentConversation, setCurrentConversation] = useState(0);

  const sendMessage = async (content) => {
    const newMessages = [...conversations];
    newMessages[currentConversation].messages.push({ sender: 'user', content });
    setConversations(newMessages);

    try {
      const response = await axios.post('https://your-heroku-backend.herokuapp.com/get-answer', {
        question: content,
      });
      newMessages[currentConversation].messages.push({ sender: 'bot', content: response.data.answer });
      setConversations(newMessages);
    } catch (error) {
      newMessages[currentConversation].messages.push({ sender: 'bot', content: 'An error occurred. Please try again.' });
      setConversations(newMessages);
    }
  };

  return (
    <div className="main-container">
      <Sidebar
        conversations={conversations}
        currentConversation={currentConversation}
        setCurrentConversation={setCurrentConversation}
      />
      <ChatWindow
        currentConversation={currentConversation}
        conversations={conversations}
        sendMessage={sendMessage}
      />
    </div>
  );
}

export default App;

