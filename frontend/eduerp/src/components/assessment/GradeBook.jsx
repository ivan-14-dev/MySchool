// frontend/src/components/assessment/GradeBook.jsx
import React, { useState, useEffect } from 'react';
import { Download, Upload, Filter, Plus, Edit, Save, X } from 'lucide-react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchAssessments, fetchGrades } from '../../store/slices/assessmentSlice';
import Button from '../common/Button';
import { toast } from 'react-hot-toast';

const GradeBook = () => {
  const dispatch = useDispatch();
  const { assessments, grades } = useSelector((state) => state.assessment);
  const [selectedClass, setSelectedClass] = useState('');
  const [selectedSubject, setSelectedSubject] = useState('');
  const [editing, setEditing] = useState(null);
  const [newGrades, setNewGrades] = useState({});

  useEffect(() => {
    dispatch(fetchAssessments());
    dispatch(fetchGrades());
  }, [dispatch]);

  const students = [
    { id: 1, name: 'Jean Dupont', class: '6A' },
    { id: 2, name: 'Marie Martin', class: '6A' },
    { id: 3, name: 'Pierre Durand', class: '6A' },
  ];

  const handleGradeChange = (studentId, assessmentId, value) => {
    setNewGrades(prev => ({
      ...prev,
      [`${studentId}-${assessmentId}`]: value
    }));
  };

  const saveGrades = () => {
    // Logique de sauvegarde des notes
    toast.success('Notes sauvegardées avec succès');
    setEditing(null);
  };

  return (
    <div className="bg-white rounded-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-800">Carnet de notes</h2>
          <p className="text-gray-600">Gestion des notes des étudiants</p>
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
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              value={selectedClass}
              onChange={(e) => setSelectedClass(e.target.value)}
            >
              <option value="">Toutes les classes</option>
              <option value="6A">6ème A</option>
              <option value="6B">6ème B</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Matière</label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              value={selectedSubject}
              onChange={(e) => setSelectedSubject(e.target.value)}
            >
              <option value="">Toutes les matières</option>
              <option value="math">Mathématiques</option>
              <option value="french">Français</option>
            </select>
          </div>
          <div className="flex items-end">
            <Button variant="outline" className="w-full">
              <Filter className="w-4 h-4 mr-2" />
              Filtrer
            </Button>
          </div>
        </div>
      </div>

      {/* Tableau des notes */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-50">
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Étudiant
              </th>
              {assessments.map(assessment => (
                <th key={assessment.id} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  {assessment.name}
                  <div className="text-xs text-gray-400">/{assessment.maximum_marks}</div>
                </th>
              ))}
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Moyenne
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {students.map(student => (
              <tr key={student.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center mr-3">
                      <span className="text-sm font-medium text-gray-600">
                        {student.name[0]}
                      </span>
                    </div>
                    <div>
                      <div className="text-sm font-medium text-gray-900">{student.name}</div>
                      <div className="text-sm text-gray-500">{student.class}</div>
                    </div>
                  </div>
                </td>
                {assessments.map(assessment => {
                  const grade = grades.find(g => g.student === student.id && g.assessment === assessment.id);
                  const editingKey = `${student.id}-${assessment.id}`;
                  
                  return (
                    <td key={assessment.id} className="px-6 py-4 whitespace-nowrap">
                      {editing === editingKey ? (
                        <input
                          type="number"
                          step="0.5"
                          min="0"
                          max={assessment.maximum_marks}
                          value={newGrades[editingKey] || grade?.marks_obtained || ''}
                          onChange={(e) => handleGradeChange(student.id, assessment.id, e.target.value)}
                          className="w-16 px-2 py-1 border border-gray-300 rounded text-sm"
                        />
                      ) : (
                        <span className="text-sm font-medium text-gray-900">
                          {grade?.marks_obtained || '-'}
                        </span>
                      )}
                    </td>
                  );
                })}
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="text-sm font-medium text-gray-900">
                    14.5/20
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Actions */}
      <div className="flex justify-end space-x-3 mt-6">
        {editing ? (
          <>
            <Button variant="outline" onClick={() => setEditing(null)}>
              <X className="w-4 h-4 mr-2" />
              Annuler
            </Button>
            <Button onClick={saveGrades}>
              <Save className="w-4 h-4 mr-2" />
              Sauvegarder
            </Button>
          </>
        ) : (
          <Button onClick={() => setEditing('all')}>
            <Edit className="w-4 h-4 mr-2" />
            Modifier les notes
          </Button>
        )}
      </div>
    </div>
  );
};

export default GradeBook;