import { useEffect, useState } from "react";

export function Typewriter({ texts, onComplete, typeSpeed = 5 }) {
  const [displayedText, setDisplayedText] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (currentIndex < texts[0].length) {
      const timeout = setTimeout(() => {
        setDisplayedText((prev) => prev + texts[0][currentIndex]);
        setCurrentIndex((prev) => prev + 1);
      }, typeSpeed);
      return () => clearTimeout(timeout);
    } else {
      if (onComplete) {
        onComplete();
      }
    }
  }, [currentIndex, texts, onComplete, typeSpeed]);

  return (
    <div
      dangerouslySetInnerHTML={{
        __html: `<span class="text-slate-700 dark:text-blue-400 text-m">${displayedText}</span>`,
      }}
    />
  );
}
