// frontend/src/pages/Extensions.jsx
import React, { useState } from 'react';
import { Routes, Route, NavLink, Outlet } from 'react-router-dom';
import { 
  Puzzle, 
  Zap, 
  GitBranch,
  Plus,
  Settings,
  Play,
  StopCircle
} from 'lucide-react';
import Button from '../components/common/Button';

const ExtensionsLayout = () => {
  const navigation = [
    {
      name: 'Extensions',
      href: '/extensions/list',
      icon: Puzzle,
    },
    {
      name: 'Intégrations API',
      href: '/extensions/integrations',
      icon: Zap,
    },
    {
      name: 'Webhooks',
      href: '/extensions/webhooks',
      icon: GitBranch,
    },
  ];

  return (
    <div className="ml-64 p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Extensions</h1>
        <p className="text-gray-600">Étendez les fonctionnalités de votre ERP</p>
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

const ExtensionsList = () => {
  const [extensions, setExtensions] = useState([
    {
      id: 1,
      name: 'Module Bibliothèque',
      version: '1.2.0',
      description: 'Gestion complète de la bibliothèque scolaire',
      author: 'EduERP Team',
      enabled: true,
      status: 'active'
    },
    {
      id: 2,
      name: 'Module Transport',
      version: '1.0.0',
      description: 'Gestion des transports scolaires',
      author: 'EduERP Team',
      enabled: false,
      status: 'inactive'
    },
    {
      id: 3,
      name: 'Module Cantine',
      version: '1.1.5',
      description: 'Gestion de la restauration scolaire',
      author: 'EduERP Team',
      enabled: true,
      status: 'active'
    }
  ]);

  const toggleExtension = (id) => {
    setExtensions(extensions.map(ext => 
      ext.id === id ? { ...ext, enabled: !ext.enabled } : ext
    ));
  };

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-800">Gestion des extensions</h2>
          <p className="text-gray-600">Installez et gérez les modules additionnels</p>
        </div>
        <Button>
          <Plus className="w-4 h-4 mr-2" />
          Installer une extension
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {extensions.map((extension) => (
          <div key={extension.id} className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                <Puzzle className="w-6 h-6 text-blue-600" />
              </div>
              <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                extension.enabled ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
              }`}>
                {extension.enabled ? 'Activé' : 'Désactivé'}
              </span>
            </div>

            <h3 className="text-lg font-semibold text-gray-800 mb-2">{extension.name}</h3>
            <p className="text-sm text-gray-600 mb-4">{extension.description}</p>

            <div className="flex items-center justify-between mb-4">
              <span className="text-sm text-gray-500">v{extension.version}</span>
              <span className="text-sm text-gray-500">par {extension.author}</span>
            </div>

            <div className="flex space-x-2">
              <Button
                variant={extension.enabled ? 'danger' : 'primary'}
                size="sm"
                className="flex-1"
                onClick={() => toggleExtension(extension.id)}
              >
                {extension.enabled ? (
                  <>
                    <StopCircle className="w-4 h-4 mr-2" />
                    Désactiver
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 mr-2" />
                    Activer
                  </>
                )}
              </Button>
              <Button variant="outline" size="sm">
                <Settings className="w-4 h-4" />
              </Button>
            </div>
          </div>
        ))}

        {/* Carte d'ajout d'extension */}
        <div className="bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 p-6 flex flex-col items-center justify-center">
          <div className="w-10 h-10 bg-gray-200 rounded-lg flex items-center justify-center mb-4">
            <Plus className="w-6 h-6 text-gray-400" />
          </div>
          <h3 className="text-lg font-semibold text-gray-600 mb-2">Nouvelle extension</h3>
          <p className="text-sm text-gray-500 text-center mb-4">
            Installez de nouvelles extensions pour étendre les fonctionnalités de votre ERP
          </p>
          <Button variant="outline">
            <Plus className="w-4 h-4 mr-2" />
            Parcourir les extensions
          </Button>
        </div>
      </div>
    </div>
  );
};

const Integrations = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Intégrations API</h2>
    <p className="text-gray-600">Contenu des intégrations API...</p>
  </div>
);

const Webhooks = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Gestion des webhooks</h2>
    <p className="text-gray-600">Contenu de la gestion des webhooks...</p>
  </div>
);

const Extensions = () => {
  return (
    <Routes>
      <Route path="/" element={<ExtensionsLayout />}>
        <Route path="list" element={<ExtensionsList />} />
        <Route path="integrations" element={<Integrations />} />
        <Route path="webhooks" element={<Webhooks />} />
        <Route path="" element={<Navigate to="list" />} />
      </Route>
    </Routes>
  );
};

export default Extensions;