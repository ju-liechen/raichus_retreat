/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./static/**/*.js", "./templates/**/*.html"],
  theme: {
    extend: {
    colors: {
      'lightest-blue': '#e6f7ff',
      'light-blue': '#99dfff',
      'medium-blue': '#4dc6ff',
      'dark-blue': '#009de6',
      'darkest-blue': '#004666',
      'navy-blue': '#002333',
      'black': '#000000',
      'white': '#FFFFFF'
    },
    },
  },
  plugins: [],
}

