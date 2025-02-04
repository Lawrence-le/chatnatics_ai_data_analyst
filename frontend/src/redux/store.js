// src/redux/store.js
// npm install @reduxjs/toolkit react-redux

import { configureStore } from "@reduxjs/toolkit";
import appDataReducer from "./slice";

const store = configureStore({
  reducer: {
    appData: appDataReducer,
  },
});

export default store;
