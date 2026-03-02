// frontend/src/utils/permissions.js
export const PERMISSIONS = {
  // Users
  USER_CREATE: 'users.create',
  USER_READ: 'users.read',
  USER_UPDATE: 'users.update',
  USER_DELETE: 'users.delete',
  
  // Academics
  SUBJECT_MANAGE: 'academics.subjects.manage',
  CLASS_MANAGE: 'academics.classes.manage',
  
  // Financial
  PAYMENT_VIEW: 'finance.payments.view',
  PAYMENT_MANAGE: 'finance.payments.manage',
};

export const hasPermission = (user, permission) => {
  return user?.permissions?.includes(permission) || user?.is_superuser;
};

export const hasRole = (user, roles) => {
  return roles.includes(user?.user_type);
};