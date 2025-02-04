import { useState, useEffect } from "react";
import { Sun, Moon } from "react-feather";
import { CustomSwitch } from "./Switch";

export function DarkModeToggle() {
  const [darkMode, setDarkMode] = useState(false);
  const [labelMode, setLabelMode] = useState("Light Mode");

  // Toggle dark mode and update label
  const handleDarkModeChange = (newDarkMode) => {
    setDarkMode(newDarkMode);
    setLabelMode(newDarkMode ? "Dark Mode" : "Light Mode");
  };

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [darkMode]);

  return (
    <div className="flex items-center space-x-2">
      <CustomSwitch
        switchFunction={darkMode} // Initial state (off)
        switchLabel={labelMode}
        icon1={Sun} // Icon for the off state
        icon2={Moon} // Icon for the on state
        handleChange={handleDarkModeChange}
        size={15}
      />
    </div>
  );
}
