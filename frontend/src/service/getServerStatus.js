// frontend/src/service/userInput.js

import axios from "axios";
import { getServerStatusApi } from "./apiUrl";

async function getServerStatus() {
  try {
    const response = await axios.get(getServerStatusApi, {
      headers: { "Content-Type": "application/json" },
    });
    return response.data;
  } catch {
    const errorMsg = "Server Down - Please wait or try again later:";
    console.error(errorMsg);
    throw new Error(errorMsg);
  }
}

export default getServerStatus;
