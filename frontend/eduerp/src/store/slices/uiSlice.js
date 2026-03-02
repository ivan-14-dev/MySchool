import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  sidebarOpen: false,
  theme: "light",
  loading: false,
  error: null,
};

const uiSlice = createSlice({
  name: "ui",
  initialState,
  reducers: {
    toggleSidebar(state) {
      state.sidebarOpen = !state.sidebarOpen;
    },
    setTheme(state, action) {
      state.theme = action.payload;
    },
    setLoading(state, action) {
      state.loading = action.payload;
    },
    setError(state, action) {
      state.error = action.payload;
    },
  },
});

export const { toggleSidebar, setTheme, setLoading, setError } = uiSlice.actions;
export default uiSlice.reducer;
