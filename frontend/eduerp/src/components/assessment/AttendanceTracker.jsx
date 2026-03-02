// frontend/src/components/assessment/AttendanceTracker.jsx
import React, { useState } from 'react';
import { Calendar, Filter, Save } from 'lucide-react';
import Button from '../common/Button';

const AttendanceTracker = () => {
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [attendance, setAttendance] = useState({});

  const students = [
    { id: 1, name: 'Jean Dupont' },
    { id: 2, name: 'Marie Martin' },
    { id: 3, name: 'Pierre Durand' },
  ];

  const attendanceStatus = [
    { value: 'present', label: 'Présent', color: 'bg-green-100 text-green-800' },
    { value: 'absent', label: 'Absent', color: 'bg-red-100 text-red-800' },
    { value: 'late', label: 'Retard', color: 'bg-yellow-100 text-yellow-800' },
    { value: 'excused', label: 'Excusé', color: 'bg-blue-100 text-blue-800' },
  ];

  const handleAttendanceChange = (studentId, status) => {
    setAttendance(prev => ({
      ...prev,
      [studentId]: status
    }));
  };

  const saveAttendance = () => {
    // Logique de sauvegarde
    console.log('Attendance saved:', attendance);
  };

  return (
    <div className="bg-white rounded-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-800">Feuille de présence</h2>
          <p className="text-gray-600">Gestion de la présence des étudiants</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="relative">
            <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
          <Button variant="outline">
            <Filter className="w-4 h-4 mr-2" />
            Filtrer
          </Button>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-50">
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                Étudiant
              </th>
              {attendanceStatus.map(status => (
                <th key={status.value} className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">
                  {status.label}
                </th>
              ))}
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
                    <div className="text-sm font-medium text-gray-900">{student.name}</div>
                  </div>
                </td>
                {attendanceStatus.map(status => (
                  <td key={status.value} className="px-6 py-4 text-center">
                    <input
                      type="radio"
                      name={`attendance-${student.id}`}
                      checked={attendance[student.id] === status.value}
                      onChange={() => handleAttendanceChange(student.id, status.value)}
                      className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
                    />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="flex justify-end mt-6">
        <Button onClick={saveAttendance}>
          <Save className="w-4 h-4 mr-2" />
          Enregistrer la présence
        </Button>
      </div>
    </div>
  );
};

export default AttendanceTracker;