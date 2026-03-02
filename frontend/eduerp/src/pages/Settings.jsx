// frontend/src/pages/Settings.jsx
import React, { useState } from 'react';
import { Routes, Route, NavLink, Outlet } from 'react-router-dom';
import { 
  User, 
  Bell, 
  Shield, 
  School,
  CreditCard,
  Database,
  Network,
  Save
} from 'lucide-react';
import Button from '../components/common/Button';

const SettingsLayout = () => {
  const navigation = [
    {
      name: 'Profil',
      href: '/settings/profile',
      icon: User,
    },
    {
      name: 'Notifications',
      href: '/settings/notifications',
      icon: Bell,
    },
    {
      name: 'Sécurité',
      href: '/settings/security',
      icon: Shield,
    },
    {
      name: 'Établissement',
      href: '/settings/school',
      icon: School,
    },
    {
      name: 'Paiements',
      href: '/settings/payments',
      icon: CreditCard,
    },
    {
      name: 'Sauvegarde',
      href: '/settings/backup',
      icon: Database,
    },
    {
      name: 'Réseau',
      href: '/settings/network',
      icon: Network,
    },
  ];

  return (
    <div className="ml-64 p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Paramètres</h1>
        <p className="text-gray-600">Configurez votre application selon vos besoins</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Navigation */}
        <div className="lg:col-span-1">
          <nav className="bg-white rounded-lg shadow-sm p-4">
            <div className="space-y-2">
              {navigation.map((item) => (
                <NavLink
                  key={item.name}
                  to={item.href}
                  className={({ isActive }) =>
                    `flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
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
        </div>

        {/* Contenu */}
        <div className="lg:col-span-3">
          <div className="bg-white rounded-lg shadow-sm">
            <Outlet />
          </div>
        </div>
      </div>
    </div>
  );
};

const ProfileSettings = () => {
  const [profile, setProfile] = useState({
    firstName: 'Jean',
    lastName: 'Dupont',
    email: 'jean.dupont@exemple.com',
    phone: '+33 6 12 34 56 78',
    position: 'Directeur',
    department: 'Direction'
  });

  const handleSave = () => {
    // Logique de sauvegarde
    alert('Profil sauvegardé avec succès!');
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-6">Paramètres du profil</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Prénom</label>
          <input
            type="text"
            value={profile.firstName}
            onChange={(e) => setProfile({ ...profile, firstName: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Nom</label>
          <input
            type="text"
            value={profile.lastName}
            onChange={(e) => setProfile({ ...profile, lastName: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
          <input
            type="email"
            value={profile.email}
            onChange={(e) => setProfile({ ...profile, email: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Téléphone</label>
          <input
            type="tel"
            value={profile.phone}
            onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Poste</label>
          <input
            type="text"
            value={profile.position}
            onChange={(e) => setProfile({ ...profile, position: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Département</label>
          <select
            value={profile.department}
            onChange={(e) => setProfile({ ...profile, department: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="Direction">Direction</option>
            <option value="Enseignement">Enseignement</option>
            <option value="Administration">Administration</option>
            <option value="Finance">Finance</option>
          </select>
        </div>
      </div>

      <div className="flex justify-end">
        <Button onClick={handleSave}>
          <Save className="w-4 h-4 mr-2" />
          Sauvegarder
        </Button>
      </div>
    </div>
  );
};

const NotificationSettings = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Paramètres de notification</h2>
    <p className="text-gray-600">Contenu des paramètres de notification...</p>
  </div>
);

const SecuritySettings = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Paramètres de sécurité</h2>
    <p className="text-gray-600">Contenu des paramètres de sécurité...</p>
  </div>
);

const SchoolSettings = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Paramètres de l'établissement</h2>
    <p className="text-gray-600">Contenu des paramètres de l'établissement...</p>
  </div>
);

const PaymentSettings = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Paramètres de paiement</h2>
    <p className="text-gray-600">Contenu des paramètres de paiement...</p>
  </div>
);

const BackupSettings = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Sauvegarde et restauration</h2>
    <p className="text-gray-600">Contenu de la sauvegarde et restauration...</p>
  </div>
);

const NetworkSettings = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Paramètres réseau</h2>
    <p className="text-gray-600">Contenu des paramètres réseau...</p>
  </div>
);

const Settings = () => {
  return (
    <Routes>
      <Route path="/" element={<SettingsLayout />}>
        <Route path="profile" element={<ProfileSettings />} />
        <Route path="notifications" element={<NotificationSettings />} />
        <Route path="security" element={<SecuritySettings />} />
        <Route path="school" element={<SchoolSettings />} />
        <Route path="payments" element={<PaymentSettings />} />
        <Route path="backup" element={<BackupSettings />} />
        <Route path="network" element={<NetworkSettings />} />
        <Route path="" element={<Navigate to="profile" />} />
      </Route>
    </Routes>
  );
};

export default Settings;