// frontend/src/pages/Analytics.jsx
import React from 'react';
import {
  BarChart3,
  Users,
  TrendingUp,
  Award,
  Clock,
  BookOpen
} from 'lucide-react';
import StatCard from '../components/dashboard/StatCard.jsx';
import AttendanceChart from '../components/dashboard/AttendanceChart.jsx';

const Analytics = () => {
  const stats = [
    {
      title: 'Taux de réussite',
      value: '92%',
      change: '+5%',
      trend: 'up',
      icon: Award,
      color: 'green'
    },
    {
      title: 'Heures de cours',
      value: '1,248h',
      change: '+12%',
      trend: 'up',
      icon: Clock,
      color: 'blue'
    },
    {
      title: 'Moyenne générale',
      value: '14.2/20',
      change: '+0.8',
      trend: 'up',
      icon: TrendingUp,
      color: 'purple'
    },
    {
      title: 'Nouvelles inscriptions',
      value: '48',
      change: '+8%',
      trend: 'up',
      icon: Users,
      color: 'orange'
    }
  ];

  return (
    <div className="ml-64 p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Analytiques</h1>
        <p className="text-gray-600">
          Statistiques et analyses de votre établissement
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => (
          <StatCard key={index} {...stat} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Graphique de présence */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-800">Présence par matière</h2>
            <BarChart3 className="w-6 h-6 text-gray-400" />
          </div>
          <AttendanceChart />
        </div>

        {/* Performance par classe */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-800">Performance par classe</h2>
            <BookOpen className="w-6 h-6 text-gray-400" />
          </div>
          <div className="space-y-4">
            {[
              { class: '6ème A', average: 15.2, trend: 'up' },
              { class: '5ème B', average: 14.8, trend: 'up' },
              { class: '4ème C', average: 13.5, trend: 'stable' },
              { class: '3ème A', average: 12.9, trend: 'down' },
            ].map((item, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span className="font-medium">{item.class}</span>
                <div className="flex items-center space-x-2">
                  <span className="font-semibold">{item.average}/20</span>
                  {item.trend === 'up' && <TrendingUp className="w-4 h-4 text-green-500" />}
                  {item.trend === 'down' && <TrendingUp className="w-4 h-4 text-red-500 transform rotate-180" />}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Tableau de bord détaillé */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-6">Indicateurs détaillés</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            { title: 'Taux d\'absentéisme', value: '4.2%', change: '-1.2%' },
            { title: 'Notes supérieures à 16', value: '23%', change: '+3%' },
            { title: 'Retards mensuels', value: '12', change: '-4' },
            { title: 'Élèves en difficulté', value: '8%', change: '-2%' },
            { title: 'Taux de participation', value: '89%', change: '+5%' },
            { title: 'Satisfaction parents', value: '94%', change: '+2%' },
          ].map((item, index) => (
            <div key={index} className="p-4 bg-gray-50 rounded-lg">
              <h3 className="font-medium text-gray-700 mb-2">{item.title}</h3>
              <div className="flex items-baseline space-x-2">
                <span className="text-2xl font-bold text-gray-800">{item.value}</span>
                <span className={`text-sm ${
                  item.change.startsWith('+') ? 'text-green-500' : 
                  item.change.startsWith('-') ? 'text-red-500' : 'text-gray-500'
                }`}>
                  {item.change}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Analytics;