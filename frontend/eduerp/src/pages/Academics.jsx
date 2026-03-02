// frontend/src/pages/Academics.jsx
import React, { useState } from 'react';
import { Routes, Route, NavLink, Outlet } from 'react-router-dom';
import { 
  BookOpen, 
  Users, 
  Clock, 
  Building, 
  Plus,
  Search,
  Filter
} from 'lucide-react';
import Button from '../components/common/Button';

const AcademicsLayout = () => {
  const navigation = [
    {
      name: 'Matières',
      href: '/academics/subjects',
      icon: BookOpen,
      permission: 'academics.manage_subjects'
    },
    {
      name: 'Classes',
      href: '/academics/classes',
      icon: Users,
      permission: 'academics.manage_class_groups'
    },
    {
      name: 'Emploi du temps',
      href: '/academics/timetable',
      icon: Clock,
      permission: 'academics.manage_timetable'
    },
    {
      name: 'Salles',
      href: '/academics/classrooms',
      icon: Building,
      permission: 'academics.manage_classrooms'
    },
  ];

  return (
    <div className="ml-64 p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Gestion académique</h1>
        <p className="text-gray-600">Gérez les aspects académiques de votre établissement</p>
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

// Composants pour chaque sous-page
const Subjects = () => {
  const [filters, setFilters] = useState({
    search: '',
    department: '',
    is_active: ''
  });

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-800">Gestion des matières</h2>
          <p className="text-gray-600">Créez et gérez les matières enseignées</p>
        </div>
        <Button>
          <Plus className="w-4 h-4 mr-2" />
          Nouvelle matière
        </Button>
      </div>

      {/* Filtres */}
      <div className="bg-gray-50 rounded-lg p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Recherche</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Rechercher une matière..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                value={filters.search}
                onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Département</label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              value={filters.department}
              onChange={(e) => setFilters({ ...filters, department: e.target.value })}
            >
              <option value="">Tous les départements</option>
              <option value="math">Mathématiques</option>
              <option value="science">Sciences</option>
              <option value="language">Langues</option>
              <option value="arts">Arts</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Statut</label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              value={filters.is_active}
              onChange={(e) => setFilters({ ...filters, is_active: e.target.value })}
            >
              <option value="">Tous</option>
              <option value="true">Actif</option>
              <option value="false">Inactif</option>
            </select>
          </div>

          <div className="flex items-end">
            <Button
              variant="outline"
              className="w-full"
              onClick={() => setFilters({ search: '', department: '', is_active: '' })}
            >
              <Filter className="w-4 h-4 mr-2" />
              Réinitialiser
            </Button>
          </div>
        </div>
      </div>

      {/* Tableau des matières */}
      <div className="bg-white rounded-lg border border-gray-200">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nom</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Code</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Département</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Crédits</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Statut</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {[].map((subject, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                        <BookOpen className="w-4 h-4 text-blue-600" />
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">{subject.name}</div>
                        <div className="text-sm text-gray-500">{subject.description}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{subject.code}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{subject.department}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{subject.credits}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      subject.is_active 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {subject.is_active ? 'Actif' : 'Inactif'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm">Modifier</Button>
                      <Button variant="danger" size="sm">Supprimer</Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {[].length === 0 && (
          <div className="text-center py-12">
            <BookOpen className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Aucune matière</h3>
            <p className="text-gray-500 mb-4">Commencez par créer votre première matière.</p>
            <Button>
              <Plus className="w-4 h-4 mr-2" />
              Créer une matière
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

const Classes = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Gestion des classes</h2>
    <p className="text-gray-600">Contenu de la gestion des classes...</p>
  </div>
);

const Timetable = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Emploi du temps</h2>
    <p className="text-gray-600">Contenu de l'emploi du temps...</p>
  </div>
);

const Classrooms = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Gestion des salles</h2>
    <p className="text-gray-600">Contenu de la gestion des salles...</p>
  </div>
);

const Academics = () => {
  return (
    <Routes>
      <Route path="/" element={<AcademicsLayout />}>
        <Route path="subjects" element={<Subjects />} />
        <Route path="classes" element={<Classes />} />
        <Route path="timetable" element={<Timetable />} />
        <Route path="classrooms" element={<Classrooms />} />
        <Route path="" element={<Navigate to="subjects" />} />
      </Route>
    </Routes>
  );
};

export default Academics;