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
    console.error("Error fetching column data. Please wait or try later");
    throw new Error("Error fetching column data. Please wait or try later");
  }
}

export default fetchColumnsData;
