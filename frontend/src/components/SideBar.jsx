// frontend\src\components\SideBar.jsx

import { useState, useEffect } from "react";
import fetchColumnsData from "../service/getColumns";
import getServerStatus from "../service/getServerStatus";
import { DarkModeToggle } from "./DarkMode";
import { useDispatch, useSelector } from "react-redux";
import { setError } from "../redux/slice";
import DataFetchingModal from "./DataFetchingModal";
import { User } from "react-feather";

const Sidebar = () => {
  const dispatch = useDispatch();
  const [columnsData, setColumnsData] = useState(null);
  const [hoveredColumn, setHoveredColumn] = useState(null);
  const [loadingCompleted, setLoadingCompleted] = useState(false);
  const [serverReady, setServerReady] = useState(false);
  const error = useSelector((state) => state.appData.error);

  const capitalizeFirstLetter = (string) => {
    if (typeof string !== "string" || string.length === 0) return string;
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  const sortItems = (items) => {
    if (items.length === 0) return items;
    return [...items].sort((a, b) => a.charAt(0).localeCompare(b.charAt(0)));
  };

  useEffect(() => {
    const getData = async () => {
      try {
        const data = await fetchColumnsData();
        setColumnsData(data.unique_values);
        setLoadingCompleted(true);
      } catch (err) {
        console.error("Error fetching columns data");

        setLoadingCompleted(false);
      }
    };
    getData();
  }, [dispatch]);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const statusResponse = await getServerStatus();
        if (getServerStatus !== null) {
          setServerReady(true);
        }
      } catch (err) {
        setServerReady(false);
        console.error("Error fetching server status:");
        setLoadingCompleted(false);
      }
    };
    checkStatus();
  }, [setServerReady]);

  useEffect(() => {
    console.log("Updated Columns Data:", columnsData);
    console.log("Loading Status:", loadingCompleted);
    console.log("Server Ready:", serverReady);
  }, [columnsData]);

  return (
    <div className="bg-secondary dark:bg-darksecondary p-4">
      <DataFetchingModal loading={serverReady} />
      <div className="text-xl font-bold">Chatnatics</div>
      <div className="text-m mb-3">Your AI Data Analyst</div>
      <hr className="mb-5 border-black dark:border-white" />
      <div className="">
        <DarkModeToggle />
      </div>
      <div className="text-xl font-bold mt-5">Dataset Information</div>
      <div className="text-lg font-bold mt-5">Title</div>
      <div className="text-m">
        Graduate Employment Survey - NTU, NUS, SIT, SMU, SUSS & SUTD (2013-2022)
      </div>
      <div className="text-lg font-bold mt-5 mb-2">Data Entities</div>
      {error && <p style={{ color: "red" }}>Error: {error}</p>}
      {!columnsData ? (
        <p>Loading...</p>
      ) : (
        <ul className="space-y-0">
          {Object.entries(columnsData).map(([column, uniqueValues]) => (
            <li
              key={column}
              className="hover:bg-primary dark:hover:bg-gray-600 p-2 rounded relative"
              onMouseEnter={() => setHoveredColumn(column)}
              onMouseLeave={() => setHoveredColumn(null)}
            >
              <span className="font-medium">
                {capitalizeFirstLetter(column)}
              </span>{" "}
              {hoveredColumn === column && (
                <div className="absolute left-full top-0 bg-white dark:bg-gray-800 text-black dark:text-white shadow-md p-2 rounded w-96 max-h-96 overflow-y-auto scrollbar-thin scrollbar-thumb-slate-700 scrollbar-track-slate-300">
                  <ul>
                    {sortItems(uniqueValues).map((value, index) => (
                      <li key={index} className="text-sm ">
                        {value}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Sidebar;
