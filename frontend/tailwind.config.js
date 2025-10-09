/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
// ...
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        primary: {
          DEFAULT: '#581c87',
          hover: '#4c1d95',
        },
        accent: {
          DEFAULT: '#f97316',
          hover: '#ea580c',
        },
        headings: '#3730a3', // <-- A cor está definida aqui
      },
    },
  },
  plugins: [],
}
