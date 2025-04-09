//

import Sidebar from "./components/SideBar";
import "./App.css";
import MainContent from "./components/MainContent";

// Disable Log
if (import.meta.env.MODE === "production") {
  console.log = () => {};
  console.info = () => {};
  console.warn = () => {};
  console.error = () => {};
}

function App() {
  return (
    <section className="flex flex-col md:flex-row h-screen bg-primary dark:bg-darkprimary">
      {/* Sidebar */}
      <section className="w-full md:w-1/5 bg-secondary dark:bg-darksecondary p-4 z-20 ">
        <Sidebar />
      </section>
      {/* Main Content */}
      <section className="flex flex-col flex-grow w-full md:w-4/5 z-10 overflow-hidden">
        <MainContent />
      </section>
    </section>
  );
}

export default App;
