// frontend/src/service/get_columns.js

import axios from "axios";
import { getColumnApi } from "./apiUrl";

async function fetchColumnsData() {
  try {
    const response = await axios.get(getColumnApi, {
      headers: { "Content-Type": "application/json" },
    });
    return response.data;
  } catch (err) {
    const errorMsg = "Error fetching data";
    console.error(errorMsg);
    throw new Error(errorMsg);
  }
}

export default fetchColumnsData;
