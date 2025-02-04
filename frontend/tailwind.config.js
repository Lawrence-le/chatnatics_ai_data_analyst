export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  darkMode: "class", // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        primary: "#f1f5f9",
        secondary: "#e2e8f0",
        input: "#f8fafc",

        darkprimary: "#171717",
        darksecondary: "#0c0a09",
        // darkinput: "#1e293b",
        darkinput: "#262626",
      },
      fontFamily: {
        sans: ['"Source Sans 3"', "sans-serif"], // Correct way to define the font family
        serif: ["serif"],
      },
    },
  },

  variants: {
    extend: {},
  },
  plugins: [
    require("tailwind-scrollbar"), // Add the plugin
  ],
};
