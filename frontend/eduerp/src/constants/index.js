// frontend/src/constants/index.js
// User roles
export const USER_ROLES = {
  ADMIN: 'admin',
  TEACHER: 'teacher',
  STUDENT: 'student',
  PARENT: 'parent',
  STAFF: 'staff'
};

// User permissions
export const PERMISSIONS = {
  // Academics
  MANAGE_SUBJECTS: 'academics.manage_subjects',
  MANAGE_CLASSROOMS: 'academics.manage_classrooms',
  MANAGE_ACADEMIC_YEARS: 'academics.manage_academic_years',
  MANAGE_CLASS_GROUPS: 'academics.manage_class_groups',
  MANAGE_TIMETABLE: 'academics.manage_timetable',
  MANAGE_ENROLLMENTS: 'academics.manage_enrollments',

  // Assessment
  MANAGE_ASSESSMENTS: 'assessment.manage_assessments',
  MANAGE_GRADES: 'assessment.manage_grades',
  MANAGE_ATTENDANCE: 'assessment.manage_attendance',
  MANAGE_REPORT_CARDS: 'assessment.manage_report_cards',

  // Finance
  MANAGE_FEES: 'finance.manage_fees',
  MANAGE_INVOICES: 'finance.manage_invoices',
  MANAGE_PAYMENTS: 'finance.manage_payments',

  // Communication
  MANAGE_MESSAGES: 'communication.manage_messages',
  MANAGE_ANNOUNCEMENTS: 'communication.manage_announcements',
  MANAGE_NOTIFICATIONS: 'communication.manage_notifications',

  // Analytics
  VIEW_DASHBOARD: 'analytics.view_dashboard',
  VIEW_PERFORMANCE: 'analytics.view_performance',
  MANAGE_REPORTS: 'analytics.manage_reports'
};

// Assessment types
export const ASSESSMENT_TYPES = {
  EXAM: 'exam',
  TEST: 'test',
  QUIZ: 'quiz',
  PROJECT: 'project',
  HOMEWORK: 'homework'
};

// Grade scales
export const GRADE_SCALES = {
  NUMERIC: 'numeric',
  LETTER: 'letter',
  PERCENTAGE: 'percentage'
};

// Attendance status
export const ATTENDANCE_STATUS = {
  PRESENT: 'present',
  ABSENT: 'absent',
  LATE: 'late',
  EXCUSED: 'excused'
};

// Payment methods
export const PAYMENT_METHODS = {
  CASH: 'cash',
  CARD: 'card',
  TRANSFER: 'transfer',
  CHECK: 'check',
  MOBILE_MONEY: 'mobile_money'
};

// Payment status
export const PAYMENT_STATUS = {
  PENDING: 'pending',
  COMPLETED: 'completed',
  FAILED: 'failed',
  REFUNDED: 'refunded'
};

// Invoice status
export const INVOICE_STATUS = {
  DRAFT: 'draft',
  SENT: 'sent',
  PAID: 'paid',
  OVERDUE: 'overdue',
  CANCELLED: 'cancelled'
};

// Notification types
export const NOTIFICATION_TYPES = {
  INFO: 'info',
  SUCCESS: 'success',
  WARNING: 'warning',
  ERROR: 'error',
  SYSTEM: 'system'
};

// Date formats
export const DATE_FORMATS = {
  SHORT: 'DD/MM/YYYY',
  LONG: 'DD MMMM YYYY',
  TIME: 'HH:mm',
  DATETIME: 'DD/MM/YYYY HH:mm'
};

// Academic periods
export const ACADEMIC_PERIODS = {
  TERM1: 'term1',
  TERM2: 'term2',
  TERM3: 'term3',
  SEMESTER1: 'semester1',
  SEMESTER2: 'semester2',
  ANNUAL: 'annual'
};

// Class levels
export const CLASS_LEVELS = [
  '6ème', '5ème', '4ème', '3ème',
  '2nde', '1ère', 'Terminale',
  'CP', 'CE1', 'CE2', 'CM1', 'CM2'
];

// Subject categories
export const SUBJECT_CATEGORIES = {
  LANGUAGES: 'languages',
  SCIENCES: 'sciences',
  ARTS: 'arts',
  HUMANITIES: 'humanities',
  TECHNICAL: 'technical',
  PHYSICAL: 'physical'
};

// Export formats
export const EXPORT_FORMATS = {
  PDF: 'pdf',
  EXCEL: 'excel',
  CSV: 'csv'
};

// Theme colors
export const THEME_COLORS = {
  PRIMARY: '#3b82f6',
  SECONDARY: '#6b7280',
  SUCCESS: '#10b981',
  WARNING: '#f59e0b',
  ERROR: '#ef4444',
  INFO: '#06b6d4'
};

// Local storage keys
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'accessToken',
  REFRESH_TOKEN: 'refreshToken',
  USER_DATA: 'userData',
  SCHOOL_DATA: 'schoolData',
  THEME: 'theme'
};

// API endpoints
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login/',
    REGISTER: '/auth/register/',
    LOGOUT: '/auth/logout/',
    REFRESH: '/auth/token/refresh/'
  },
  USERS: '/users/',
  SUBJECTS: '/academics/subjects/',
  CLASSROOMS: '/academics/classrooms/',
  CLASS_GROUPS: '/academics/class-groups/',
  ASSESSMENTS: '/assessment/assessments/',
  ATTENDANCE: '/assessment/attendance/',
  FEES: '/finance/fees/',
  INVOICES: '/finance/invoices/',
  PAYMENTS: '/finance/payments/',
  NOTIFICATIONS: '/notifications/'
};