// frontend/src/service/get_columns.js

import axios from "axios";

async function fetchColumnsData() {
  try {
    const response = await axios.get("http://localhost:5000/api/get_columns");
    return response.data;
  } catch (err) {
    console.error("Error fetching data:", err.message);
    throw new Error("Failed to fetch columns data.");
  }
}

export default fetchColumnsData;
