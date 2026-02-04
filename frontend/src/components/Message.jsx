import React from 'react';
import './Message.css';

const Message = ({ message }) => {
  const isUser = message.role === 'user';
  
  return (
    <div className={`message ${isUser ? 'user-message' : 'assistant-message'}`}>
      <div className="message-content">
        {message.content}
        {message.tool_calls && message.tool_calls.length > 0 && (
          <div className="tool-calls">
            <small>Used tools: {message.tool_calls.map(tc => tc.tool).join(', ')}</small>
          </div>
        )}
        {message.error && (
          <div className="error-indicator">⚠️ Error occurred</div>
        )}
      </div>
      {message.timestamp && (
        <div className="message-timestamp">
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      )}
    </div>
  );
};

export default Message;

