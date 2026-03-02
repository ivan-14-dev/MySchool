// frontend/src/components/analytics/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import {
  BarChart3,
  Users,
  TrendingUp,
  Award,
  Clock,
  BookOpen,
  Filter,
  Download
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
import { Bar, Line, Doughnut, Pie } from 'react-chartjs-2';
import { analyticsService } from '../../services/api';
import Button from '../common/Button';

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

const AnalyticsDashboard = () => {
  const [timeRange, setTimeRange] = useState('month');
  const [selectedClass, setSelectedClass] = useState('all');
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalyticsData();
  }, [timeRange, selectedClass]);

  const loadAnalyticsData = async () => {
    try {
      setLoading(true);
      const response = await analyticsService.getDashboardData({
        time_range: timeRange,
        class_level: selectedClass
      });
      setData(response.data);
    } catch (error) {
      console.error('Error loading analytics data:', error);
    } finally {
      setLoading(false);
    }
  };

  const performanceData = {
    labels: data.performance?.labels || [],
    datasets: [
      {
        label: 'Moyenne générale',
        data: data.performance?.values || [],
        backgroundColor: 'rgba(59, 130, 246, 0.6)',
        borderColor: 'rgb(59, 130, 246)',
        borderWidth: 1,
      },
    ],
  };

  const attendanceData = {
    labels: data.attendance?.labels || [],
    datasets: [
      {
        label: 'Présence',
        data: data.attendance?.present || [],
        backgroundColor: 'rgba(34, 197, 94, 0.6)',
        borderColor: 'rgb(34, 197, 94)',
        borderWidth: 1,
      },
      {
        label: 'Absence',
        data: data.attendance?.absent || [],
        backgroundColor: 'rgba(239, 68, 68, 0.6)',
        borderColor: 'rgb(239, 68, 68)',
        borderWidth: 1,
      },
    ],
  };

  const gradeDistributionData = {
    labels: data.grade_distribution?.labels || [],
    datasets: [
      {
        label: 'Nombre d\'élèves',
        data: data.grade_distribution?.values || [],
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
    maintainAspectRatio: false,
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Filtres et en-tête */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Analytiques avancées</h1>
          <p className="text-gray-600">Données et statistiques de votre établissement</p>
        </div>
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
            <option value="6eme">6ème</option>
            <option value="5eme">5ème</option>
            <option value="4eme">4ème</option>
            <option value="3eme">3ème</option>
          </select>
          <Button variant="outline">
            <Download className="w-4 h-4 mr-2" />
            Exporter
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {data.kpis?.map((kpi, index) => (
          <div key={index} className="bg-white rounded-lg p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <kpi.icon className={`w-8 h-8 text-${kpi.color}-500`} />
              <span className={`text-sm font-medium ${
                kpi.trend.startsWith('+') ? 'text-green-500' :
                kpi.trend.startsWith('-') ? 'text-red-500' : 'text-gray-500'
              }`}>
                {kpi.trend}
              </span>
            </div>
            <h3 className="text-2xl font-bold text-gray-800 mb-2">{kpi.value}</h3>
            <p className="text-sm text-gray-600">{kpi.title}</p>
          </div>
        ))}
      </div>

      {/* Grille de graphiques */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Performance par classe */}
        <div className="bg-white rounded-lg p-6 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-800">Performance par classe</h3>
            <BarChart3 className="w-5 h-5 text-gray-400" />
          </div>
          <div className="h-64">
            <Bar data={performanceData} options={chartOptions} />
          </div>
        </div>

        {/* Évolution des résultats */}
        <div className="bg-white rounded-lg p-6 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-800">Évolution des résultats</h3>
            <TrendingUp className="w-5 h-5 text-gray-400" />
          </div>
          <div className="h-64">
            <Line 
              data={{
                labels: data.trends?.labels || [],
                datasets: [
                  {
                    label: 'Moyenne générale',
                    data: data.trends?.values || [],
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.3,
                  },
                ],
              }} 
              options={chartOptions} 
            />
          </div>
        </div>

        {/* Distribution des notes */}
        <div className="bg-white rounded-lg p-6 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-800">Distribution des notes</h3>
            <Award className="w-5 h-5 text-gray-400" />
          </div>
          <div className="h-64">
            <Doughnut data={gradeDistributionData} options={chartOptions} />
          </div>
        </div>

        {/* Présence par jour */}
        <div className="bg-white rounded-lg p-6 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-800">Présence par jour</h3>
            <Clock className="w-5 h-5 text-gray-400" />
          </div>
          <div className="h-64">
            <Bar data={attendanceData} options={chartOptions} />
          </div>
        </div>
      </div>

      {/* Tableaux de données détaillées */}
      <div className="bg-white rounded-lg shadow-sm">
        <div className="p-6 border-b">
          <h3 className="text-lg font-semibold text-gray-800">Détails par matière</h3>
        </div>
        <div className="p-6">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-gray-50">
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Matière</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Moyenne</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Évolution</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Taux de réussite</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {data.subjects?.map((subject, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-800">
                      {subject.name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-800">
                      {subject.average}/20
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span className={`inline-flex items-center ${
                        subject.trend.startsWith('+') ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {subject.trend.startsWith('+') ? '↗' : '↘'}
                        {subject.trend}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-800">
                      {subject.success_rate}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;