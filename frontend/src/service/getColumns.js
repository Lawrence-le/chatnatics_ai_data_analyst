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
    console.error("Error fetching data:", err.message);
    throw new Error("Failed to fetch columns data.");
  }
}

export default fetchColumnsData;
