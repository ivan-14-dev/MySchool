// frontend/src/store/slices/assessmentSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { assessmentService } from '../../services/api';

// Async thunks
export const fetchAssessments = createAsyncThunk(
  'assessment/fetchAssessments',
  async (params, { rejectWithValue }) => {
    try {
      const response = await assessmentService.getAssessments(params);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

export const fetchGrades = createAsyncThunk(
  'assessment/fetchGrades',
  async (params, { rejectWithValue }) => {
    try {
      const response = await assessmentService.getGrades(params);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

export const fetchAttendance = createAsyncThunk(
  'assessment/fetchAttendance',
  async (params, { rejectWithValue }) => {
    try {
      const response = await assessmentService.getAttendance(params);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

const initialState = {
  assessments: [],
  grades: [],
  attendance: [],
  loading: false,
  error: null,
};

const assessmentSlice = createSlice({
  name: 'assessment',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    addAssessment: (state, action) => {
      state.assessments.push(action.payload);
    },
    updateAssessment: (state, action) => {
      const index = state.assessments.findIndex(a => a.id === action.payload.id);
      if (index !== -1) {
        state.assessments[index] = action.payload;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Assessments
      .addCase(fetchAssessments.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAssessments.fulfilled, (state, action) => {
        state.loading = false;
        state.assessments = action.payload;
      })
      .addCase(fetchAssessments.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Fetch Grades
      .addCase(fetchGrades.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchGrades.fulfilled, (state, action) => {
        state.loading = false;
        state.grades = action.payload;
      })
      .addCase(fetchGrades.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Fetch Attendance
      .addCase(fetchAttendance.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAttendance.fulfilled, (state, action) => {
        state.loading = false;
        state.attendance = action.payload;
      })
      .addCase(fetchAttendance.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { clearError, addAssessment, updateAssessment } = assessmentSlice.actions;
export default assessmentSlice.reducer;