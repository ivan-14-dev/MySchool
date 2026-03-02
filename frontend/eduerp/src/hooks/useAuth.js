// frontend/src/hooks/useAuth.js
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { logout } from '../store/slices/authSlice';

export const useAuth = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { isAuthenticated, user } = useSelector((state) => state.auth);

  const checkAuth = () => {
    if (!isAuthenticated) {
      dispatch(logout());
      navigate('/login');
    }
  };

  useEffect(() => {
    checkAuth();
  }, [isAuthenticated]);

  return {
    isAuthenticated,
    user,
    checkAuth,
  };
};

export const useRole = (allowedRoles = []) => {
  const { user } = useSelector((state) => state.auth);
  
  if (!user || !allowedRoles.length) return false;
  
  return allowedRoles.includes(user.user_type);
};