// frontend/src/components/dashboard/StatCard.jsx
import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

const StatCard = ({ title, value, change, trend, icon: Icon, color }) => {
  const colorClasses = {
    blue: 'text-blue-500 bg-blue-100',
    green: 'text-green-500 bg-green-100',
    purple: 'text-purple-500 bg-purple-100',
    orange: 'text-orange-500 bg-orange-100',
  };

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-800 mt-1">{value}</p>
          <div className="flex items-center mt-2">
            {trend === 'up' ? (
              <TrendingUp className="w-4 h-4 text-green-500" />
            ) : (
              <TrendingDown className="w-4 h-4 text-red-500" />
            )}
            <span
              className={`ml-1 text-sm font-medium ${
                trend === 'up' ? 'text-green-500' : 'text-red-500'
              }`}
            >
              {change}
            </span>
            <span className="text-sm text-gray-500 ml-1">vs mois dernier</span>
          </div>
        </div>
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  );
};

export default StatCard;