// frontend/src/contexts/SchoolContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { schoolService } from '../services/api';

const SchoolContext = createContext();

export const useSchool = () => {
  const context = useContext(SchoolContext);
  if (!context) {
    throw new Error('useSchool must be used within a SchoolProvider');
  }
  return context;
};

export const SchoolProvider = ({ children }) => {
  const [currentSchool, setCurrentSchool] = useState(null);
  const [schools, setSchools] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSchools();
  }, []);

  const loadSchools = async () => {
    try {
      const response = await schoolService.getSchools();
      setSchools(response.data);
      
      // Set default school or remember last selection
      const savedSchoolId = localStorage.getItem('currentSchoolId');
      const defaultSchool = savedSchoolId 
        ? response.data.find(s => s.id === savedSchoolId)
        : response.data[0];
      
      if (defaultSchool) {
        setCurrentSchool(defaultSchool);
      }
    } catch (error) {
      console.error('Error loading schools:', error);
    } finally {
      setLoading(false);
    }
  };

  const switchSchool = (schoolId) => {
    const school = schools.find(s => s.id === schoolId);
    if (school) {
      setCurrentSchool(school);
      localStorage.setItem('currentSchoolId', schoolId);
    }
  };

  const value = {
    currentSchool,
    schools,
    loading,
    switchSchool,
    refreshSchools: loadSchools
  };

  return (
    <SchoolContext.Provider value={value}>
      {children}
    </SchoolContext.Provider>
  );
};