// frontend/src/components/finance/FeeManager.jsx
import React, { useState, useEffect } from 'react';
import { Plus, Download, Upload, Euro } from 'lucide-react';
import { feeService } from '../../services/api';
import Button from '../common/Button';
import DataTable from '../common/DataTable';
import FeeForm from './FeeForm';

const FeeManager = () => {
  const [fees, setFees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [selectedFee, setSelectedFee] = useState(null);

  useEffect(() => {
    loadFees();
  }, []);

  const loadFees = async () => {
    try {
      const response = await feeService.getFees();
      setFees(response.data);
    } catch (error) {
      console.error('Error loading fees:', error);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      name: 'Nom',
      selector: row => row.name,
      sortable: true,
    },
    {
      name: 'Montant',
      selector: row => row.amount,
      sortable: true,
      format: row => (
        <span className="font-semibold">
          {row.amount} €
        </span>
      )
    },
    {
      name: 'Périodicité',
      selector: row => row.frequency,
      sortable: true,
    },
    {
      name: 'Statut',
      selector: row => row.is_active,
      format: row => (
        <span className={`px-2 py-1 text-xs rounded-full ${
          row.is_active 
            ? 'bg-green-100 text-green-800' 
            : 'bg-gray-100 text-gray-800'
        }`}>
          {row.is_active ? 'Actif' : 'Inactif'}
        </span>
      )
    },
    {
      name: 'Actions',
      cell: row => (
        <div className="flex space-x-2">
          <Button variant="outline" size="sm">
            <Euro className="w-4 h-4" />
          </Button>
          <Button variant="outline" size="sm" onClick={() => handleEdit(row)}>
            Modifier
          </Button>
        </div>
      )
    }
  ];

  const handleCreate = () => {
    setSelectedFee(null);
    setShowForm(true);
  };

  const handleEdit = (fee) => {
    setSelectedFee(fee);
    setShowForm(true);
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-800">Gestion des frais scolaires</h2>
          <p className="text-gray-600">Configurez les frais et échéanciers</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline">
            <Upload className="w-4 h-4 mr-2" />
            Importer
          </Button>
          <Button variant="outline">
            <Download className="w-4 h-4 mr-2" />
            Exporter
          </Button>
          <Button onClick={handleCreate}>
            <Plus className="w-4 h-4 mr-2" />
            Nouveau frais
          </Button>
        </div>
      </div>

      <DataTable
        columns={columns}
        data={fees}
        loading={loading}
        pagination
        searchable
      />

      {showForm && (
        <FeeForm
          fee={selectedFee}
          onClose={() => {
            setShowForm(false);
            setSelectedFee(null);
          }}
          onSave={() => {
            setShowForm(false);
            setSelectedFee(null);
            loadFees();
          }}
        />
      )}
    </div>
  );
};

export default FeeManager;