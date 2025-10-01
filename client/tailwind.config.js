module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
  ],
  safelist: [
    {
      pattern: /fill-red-(50|100|200|300|400|500|600|700|800|900|950)/,
    }
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
