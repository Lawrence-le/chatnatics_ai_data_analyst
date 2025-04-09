// frontend/src/service/userInput.js

import axios from "axios";
import { getServerStatusApi } from "./apiUrl";

async function getServerStatus() {
  try {
    const response = await axios.get(getServerStatusApi, {
      headers: { "Content-Type": "application/json" },
    });
    return response.data;
  } catch (err) {
    console.error("Error fetching data:", err.message);
    throw new Error("Failed to fetch columns data.");
  }
}

export default getServerStatus;
