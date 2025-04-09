import axios from "axios";
import { getColumnApi } from "./apiUrl";

async function fetchColumnsData() {
  try {
    const response = await axios.get(getColumnApi, {
      headers: { "Content-Type": "application/json" },
    });
    return response.data;
  } catch (err) {
    if (err.response) {
      console.error("Service temporarily unavailable. Please try again later.");
    } else if (err.request) {
      console.error(
        "Unable to connect to the backend. Please check your connection."
      );
    } else {
      console.error("An unexpected error occurred.");
    }
    throw new Error("Error fetching column data. Please try again later");
  }
}

export default fetchColumnsData;
