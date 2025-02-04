// frontend\src\components\MainContent.jsx

// React
import { useState, useEffect, useRef } from "react";

// Effects , Graphics, Icons
import { ArrowUp } from "react-feather";
import { Typewriter } from "./TypeWriter";
import { PulseLoader } from "react-spinners";

// Service
import fetchUserInput from "../service/userInput";

// Custom Functions
import { AiAssist } from "./Assist";

// Redux
import { useDispatch, useSelector } from "react-redux";
import {
  setResponse,
  setError,
  setLoadingEntry,
  setUserInput,
  addUserDataInput,
  setAssistMode,
} from "../redux/slice";

// COMPONENT
const MainContent = () => {
  // Redux States
  const dispatch = useDispatch();
  const error = useSelector((state) => state.appData.error);
  const response = useSelector((state) => state.appData.response);
  const loadingEntry = useSelector((state) => state.appData.loadingEntry);
  const userDataInput = useSelector((state) => state.appData.userDataInput);
  const userInput = useSelector((state) => state.appData.userInput);
  const assistMode = useSelector((state) => state.appData.assistMode);

  // Local States
  const [chartData, setChartData] = useState([]);
  const scrollContainerRef = useRef(null);
  const [showSecondTypewriter, setShowSecondTypewriter] = useState(false);
  // const [userInput, setUserInput] = useState("");
  // const [userDataInput, setUserDataInput] = useState([]);
  // const [loadingEntry, setLoadingEntry] = useState(false);
  // const [response, setResponse] = useState(null);
  // const [error, setError] = useState(null);
  // const [assistMode, setAssistMode] = useState(false);

  const handleAssistModeChange = (newMode) => {
    dispatch(setAssistMode(newMode));
    console.log("Assist mode changed to:", newMode);
  };

  async function handleSubmit(e) {
    e.preventDefault();
    dispatch(setError(null));

    // Check for empty user input
    if (!userInput.trim().length) {
      return;
    }

    dispatch(setLoadingEntry(true));

    try {
      // setUserDataInput((prevData) => [
      //   ...prevData,
      //   { type: "user", text: userInput },
      // ]);
      // setUserInput("");

      dispatch(addUserDataInput({ type: "user", text: userInput }));
      dispatch(setUserInput(""));

      const data = await fetchUserInput(userInput, assistMode);
      dispatch(setResponse(data));

      // Log the data to check the response structure
      console.log("Fetched Data:", data);

      // Extract charts and response
      const charts = data.process_response.charts || [];
      const chartUrls = charts.map(
        (chartBase64) => `data:image/png;base64,${chartBase64}`
      );

      const responseText =
        data.process_response.response ||
        "The course/school/university does not co-exist.";

      // setUserDataInput((prevData) => [
      //   ...prevData,
      //   { type: "com", text: responseText, charts: chartUrls },
      // ]);

      dispatch(
        addUserDataInput({ type: "com", text: responseText, charts: chartUrls })
      );

      console.log("Fetched User Input:", data);
      dispatch(setLoadingEntry(false));
      console.log(loadingEntry);
    } catch (err) {
      dispatch(setError(err.message));
      dispatch(setLoadingEntry(false));
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      handleSubmit(e);
    }
    if (e.key === "ArrowUp") {
      // check for previous user inputs
      const lastUserInput = userDataInput[userDataInput.length - 2];

      if (lastUserInput && lastUserInput.type === "user") {
        dispatch(setUserInput(lastUserInput.text));
        // setUserInput(lastUserInput.text);
      }
    }
    if (e.key === "ArrowDown") {
      dispatch(setUserInput(""));
      // setUserInput("");
    }
  };

  useEffect(() => {
    console.log("User Input Data:", userDataInput);
    console.log("Chart Data:", chartData);
  }, [userDataInput, chartData]);

  useEffect(() => {
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop =
        scrollContainerRef.current.scrollHeight;
    }
  }, [userDataInput, chartData]);

  return (
    <section className="flex flex-col md:flex-row h-screen bg-primary dark:bg-darkprimary">
      <section className="flex flex-col flex-grow w-full md:w-4/5 p-4 overflow-y-auto ">
        {/* Conversation Container */}
        <section
          className="flex flex-col-reverse w-full md:w-3/5 p-4 space-y-4 rounded-lg mx-auto overflow-y-auto scrollbar-thin dark:scrollbar-track-darkprimary dark:scrollbar-thumb-slate-700"
          style={{ height: "100%" }}
          ref={scrollContainerRef}
        >
          <div className="flex flex-col px-2 rounded-md">
            <div className="font-bold">
              <Typewriter
                texts={[
                  `Hello, I am your Virtual Data Analyst! How can I assist you with this dataset today?`,
                ]}
                onComplete={() => setShowSecondTypewriter(true)}
              />
            </div>
            {showSecondTypewriter && (
              <p className="text-slate-500">
                <em>
                  Tip: Use the available data entities to specify the
                  information you'd like me to analyse for you.
                </em>
              </p>
            )}
            {userDataInput.map((entry, index) =>
              entry.type === "user" ? (
                <p
                  key={index}
                  className="text-left ml-auto bg-blue-400 text-white p-2 px-5 my-4 rounded-lg"
                  style={{ whiteSpace: "pre-line" }}
                >
                  {entry.text}
                </p>
              ) : (
                <div
                  key={index}
                  className="text-left mr-auto bg-gray-300 dark:bg-gray-800 p-2 px-5 my-1 rounded-lg"
                  style={{ whiteSpace: "pre-line" }}
                >
                  <Typewriter texts={[entry.text]} />
                  {entry.charts && entry.charts.length > 0 && (
                    <div className="mt-2">
                      {entry.charts.map((url, chartIndex) => (
                        <img
                          key={chartIndex}
                          src={url}
                          alt={`Generated Chart ${chartIndex + 1}`}
                          className="mb-2"
                        />
                      ))}
                    </div>
                  )}
                </div>
              )
            )}
            {loadingEntry && (
              <div className="mr-auto bg-transparent px-4 my-1 rounded-lg">
                <PulseLoader
                  color={
                    document.documentElement.classList.contains("dark")
                      ? "#e2e8f0"
                      : "#334155"
                  }
                  size={10}
                />
              </div>
            )}
          </div>
        </section>

        {/* Input Container */}
        <section className="flex flex-col w-full md:w-3/5 p-2 mt-0 mx-auto bg-secondary dark:bg-darkinput shadow rounded-lg">
          <form onSubmit={handleSubmit}>
            <textarea
              type="text"
              placeholder="Message ME"
              className="flex-1 w-full overflow-y-auto resize-none border-gray-300 bg-transparent px-4 py-2 focus:outline-none mb-2"
              style={{ height: "auto", minHeight: "40px" }}
              value={userInput}
              // onChange={(e) => setUserInput(e.target.value)}
              onChange={(e) => dispatch(setUserInput(e.target.value))}
              onKeyDown={handleKeyDown}
            />

            <section className="flex w-full px-4">
              <div>
                <p className="text-xs mb-1">
                  Push "Arrow Up" key to repeat previous input
                </p>
                <p className="text-sm text-slate-600 dark:text-white mb-1">
                  AI Assist (Powered By OpenAI)
                </p>
                <AiAssist
                  assistMode={assistMode}
                  onAssistModeChange={handleAssistModeChange}
                />
              </div>
              <button
                type="submit"
                className="bg-blue-400 text-white w-8 h-8 rounded-full hover:bg-blue-600 focus:ring focus:ring-blue-300 ml-auto flex justify-center items-center"
              >
                <ArrowUp size={16} color="white" />
              </button>
            </section>
          </form>
        </section>

        <section className="text-sm text-center flex flex-col w-full md:w-3/5 p-2 mt-0 mx-auto">
          <a
            href="https://data.gov.sg/datasets?page=1&query=graduate+employment&coverage=&resultId=d_3c55210de27fcccda2ed0c63fdd2b352"
            target="_blank"
            className="text-blue-500"
          >
            Dataset API by Open Government Products
          </a>
        </section>
      </section>
    </section>
  );
};

export default MainContent;
