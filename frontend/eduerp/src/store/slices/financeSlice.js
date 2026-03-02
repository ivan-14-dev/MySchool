// frontend/src/store/slices/financeSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { financeService } from '../../services/api';

// Async thunks
export const fetchFees = createAsyncThunk(
  'finance/fetchFees',
  async (params, { rejectWithValue }) => {
    try {
      const response = await financeService.getFees(params);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

export const fetchInvoices = createAsyncThunk(
  'finance/fetchInvoices',
  async (params, { rejectWithValue }) => {
    try {
      const response = await financeService.getInvoices(params);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

export const fetchPayments = createAsyncThunk(
  'finance/fetchPayments',
  async (params, { rejectWithValue }) => {
    try {
      const response = await financeService.getPayments(params);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

const initialState = {
  fees: [],
  invoices: [],
  payments: [],
  loading: false,
  error: null,
};

const financeSlice = createSlice({
  name: 'finance',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    addPayment: (state, action) => {
      state.payments.push(action.payload);
    },
    updateInvoice: (state, action) => {
      const index = state.invoices.findIndex(i => i.id === action.payload.id);
      if (index !== -1) {
        state.invoices[index] = action.payload;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Fees
      .addCase(fetchFees.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchFees.fulfilled, (state, action) => {
        state.loading = false;
        state.fees = action.payload;
      })
      .addCase(fetchFees.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Fetch Invoices
      .addCase(fetchInvoices.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchInvoices.fulfilled, (state, action) => {
        state.loading = false;
        state.invoices = action.payload;
      })
      .addCase(fetchInvoices.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Fetch Payments
      .addCase(fetchPayments.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPayments.fulfilled, (state, action) => {
        state.loading = false;
        state.payments = action.payload;
      })
      .addCase(fetchPayments.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { clearError, addPayment, updateInvoice } = financeSlice.actions;
export default financeSlice.reducer;