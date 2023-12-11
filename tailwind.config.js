/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./static/**/*.js", "./templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        'lightest-blue': '#D2E1FF',
        'light-blue': '#A5C3FF',
        'medium-blue': '#0C3D9D',
        'dark-blue': '#012873',
        'dark-orange': '#842A00',
        'orange': '#FFA15E',
        'light-orange': '#FFD0AE',
        'light-grey': '#F0EFE9',
        'dark-grey': '#575764',
        'black': '#000000',
        'white': '#FFFFFF',
        'error-red': '#FF7E86',
      },
      spacing: {
        '350': '350px',
        '316': '316px',
        '70': '70px',
      },
    },
  },
  plugins: [],
}

