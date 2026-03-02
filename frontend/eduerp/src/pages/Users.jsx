// frontend/src/pages/Users.jsx
import React, { useState, useEffect } from 'react';
import { Plus, Search, Filter, Edit, Trash2, Eye, Download, Upload } from 'lucide-react';
import { useSelector } from 'react-redux';
import { userService } from '../services/api';
import DataTable from '../components/common/DataTable';
import Button from '../components/common/Button';
import UserForm from '../components/users/UserForm';
import { toast } from 'react-hot-toast';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [filters, setFilters] = useState({
    search: '',
    user_type: '',
    is_active: ''
  });

  const { user: currentUser } = useSelector((state) => state.auth);

  useEffect(() => {
    loadUsers();
  }, [filters]);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const params = {};
      if (filters.search) params.search = filters.search;
      if (filters.user_type) params.user_type = filters.user_type;
      if (filters.is_active) params.is_active = filters.is_active;

      const response = await userService.getUsers(params);
      setUsers(response.data.results || response.data);
    } catch (error) {
      toast.error('Erreur lors du chargement des utilisateurs');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    setSelectedUser(null);
    setShowForm(true);
  };

  const handleEdit = (user) => {
    setSelectedUser(user);
    setShowForm(true);
  };

  const handleDelete = async (user) => {
    if (!window.confirm(`Êtes-vous sûr de vouloir supprimer ${user.first_name} ${user.last_name} ?`)) {
      return;
    }

    try {
      await userService.deleteUser(user.id);
      toast.success('Utilisateur supprimé avec succès');
      loadUsers();
    } catch (error) {
      toast.error('Erreur lors de la suppression');
    }
  };

  const columns = [
    {
      name: 'Nom',
      selector: row => `${row.first_name} ${row.last_name}`,
      sortable: true,
    },
    {
      name: 'Email',
      selector: row => row.email,
      sortable: true,
    },
    {
      name: 'Type',
      selector: row => row.user_type,
      sortable: true,
      format: row => (
        <span className="capitalize px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
          {row.user_type}
        </span>
      )
    },
    {
      name: 'Statut',
      selector: row => row.is_active,
      sortable: true,
      format: row => (
        <span className={`px-2 py-1 text-xs rounded-full ${
          row.is_active 
            ? 'bg-green-100 text-green-800' 
            : 'bg-red-100 text-red-800'
        }`}>
          {row.is_active ? 'Actif' : 'Inactif'}
        </span>
      )
    },
    {
      name: 'Actions',
      cell: row => (
        <div className="flex space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => handleEdit(row)}
          >
            <Edit className="w-4 h-4" />
          </Button>
          <Button
            variant="danger"
            size="sm"
            onClick={() => handleDelete(row)}
            disabled={row.id === currentUser.id}
          >
            <Trash2 className="w-4 h-4" />
          </Button>
        </div>
      )
    }
  ];

  return (
    <div className="ml-64 p-6">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Gestion des utilisateurs</h1>
          <p className="text-gray-600">Gérez les utilisateurs de votre établissement</p>
        </div>
        <Button onClick={handleCreate}>
          <Plus className="w-4 h-4 mr-2" />
          Nouvel utilisateur
        </Button>
      </div>

      {/* Filtres */}
      <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Recherche</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Rechercher..."
                className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                value={filters.search}
                onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Type</label>
            <select
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              value={filters.user_type}
              onChange={(e) => setFilters({ ...filters, user_type: e.target.value })}
            >
              <option value="">Tous</option>
              <option value="admin">Administrateur</option>
              <option value="teacher">Enseignant</option>
              <option value="student">Étudiant</option>
              <option value="parent">Parent</option>
              <option value="staff">Staff</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Statut</label>
            <select
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
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
              onClick={() => setFilters({ search: '', user_type: '', is_active: '' })}
            >
              <Filter className="w-4 h-4 mr-2" />
              Réinitialiser
            </Button>
          </div>
        </div>
      </div>

      {/* Tableau */}
      <div className="bg-white rounded-lg shadow-sm">
        <DataTable
          columns={columns}
          data={users}
          loading={loading}
          pagination
          searchable
        />
      </div>

      {/* Modal de formulaire */}
      {showForm && (
        <UserForm
          user={selectedUser}
          onClose={() => {
            setShowForm(false);
            setSelectedUser(null);
          }}
          onSave={() => {
            setShowForm(false);
            setSelectedUser(null);
            loadUsers();
          }}
        />
      )}
    </div>
  );
};

export default Users;