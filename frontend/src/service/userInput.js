// frontend/src/service/userInput.js

import axios from "axios";
import { getUserPromptApi } from "./apiUrl";

async function fetchUserInput(userInput, assistMode) {
  try {
    // const apiUrl = `${apiGetUrl}/api/user_prompt/prompt`;
    const response = await axios.post(getUserPromptApi, {
      user_input: userInput,
      openai_status: assistMode,
    });

    // const response = await axios.post(
    //   "http://localhost:5000/api/user_prompt/prompt",
    //   { user_input: userInput, openai_status: assistMode }
    // );
    return response.data;
  } catch (err) {
    console.error("Error fetching data:", err.message);
    throw new Error("Failed to fetch columns data.");
  }
}

export default fetchUserInput;
