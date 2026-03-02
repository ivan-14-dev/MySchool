// frontend/src/pages/Communication.jsx
import React, { useState } from 'react';
import { Routes, Route, NavLink, Outlet } from 'react-router-dom';
import { 
  MessageSquare, 
  Bell, 
  Mail, 
  Send,
  Plus,
  Search
} from 'lucide-react';
import Button from '../components/common/Button';

const CommunicationLayout = () => {
  const navigation = [
    {
      name: 'Messagerie',
      href: '/communication/messaging',
      icon: MessageSquare,
    },
    {
      name: 'Notifications',
      href: '/communication/notifications',
      icon: Bell,
    },
    {
      name: 'Emails',
      href: '/communication/emails',
      icon: Mail,
    },
    {
      name: 'Annonces',
      href: '/communication/announcements',
      icon: Send,
    },
  ];

  return (
    <div className="ml-64 p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Communication</h1>
        <p className="text-gray-600">Communiquez avec les étudiants, parents et enseignants</p>
      </div>

      <nav className="bg-white rounded-lg shadow-sm p-4 mb-6">
        <div className="flex space-x-8">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                `flex items-center space-x-2 px-3 py-2 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
                }`
              }
            >
              <item.icon className="w-5 h-5" />
              <span className="font-medium">{item.name}</span>
            </NavLink>
          ))}
        </div>
      </nav>

      <div className="bg-white rounded-lg shadow-sm">
        <Outlet />
      </div>
    </div>
  );
};

const Messaging = () => {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-800">Messagerie</h2>
          <p className="text-gray-600">Communiquez avec les étudiants et parents</p>
        </div>
        <Button>
          <Plus className="w-4 h-4 mr-2" />
          Nouveau message
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Liste des conversations */}
        <div className="lg:col-span-1 bg-white rounded-lg border border-gray-200">
          <div className="p-4 border-b">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Rechercher une conversation..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          <div className="divide-y divide-gray-200 max-h-96 overflow-y-auto">
            {[].map((conversation, index) => (
              <div
                key={index}
                className={`p-4 cursor-pointer hover:bg-gray-50 ${
                  selectedConversation?.id === conversation.id ? 'bg-blue-50' : ''
                }`}
                onClick={() => setSelectedConversation(conversation)}
              >
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white">
                    {conversation.name[0]}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <h3 className="text-sm font-medium text-gray-900 truncate">
                        {conversation.name}
                      </h3>
                      <span className="text-xs text-gray-500">{conversation.time}</span>
                    </div>
                    <p className="text-sm text-gray-500 truncate">{conversation.lastMessage}</p>
                    {conversation.unread > 0 && (
                      <span className="inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white bg-red-500 rounded-full">
                        {conversation.unread}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {[].length === 0 && (
            <div className="text-center py-12">
              <MessageSquare className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Aucune conversation</h3>
              <p className="text-gray-500">Commencez une nouvelle conversation.</p>
            </div>
          )}
        </div>

        {/* Zone de conversation */}
        <div className="lg:col-span-2 bg-white rounded-lg border border-gray-200">
          {selectedConversation ? (
            <div className="flex flex-col h-96">
              {/* En-tête de conversation */}
              <div className="p-4 border-b">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white">
                    {selectedConversation.name[0]}
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-gray-900">{selectedConversation.name}</h3>
                    <p className="text-sm text-gray-500">En ligne</p>
                  </div>
                </div>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-lg px-4 py-2 max-w-xs">
                    <p className="text-sm text-gray-800">Bonjour, comment puis-je vous aider ?</p>
                    <span className="text-xs text-gray-500">10:30</span>
                  </div>
                </div>

                <div className="flex justify-end">
                  <div className="bg-blue-500 text-white rounded-lg px-4 py-2 max-w-xs">
                    <p className="text-sm">J'ai une question concernant les frais de scolarité.</p>
                    <span className="text-xs text-blue-200">10:32</span>
                  </div>
                </div>
              </div>

              {/* Input message */}
              <div className="p-4 border-t">
                <div className="flex space-x-3">
                  <input
                    type="text"
                    placeholder="Tapez votre message..."
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                  <Button>Envoyer</Button>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <MessageSquare className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Sélectionnez une conversation</h3>
              <p className="text-gray-500">Choisissez une conversation pour commencer à discuter.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const Notifications = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Gestion des notifications</h2>
    <p className="text-gray-600">Contenu de la gestion des notifications...</p>
  </div>
);

const Emails = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Gestion des emails</h2>
    <p className="text-gray-600">Contenu de la gestion des emails...</p>
  </div>
);

const Announcements = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Gestion des annonces</h2>
    <p className="text-gray-600">Contenu de la gestion des annonces...</p>
  </div>
);

const Communication = () => {
  return (
    <Routes>
      <Route path="/" element={<CommunicationLayout />}>
        <Route path="messaging" element={<Messaging />} />
        <Route path="notifications" element={<Notifications />} />
        <Route path="emails" element={<Emails />} />
        <Route path="announcements" element={<Announcements />} />
        <Route path="" element={<Navigate to="messaging" />} />
      </Route>
    </Routes>
  );
};

export default Communication;