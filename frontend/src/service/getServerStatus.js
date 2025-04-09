// frontend/src/service/getServerStatus.js

import axios from "axios";
import { getServerStatusApi } from "./apiUrl";

async function getServerStatus() {
  try {
    const response = await axios.get(getServerStatusApi, {
      headers: { "Content-Type": "application/json" },
    });
    return response.data;
  } catch (err) {
    if (import.meta.env.MODE === "development") {
      console.log("Dev-only log:", err);
    }
    return null;
  }
}

export default getServerStatus;
