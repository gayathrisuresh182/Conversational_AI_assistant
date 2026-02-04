import React from 'react';
import Message from './Message';
import './MessageList.css';

const MessageList = ({ messages, isLoading, messagesEndRef }) => {
  return (
    <div className="message-list">
      {messages.length === 0 && (
        <div className="empty-state">
          <div className="empty-icon">💬</div>
          <h2>Start a conversation</h2>
          <p>Ask me anything! I can search the web, do calculations, answer questions about your documents, and remember your preferences.</p>
        </div>
      )}
      
      {messages.map((message, index) => (
        <Message key={index} message={message} />
      ))}
      
      {isLoading && (
        <div className="loading-message">
          <div className="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}
      
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;

