// frontend/src/store/slices/academicsSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { academicsService } from '../../services/api';

// Async thunks
export const fetchSubjects = createAsyncThunk(
  'academics/fetchSubjects',
  async (params, { rejectWithValue }) => {
    try {
      const response = await academicsService.getSubjects(params);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

export const fetchClassGroups = createAsyncThunk(
  'academics/fetchClassGroups',
  async (params, { rejectWithValue }) => {
    try {
      const response = await academicsService.getClassGroups(params);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

export const fetchTimetables = createAsyncThunk(
  'academics/fetchTimetables',
  async (params, { rejectWithValue }) => {
    try {
      const response = await academicsService.getTimetables(params);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

const initialState = {
  subjects: [],
  classGroups: [],
  timetables: [],
  loading: false,
  error: null,
};

const academicsSlice = createSlice({
  name: 'academics',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Subjects
      .addCase(fetchSubjects.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSubjects.fulfilled, (state, action) => {
        state.loading = false;
        state.subjects = action.payload;
      })
      .addCase(fetchSubjects.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Fetch Class Groups
      .addCase(fetchClassGroups.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchClassGroups.fulfilled, (state, action) => {
        state.loading = false;
        state.classGroups = action.payload;
      })
      .addCase(fetchClassGroups.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Fetch Timetables
      .addCase(fetchTimetables.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTimetables.fulfilled, (state, action) => {
        state.loading = false;
        state.timetables = action.payload;
      })
      .addCase(fetchTimetables.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { clearError } = academicsSlice.actions;
export default academicsSlice.reducer;