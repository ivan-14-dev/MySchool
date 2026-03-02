// frontend/src/pages/Dashboard.jsx
import React from 'react';
import { useSelector } from 'react-redux';
import {
  Users,
  BookOpen,
  GraduationCap,
  CreditCard,
  Calendar,
  BarChart3,
  TrendingUp,
  AlertCircle
} from 'lucide-react';
import StatCard from '../components/dashboard/StatCard';
import RecentActivity from '../components/dashboard/RecentActivity';
import AttendanceChart from '../components/dashboard/AttendanceChart';
import UpcomingEvents from '../components/dashboard/UpcomingEvents';

const Dashboard = () => {
  const { user } = useSelector((state) => state.auth);

  // Données factices pour la démo
  const stats = [
    {
      title: 'Étudiants',
      value: '1,248',
      change: '+12%',
      trend: 'up',
      icon: Users,
      color: 'blue'
    },
    {
      title: 'Enseignants',
      value: '48',
      change: '+4%',
      trend: 'up',
      icon: GraduationCap,
      color: 'green'
    },
    {
      title: 'Cours',
      value: '156',
      change: '+8%',
      trend: 'up',
      icon: BookOpen,
      color: 'purple'
    },
    {
      title: 'Revenus',
      value: '€45,236',
      change: '+23%',
      trend: 'up',
      icon: CreditCard,
      color: 'orange'
    }
  ];

  const recentActivities = [
    {
      id: 1,
      type: 'grade',
      title: 'Nouvelle note ajoutée',
      description: 'Mathématiques - Contrôle de géométrie',
      time: '2 minutes ago',
      icon: TrendingUp
    },
    {
      id: 2,
      type: 'attendance',
      title: 'Absence signalée',
      description: 'Jean Dupret - Cours de physique',
      time: '1 heure ago',
      icon: AlertCircle
    },
    {
      id: 3,
      type: 'payment',
      title: 'Paiement reçu',
      description: 'Famille Martin - Frais de scolarité',
      time: '3 heures ago',
      icon: CreditCard
    },
    {
      id: 4,
      type: 'event',
      title: 'Nouvel événement',
      description: 'Réunion parents-professeurs',
      time: '5 heures ago',
      icon: Calendar
    }
  ];

  return (
    <div className="ml-64 p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">
          Bonjour, {user?.first_name} 👋
        </h1>
        <p className="text-gray-600">
          Voici un résumé de votre établissement aujourd'hui
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat, index) => (
          <StatCard key={index} {...stat} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Graphique de présence */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-800">Présence mensuelle</h2>
              <BarChart3 className="w-6 h-6 text-gray-400" />
            </div>
            <AttendanceChart />
          </div>
        </div>

        {/* Événements à venir */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-800">Événements à venir</h2>
            <Calendar className="w-6 h-6 text-gray-400" />
          </div>
          <UpcomingEvents />
        </div>
      </div>

      {/* Activité récente */}
      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-gray-800">Activité récente</h2>
        </div>
        <RecentActivity activities={recentActivities} />
      </div>
    </div>
  );
};

export default Dashboard;