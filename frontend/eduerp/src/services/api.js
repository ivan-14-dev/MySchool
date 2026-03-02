// frontend/src/services/api.js (complet)
import axios from 'axios';
import { store } from '../store';
import { logout } from '../store/slices/authSlice';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshTokenValue = localStorage.getItem('refreshToken');
        if (refreshTokenValue) {
          const response = await axios.post(`${BASE_URL}/auth/token/refresh/`, {
            refresh: refreshTokenValue,
          });
          
          const { access } = response.data;
          localStorage.setItem('accessToken', access);
          originalRequest.headers.Authorization = `Bearer ${access}`;
          
          return api(originalRequest);
        }
      } catch (refreshError) {
        store.dispatch(logout());
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth services
export const authService = {
  login: (credentials) => api.post('/auth/login/', credentials),
  register: (userData) => api.post('/auth/register/', userData),
  logout: () => api.post('/auth/logout/'),
  refreshToken: () => api.post('/auth/token/refresh/'),
  verifyEmail: (token) => api.post('/auth/verify-email/', { token }),
  passwordReset: (email) => api.post('/auth/password-reset/', { email }),
  passwordResetConfirm: (data) => api.post('/auth/password-reset-confirm/', data),
  changePassword: (data) => api.post('/auth/change-password/', data),
};

// User services
export const userService = {
  getUsers: (params) => api.get('/users/users/', { params }),
  getUser: (id) => api.get(`/users/users/${id}/`),
  createUser: (data) => api.post('/users/users/', data),
  updateUser: (id, data) => api.patch(`/users/users/${id}/`, data),
  deleteUser: (id) => api.delete(`/users/users/${id}/`),
  getProfile: () => api.get('/users/users/me/'),
  updateProfile: (data) => api.patch('/users/users/me/', data),
};

// Academics services
export const academicsService = {
  getSubjects: (params) => api.get('/academics/subjects/', { params }),
  createSubject: (data) => api.post('/academics/subjects/', data),
  updateSubject: (id, data) => api.patch(`/academics/subjects/${id}/`, data),
  deleteSubject: (id) => api.delete(`/academics/subjects/${id}/`),
  
  getClassrooms: (params) => api.get('/academics/classrooms/', { params }),
  createClassroom: (data) => api.post('/academics/classrooms/', data),
  updateClassroom: (id, data) => api.patch(`/academics/classrooms/${id}/`, data),
  deleteClassroom: (id) => api.delete(`/academics/classrooms/${id}/`),
  
  getAcademicYears: (params) => api.get('/academics/academic-years/', { params }),
  createAcademicYear: (data) => api.post('/academics/academic-years/', data),
  updateAcademicYear: (id, data) => api.patch(`/academics/academic-years/${id}/`, data),
  deleteAcademicYear: (id) => api.delete(`/academics/academic-years/${id}/`),
  
  getClassGroups: (params) => api.get('/academics/class-groups/', { params }),
  createClassGroup: (data) => api.post('/academics/class-groups/', data),
  updateClassGroup: (id, data) => api.patch(`/academics/class-groups/${id}/`, data),
  deleteClassGroup: (id) => api.delete(`/academics/class-groups/${id}/`),
  
  getTimetables: (params) => api.get('/academics/timetables/', { params }),
  createTimetable: (data) => api.post('/academics/timetables/', data),
  updateTimetable: (id, data) => api.patch(`/academics/timetables/${id}/`, data),
  deleteTimetable: (id) => api.delete(`/academics/timetables/${id}/`),
  
  getEnrollments: (params) => api.get('/academics/enrollments/', { params }),
  createEnrollment: (data) => api.post('/academics/enrollments/', data),
  updateEnrollment: (id, data) => api.patch(`/academics/enrollments/${id}/`, data),
  deleteEnrollment: (id) => api.delete(`/academics/enrollments/${id}/`),
};

// Assessment services
export const assessmentService = {
  getAssessments: (params) => api.get('/assessment/assessments/', { params }),
  createAssessment: (data) => api.post('/assessment/assessments/', data),
  updateAssessment: (id, data) => api.patch(`/assessment/assessments/${id}/`, data),
  deleteAssessment: (id) => api.delete(`/assessment/assessments/${id}/`),
  
  getGrades: (params) => api.get('/assessment/grades/', { params }),
  createGrade: (data) => api.post('/assessment/grades/', data),
  updateGrade: (id, data) => api.patch(`/assessment/grades/${id}/`, data),
  deleteGrade: (id) => api.delete(`/assessment/grades/${id}/`),
  
  getAttendance: (params) => api.get('/assessment/attendance/', { params }),
  createAttendance: (data) => api.post('/assessment/attendance/', data),
  updateAttendance: (id, data) => api.patch(`/assessment/attendance/${id}/`, data),
  deleteAttendance: (id) => api.delete(`/assessment/attendance/${id}/`),
  
  getReportCards: (params) => api.get('/assessment/report-cards/', { params }),
  createReportCard: (data) => api.post('/assessment/report-cards/', data),
  updateReportCard: (id, data) => api.patch(`/assessment/report-cards/${id}/`, data),
  deleteReportCard: (id) => api.delete(`/assessment/report-cards/${id}/`),
};

// Finance services
export const financeService = {
  getFees: (params) => api.get('/finance/fees/', { params }),
  createFee: (data) => api.post('/finance/fees/', data),
  updateFee: (id, data) => api.patch(`/finance/fees/${id}/`, data),
  deleteFee: (id) => api.delete(`/finance/fees/${id}/`),
  
  getInvoices: (params) => api.get('/finance/invoices/', { params }),
  createInvoice: (data) => api.post('/finance/invoices/', data),
  updateInvoice: (id, data) => api.patch(`/finance/invoices/${id}/`, data),
  deleteInvoice: (id) => api.delete(`/finance/invoices/${id}/`),
  
  getPayments: (params) => api.get('/finance/payments/', { params }),
  createPayment: (data) => api.post('/finance/payments/', data),
  updatePayment: (id, data) => api.patch(`/finance/payments/${id}/`, data),
  deletePayment: (id) => api.delete(`/finance/payments/${id}/`),
};

// Communication services
export const messagingService = {
  getConversations: () => api.get('/communication/conversations/'),
  getMessages: (conversationId) => api.get(`/communication/conversations/${conversationId}/messages/`),
  sendMessage: (conversationId, data) => api.post(`/communication/conversations/${conversationId}/messages/`, data),
  markAsRead: (conversationId) => api.post(`/communication/conversations/${conversationId}/read/`),
};

export const notificationService = {
  getNotifications: () => api.get('/notifications/'),
  markAsRead: (id) => api.patch(`/notifications/${id}/read/`),
  markAllAsRead: () => api.post('/notifications/read-all/'),
  getUnreadCount: () => api.get('/notifications/unread-count/'),
};

// Analytics services
export const analyticsService = {
  getDashboardData: (params) => api.get('/analytics/dashboard/', { params }),
  getStudentPerformance: (studentId) => api.get(`/analytics/students/${studentId}/performance/`),
  getClassStatistics: (classId) => api.get(`/analytics/classes/${classId}/statistics/`),
  exportData: (format, params) => api.get(`/analytics/export/${format}/`, { 
    params,
    responseType: 'blob'
  }),
};

export default api;