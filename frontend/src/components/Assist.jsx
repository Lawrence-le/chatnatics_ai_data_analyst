//frontend\src\components\Assist.jsx

import { Check, X } from "react-feather";
import { CustomSwitch } from "./Switch";

export function AiAssist({ assistMode, onAssistModeChange }) {
  const handleAssistChange = () => {
    onAssistModeChange(!assistMode);
  };

  return (
    <div className="flex items-center space-x-2">
      <CustomSwitch
        switchFunction={assistMode}
        switchLabel={
          assistMode ? (
            <span className="text-sm">ON (Running on OpenAI)</span> // Font size for ON
          ) : (
            <span className="text-sm">
              OFF (Running on Local Language Processing Model)
            </span>
          )
        }
        icon1={X}
        icon2={Check}
        handleChange={handleAssistChange}
        size={12}
      />
    </div>
  );
}
