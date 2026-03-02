// frontend/src/store/index.js (mise à jour)
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import userReducer from './slices/userSlice';
import academicsReducer from './slices/academicsSlice';
import assessmentReducer from './slices/assessmentSlice';
import financeReducer from './slices/financeSlice';
import communicationReducer from './slices/communicationSlice';
import uiReducer from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    user: userReducer,
    academics: academicsReducer,
    assessment: assessmentReducer,
    finance: financeReducer,
    communication: communicationReducer,
    ui: uiReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export default store;