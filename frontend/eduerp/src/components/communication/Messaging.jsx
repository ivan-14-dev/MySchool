// frontend/src/components/communication/Messaging.jsx
import React, { useState, useEffect } from 'react';
import { Send, Paperclip, Search, User, Clock } from 'lucide-react';
import { messagingService } from '../../services/api';
import Button from '../common/Button';

const Messaging = () => {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  useEffect(() => {
    loadConversations();
  }, []);

  useEffect(() => {
    if (selectedConversation) {
      loadMessages(selectedConversation.id);
    }
  }, [selectedConversation]);

  const loadConversations = async () => {
    try {
      const response = await messagingService.getConversations();
      setConversations(response.data);
      if (response.data.length > 0) {
        setSelectedConversation(response.data[0]);
      }
    } catch (error) {
      console.error('Error loading conversations:', error);
    }
  };

  const loadMessages = async (conversationId) => {
    try {
      const response = await messagingService.getMessages(conversationId);
      setMessages(response.data);
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const sendMessage = async () => {
    if (!newMessage.trim() || !selectedConversation) return;

    try {
      await messagingService.sendMessage(selectedConversation.id, {
        content: newMessage,
        type: 'text'
      });
      setNewMessage('');
      loadMessages(selectedConversation.id);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="flex h-[600px] bg-white rounded-lg shadow-sm">
      {/* Sidebar des conversations */}
      <div className="w-1/3 border-r">
        <div className="p-4 border-b">
          <h3 className="font-semibold text-gray-800">Messages</h3>
          <div className="relative mt-3">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Rechercher..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
        </div>
        
        <div className="overflow-y-auto">
          {conversations.map(conversation => (
            <div
              key={conversation.id}
              className={`p-4 border-b cursor-pointer hover:bg-gray-50 ${
                selectedConversation?.id === conversation.id ? 'bg-blue-50' : ''
              }`}
              onClick={() => setSelectedConversation(conversation)}
            >
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white">
                  <User className="w-5 h-5" />
                </div>
                <div className="flex-1">
                  <div className="flex justify-between items-start">
                    <h4 className="font-medium text-gray-800">
                      {conversation.participants[0].first_name} {conversation.participants[0].last_name}
                    </h4>
                    <span className="text-xs text-gray-500">
                      <Clock className="w-3 h-3 inline mr-1" />
                      {conversation.last_message_time}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 truncate">
                    {conversation.last_message}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Zone de conversation */}
      <div className="flex-1 flex flex-col">
        {selectedConversation && (
          <>
            <div className="p-4 border-b">
              <h3 className="font-semibold text-gray-800">
                {selectedConversation.participants[0].first_name} {selectedConversation.participants[0].last_name}
              </h3>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map(message => (
                <div
                  key={message.id}
                  className={`flex ${message.is_own ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                      message.is_own
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    <p>{message.content}</p>
                    <span className={`text-xs ${message.is_own ? 'text-blue-200' : 'text-gray-500'}`}>
                      {message.timestamp}
                    </span>
                  </div>
                </div>
              ))}
            </div>

            <div className="p-4 border-t">
              <div className="flex space-x-3">
                <button className="p-2 text-gray-400 hover:text-gray-600">
                  <Paperclip className="w-5 h-5" />
                </button>
                <input
                  type="text"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                  placeholder="Tapez votre message..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
                <Button onClick={sendMessage}>
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Messaging;