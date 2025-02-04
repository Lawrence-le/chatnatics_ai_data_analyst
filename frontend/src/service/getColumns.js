// frontend/src/service/get_columns.js

import axios from "axios";
import { getColumnApi } from "./apiUrl";

async function fetchColumnsData() {
  try {
    // const apiUrl = `${apiGetUrl}/api/get_columns`;
    // console.log(apiUrl);
    const response = await axios.get(getColumnApi);
    // const response = await axios.get("http://localhost:5000/api/get_columns");
    return response.data;
  } catch (err) {
    console.error("Error fetching data:", err.message);
    throw new Error("Failed to fetch columns data.");
  }
}

export default fetchColumnsData;
