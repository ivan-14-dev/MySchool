// frontend/src/components/analytics/AdvancedDashboard.jsx
import React, { useState } from 'react';
import {
  BarChart3,
  Users,
  TrendingUp,
  Award,
  Clock,
  BookOpen,
  Filter
} from 'lucide-react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Line, Doughnut } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const AdvancedDashboard = () => {
  const [timeRange, setTimeRange] = useState('month');
  const [selectedClass, setSelectedClass] = useState('all');

  const performanceData = {
    labels: ['6ème A', '6ème B', '5ème A', '5ème B', '4ème A', '4ème B', '3ème A', '3ème B'],
    datasets: [
      {
        label: 'Moyenne générale',
        data: [14.2, 13.8, 15.1, 14.5, 13.2, 12.8, 14.9, 13.7],
        backgroundColor: 'rgba(59, 130, 246, 0.6)',
        borderColor: 'rgb(59, 130, 246)',
        borderWidth: 1,
      },
    ],
  };

  const attendanceData = {
    labels: ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'],
    datasets: [
      {
        label: 'Présence',
        data: [95, 92, 97, 94, 89, 45],
        backgroundColor: 'rgba(34, 197, 94, 0.6)',
        borderColor: 'rgb(34, 197, 94)',
        borderWidth: 1,
      },
      {
        label: 'Absence',
        data: [5, 8, 3, 6, 11, 55],
        backgroundColor: 'rgba(239, 68, 68, 0.6)',
        borderColor: 'rgb(239, 68, 68)',
        borderWidth: 1,
      },
    ],
  };

  const gradeDistributionData = {
    labels: ['0-5', '5-10', '10-12', '12-14', '14-16', '16-20'],
    datasets: [
      {
        label: 'Nombre d\'élèves',
        data: [2, 8, 15, 32, 28, 15],
        backgroundColor: [
          'rgba(239, 68, 68, 0.8)',
          'rgba(249, 115, 22, 0.8)',
          'rgba(234, 179, 8, 0.8)',
          'rgba(132, 204, 22, 0.8)',
          'rgba(34, 197, 94, 0.8)',
          'rgba(21, 128, 61, 0.8)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
    },
  };

  return (
    <div className="space-y-6">
      {/* Filtres */}
      <div className="bg-white rounded-lg p-4 shadow-sm">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-800">Filtres analytiques</h3>
          <div className="flex items-center space-x-4">
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg"
            >
              <option value="week">Cette semaine</option>
              <option value="month">Ce mois</option>
              <option value="quarter">Ce trimestre</option>
              <option value="year">Cette année</option>
            </select>
            <select
              value={selectedClass}
              onChange={(e) => setSelectedClass(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg"
            >
              <option value="all">Toutes les classes</option>
              <option value="6A">6ème A</option>
              <option value="6B">6ème B</option>
              <option value="5A">5ème A</option>
              <option value="5B">5ème B</option>
            </select>
            <Button variant="outline">
              <Filter className="w-4 h-4 mr-2" />
              Appliquer
            </Button>
          </div>
        </div>
      </div>

      {/* Grille de graphiques */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Performance par classe */}
        <div className="bg-white rounded-lg p-6 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-800">Performance par classe</h3>
            <BarChart3 className="w-5 h-5 text-gray-400" />
          </div>
          <Bar data={performanceData} options={chartOptions} height={250} />
        </div>

        {/* Tendance des résultats */}
        <div className="bg-white rounded-lg p-6 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-800">Évolution des résultats</h3>
            <TrendingUp className="w-5 h-5 text-gray-400" />
          </div>
          <Line 
            data={{
              labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'],
              datasets: [
                {
                  label: 'Moyenne générale',
                  data: [12.8, 13.2, 13.8, 14.1, 14.5, 14.9],
                  borderColor: 'rgb(59, 130, 246)',
                  backgroundColor: 'rgba(59, 130, 246, 0.1)',
                  tension: 0.3,
                },
              ],
            }} 
            options={chartOptions} 
            height={250} 
          />
        </div>

        {/* Distribution des notes */}
        <div className="bg-white rounded-lg p-6 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-800">Distribution des notes</h3>
            <Award className="w-5 h-5 text-gray-400" />
          </div>
          <Doughnut data={gradeDistributionData} options={chartOptions} height={250} />
        </div>

        {/* Présence par jour */}
        <div className="bg-white rounded-lg p-6 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-800">Présence par jour</h3>
            <Clock className="w-5 h-5 text-gray-400" />
          </div>
          <Bar data={attendanceData} options={chartOptions} height={250} />
        </div>
      </div>

      {/* Indicateurs de performance */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { title: 'Taux de réussite', value: '92%', change: '+5%', icon: Award, color: 'green' },
          { title: 'Absentéisme moyen', value: '4.2%', change: '-1.2%', icon: Clock, color: 'blue' },
          { title: 'Satisfaction parents', value: '94%', change: '+2%', icon: Users, color: 'purple' },
          { title: 'Taux d\'encadrement', value: '1:15', change: 'Stable', icon: BookOpen, color: 'orange' },
        ].map((item, index) => {
          const Icon = item.icon;
          return (
            <div key={index} className="bg-white rounded-lg p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <Icon className={`w-8 h-8 text-${item.color}-500`} />
                <span className={`text-sm font-medium ${
                  item.change.startsWith('+') ? 'text-green-500' :
                  item.change.startsWith('-') ? 'text-red-500' : 'text-gray-500'
                }`}>
                  {item.change}
                </span>
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-2">{item.value}</h3>
              <p className="text-sm text-gray-600">{item.title}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default AdvancedDashboard;