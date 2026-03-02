// frontend/src/App.jsx
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { Toaster } from 'react-hot-toast';
import Layout from './components/layout/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Users from './pages/Users';
import Academics from './pages/Academics';
import Assessment from './pages/Assessment';
import Finance from './pages/Finance';
import Communication from './pages/Communication';
import Analytics from './pages/Analytics';
import Settings from './pages/Settings';

function App() {
  const { isAuthenticated } = useSelector((state) => state.auth);

  return (
    <div className="App">
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
        }}
      />
      
      <Routes>
        {/* Public Routes */}
        <Route 
          path="/login" 
          element={!isAuthenticated ? <Login /> : <Navigate to="/dashboard" />} 
        />
        <Route 
          path="/register" 
          element={!isAuthenticated ? <Register /> : <Navigate to="/dashboard" />} 
        />
        
        {/* Protected Routes */}
        <Route 
          path="/*" 
          element={isAuthenticated ? <Layout /> : <Navigate to="/login" />}
        >
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="users" element={<Users />} />
          <Route path="academics/*" element={<Academics />} />
          <Route path="assessment/*" element={<Assessment />} />
          <Route path="finance/*" element={<Finance />} />
          <Route path="communication/*" element={<Communication />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="settings" element={<Settings />} />
          <Route path="/extensions/*" element={<Extensions />} />
          <Route path="" element={<Navigate to="/dashboard" />} />
        </Route>
      </Routes>
    </div>
  );
}

export default App;