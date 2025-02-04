import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  error: null,
  response: null,
  loadingEntry: false,
  userDataInput: [],
  userInput: "",
  assistMode: false,
};

const appDataReducer = createSlice({
  name: "appData",
  initialState,
  reducers: {
    setError: (state, action) => {
      state.error = action.payload;
    },

    setResponse: (state, action) => {
      state.response = action.payload;
    },

    setLoadingEntry: (state, action) => {
      state.loadingEntry = action.payload;
    },

    setUserDataInput: (state, action) => {
      state.userDataInput = action.payload;
    },

    addUserDataInput: (state, action) => {
      state.userDataInput.push(action.payload); // Push new user data to the array
    },

    setUserInput: (state, action) => {
      state.userInput = action.payload;
    },

    setAssistMode: (state, action) => {
      state.assistMode = action.payload;
    },
  },
});

export const {
  setError,
  setResponse,
  setLoadingEntry,
  setUserDataInput,
  addUserDataInput,
  setUserInput,
  setAssistMode,
} = appDataReducer.actions;

export default appDataReducer.reducer;
