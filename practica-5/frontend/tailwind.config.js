/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        marvel: '#ed1d24',
        dc: '#0476f2'
      }
    },
  },
  plugins: [],
}
