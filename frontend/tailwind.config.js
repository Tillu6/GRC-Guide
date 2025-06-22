/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class', // enable class-based dark mode
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Existing palette
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

        // Neon / futuristic additions
        'neon-teal': '#00FFBB',      // bright accent
        'bg-very-dark': '#0a0f14',   // darker than bg-dark
        'bg-darker': '#081017',      // optional extra dark
      },
      fontFamily: {
        sans: ['"Segoe UI"', 'Roboto', 'Arial', 'sans-serif'],
      },
      boxShadow: {
        // Existing
        'lg-dark': '0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1)',
        // Neon glow shadows
        // Adjust blur/spread and color as desired.
        'neon-sm': '0 0 4px #00FFBB, 0 0 8px #00FFBB',
        'neon-md': '0 0 6px #00FFBB, 0 0 12px #00FFBB',
        'neon-lg': '0 0 8px #00FFBB, 0 0 16px #00FFBB, 0 0 24px #00FFBB',
      },
      keyframes: {
        'bounce-slow': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-3px)' },
        },
        'fade-in-up': {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        // Neon text pulse
        'neon-pulse': {
          '0%, 100%': { 'text-shadow': '0 0 4px #00FFBB, 0 0 8px #00FFBB' },
          '50%': { 'text-shadow': '0 0 6px #00FFBB, 0 0 12px #00FFBB' },
        },
      },
      animation: {
        'bounce-slow': 'bounce-slow 2s infinite',
        'fade-in-up': 'fade-in-up 0.5s ease-out forwards',
        'neon-pulse': 'neon-pulse 2s infinite',
      },
    },
  },
  plugins: [
    // Small plugin to add a .neon-text utility for text-shadow glow
    function({ addUtilities, theme }) {
      const neonColor = theme('colors.neon-teal') || '#00FFBB'
      const newUtilities = {
        '.neon-text': {
          /* text-shadow: offset-x offset-y blur color, ...
             Adjust blur values if desired */
          'text-shadow': `0 0 4px ${neonColor}, 0 0 8px ${neonColor}`,
        },
        // Optionally add a hover variant:
        '.hover-neon-text:hover': {
          'text-shadow': `0 0 6px ${neonColor}, 0 0 12px ${neonColor}`,
        },
      }
      addUtilities(newUtilities, ['responsive', 'hover'])
    }
  ],
}
