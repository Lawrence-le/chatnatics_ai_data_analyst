import React from "react";
import Switch from "react-switch";

export function CustomSwitch({
  switchFunction,
  switchLabel,
  icon1,
  icon2,
  handleChange,
  size,
}) {
  return (
    <div className="flex items-center space-x-2">
      <Switch
        checked={switchFunction}
        onChange={handleChange}
        offColor="#334155"
        onColor="#90a4ae"
        offHandleColor="#e2e8f0"
        onHandleColor="#334155"
        height={20}
        width={40}
        uncheckedIcon={
          <div className="flex justify-center items-center h-full">
            {React.createElement(icon1, {
              height: size,

              className: "text-white", // Ensure icon color is white
            })}
          </div>
        }
        checkedIcon={
          <div className="flex justify-center items-center h-full">
            {React.createElement(icon2, {
              height: size,
              className: "text-black", // Ensure icon color is white
            })}
          </div>
        }
      />
      <p className="text-s">{switchLabel}</p>
    </div>
  );
}
