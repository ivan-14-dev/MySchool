// frontend/src/pages/Assessment.jsx
import React, { useState } from 'react';
import { Routes, Route, NavLink, Outlet } from 'react-router-dom';
import { 
  ClipboardList, 
  FileText, 
  Calendar, 
  TrendingUp,
  Plus,
  Download,
  Upload
} from 'lucide-react';
import Button from '../components/common/Button';

const AssessmentLayout = () => {
  const navigation = [
    {
      name: 'Notes',
      href: '/assessment/grades',
      icon: ClipboardList,
    },
    {
      name: 'Bulletins',
      href: '/assessment/reports',
      icon: FileText,
    },
    {
      name: 'Présence',
      href: '/assessment/attendance',
      icon: Calendar,
    },
    {
      name: 'Statistiques',
      href: '/assessment/statistics',
      icon: TrendingUp,
    },
  ];

  return (
    <div className="ml-64 p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Évaluation</h1>
        <p className="text-gray-600">Gérez les évaluations et résultats des étudiants</p>
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

const Grades = () => {
  const [selectedClass, setSelectedClass] = useState('');
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedAssessment, setSelectedAssessment] = useState('');

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-800">Gestion des notes</h2>
          <p className="text-gray-600">Saisissez et consultez les notes des étudiants</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline">
            <Download className="w-4 h-4 mr-2" />
            Exporter
          </Button>
          <Button variant="outline">
            <Upload className="w-4 h-4 mr-2" />
            Importer
          </Button>
          <Button>
            <Plus className="w-4 h-4 mr-2" />
            Nouvelle évaluation
          </Button>
        </div>
      </div>

      {/* Filtres */}
      <div className="bg-gray-50 rounded-lg p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Classe</label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              value={selectedClass}
              onChange={(e) => setSelectedClass(e.target.value)}
            >
              <option value="">Sélectionner une classe</option>
              <option value="6A">6ème A</option>
              <option value="6B">6ème B</option>
              <option value="5A">5ème A</option>
              <option value="5B">5ème B</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Matière</label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              value={selectedSubject}
              onChange={(e) => setSelectedSubject(e.target.value)}
            >
              <option value="">Sélectionner une matière</option>
              <option value="math">Mathématiques</option>
              <option value="french">Français</option>
              <option value="science">Sciences</option>
              <option value="history">Histoire</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Évaluation</label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              value={selectedAssessment}
              onChange={(e) => setSelectedAssessment(e.target.value)}
            >
              <option value="">Sélectionner une évaluation</option>
              <option value="test1">Contrôle n°1</option>
              <option value="test2">Contrôle n°2</option>
              <option value="exam">Examen trimestriel</option>
            </select>
          </div>
        </div>
      </div>

      {/* Tableau des notes */}
      <div className="bg-white rounded-lg border border-gray-200">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Étudiant</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Note</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Sur</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">%</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Appréciation</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {[].map((student, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center mr-3">
                        <span className="text-sm font-medium text-gray-600">
                          {student.name[0]}
                        </span>
                      </div>
                      <div>
                        <div className="text-sm font-medium text-gray-900">{student.name}</div>
                        <div className="text-sm text-gray-500">#{student.id}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="text-sm font-medium text-gray-900">{student.grade}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">20</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                      student.percentage >= 80 ? 'bg-green-100 text-green-800' :
                      student.percentage >= 50 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {student.percentage}%
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {student.appreciation}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <Button variant="outline" size="sm">Modifier</Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {[].length === 0 && (
          <div className="text-center py-12">
            <ClipboardList className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Aucune note</h3>
            <p className="text-gray-500">Sélectionnez une classe, une matière et une évaluation pour afficher les notes.</p>
          </div>
        )}
      </div>
    </div>
  );
};

const Reports = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Bulletins scolaires</h2>
    <p className="text-gray-600">Contenu des bulletins scolaires...</p>
  </div>
);

const Attendance = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Gestion de la présence</h2>
    <p className="text-gray-600">Contenu de la gestion de la présence...</p>
  </div>
);

const Statistics = () => (
  <div className="p-6">
    <h2 className="text-xl font-semibold text-gray-800 mb-4">Statistiques d'évaluation</h2>
    <p className="text-gray-600">Contenu des statistiques...</p>
  </div>
);

const Assessment = () => {
  return (
    <Routes>
      <Route path="/" element={<AssessmentLayout />}>
        <Route path="grades" element={<Grades />} />
        <Route path="reports" element={<Reports />} />
        <Route path="attendance" element={<Attendance />} />
        <Route path="statistics" element={<Statistics />} />
        <Route path="" element={<Navigate to="grades" />} />
      </Route>
    </Routes>
  );
};

export default Assessment;