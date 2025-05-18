/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{ts,tsx,js,jsx,mdx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#1f2937',
      },
    },
  },
  plugins: [],
};