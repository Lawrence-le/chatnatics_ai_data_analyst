// frontend/src/service/getServerStatus.js

import axios from "axios";
import { getServerStatusApi } from "./apiUrl";

async function getServerStatus() {
  try {
    const response = await axios.get(getServerStatusApi, {
      headers: { "Content-Type": "application/json" },
    });
    return response.data;
  } catch {
    const errorMessage =
      "Service temporarily unavailable. Please try again later.";
    console.error(errorMessage);
    throw new Error(errorMessage);
  }
}

export default getServerStatus;
