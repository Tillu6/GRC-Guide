/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary-blue': '#007bff',
        'dark-blue': '#004085',
        'light-gray': '#f8f9fa',
        'text-dark': '#343a40',
        'compliant-green': '#28a745',
        'noncompliant-red': '#dc3545',
        'partial-orange': '#ffc107',
        'muted-gray': '#6c757d',
        'bg-dark': '#1a202c',
        'card-dark': '#2d3748',
        'text-light': '#cbd5e0',
      },
      fontFamily: {
        sans: ['"Segoe UI"', 'Roboto', 'Arial', 'sans-serif'],
      },
      boxShadow: {
        'lg-dark': '0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1)',
      }
    },
  },
  plugins: [],
}