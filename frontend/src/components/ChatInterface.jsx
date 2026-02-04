import React, { useState, useEffect, useRef } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import DocumentUpload from './DocumentUpload';
import { sendMessage, getConversations } from '../services/api';
import './ChatInterface.css';

const ChatInterface = ({ userId }) => {
  const [messages, setMessages] = useState([]);
  const [conversationId, setConversationId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [conversations, setConversations] = useState([]);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Load conversations on mount
    loadConversations();
  }, [userId]);

  useEffect(() => {
    // Scroll to bottom when messages change
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversations = async () => {
    try {
      const convos = await getConversations(userId);
      setConversations(convos);
      
      // Load most recent conversation if available
      if (convos.length > 0 && !conversationId) {
        loadConversation(convos[0].id);
      }
    } catch (error) {
      console.error('Error loading conversations:', error);
    }
  };

  const loadConversation = async (convId) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/chat/conversations/${convId}/messages`);
      const data = await response.json();
      
      setMessages(data.map(msg => ({
        role: msg.role,
        content: msg.content,
        timestamp: msg.created_at
      })));
      setConversationId(convId);
    } catch (error) {
      console.error('Error loading conversation:', error);
    }
  };

  const handleSendMessage = async (messageText) => {
    if (!messageText.trim()) return;

    // Add user message to UI immediately
    const userMessage = {
      role: 'user',
      content: messageText,
      timestamp: new Date().toISOString()
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendMessage({
        user_id: userId,
        conversation_id: conversationId,
        message: messageText
      });

      // Update conversation ID if new conversation was created
      if (response.conversation_id !== conversationId) {
        setConversationId(response.conversation_id);
        loadConversations();
      }

      // Add assistant response
      const assistantMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
        tool_calls: response.tool_calls
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
        error: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewConversation = () => {
    setConversationId(null);
    setMessages([]);
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h1>🤖 AI Assistant</h1>
        <div className="header-actions">
          <button onClick={handleNewConversation} className="new-chat-btn">
            New Chat
          </button>
          <DocumentUpload userId={userId} />
        </div>
      </div>
      
      <MessageList 
        messages={messages} 
        isLoading={isLoading}
        messagesEndRef={messagesEndRef}
      />
      
      <MessageInput 
        onSendMessage={handleSendMessage}
        disabled={isLoading}
      />
    </div>
  );
};

export default ChatInterface;

