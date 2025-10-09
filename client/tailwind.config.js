module.exports = {
  content: [
    './src/components/*.{js,ts,jsx,tsx}',
    './src/app/**/*.{js,ts,jsx,tsx}',
    './src/app/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'primary': {
          50: '#838E83',
          100: '#D9E6D9',
          200: '#BBCBBB',
          300: '#A1AFA1',
          400: '#889488',
          500: '#707A70',
          600: '#586058',
          700: '#424842',
          800: '#2D322D',
          900: '#191C19',
        },
        'secondary': {
          50: '#F6F6F8',
          100: '#E8E8ED',
          200: '#CBCBD7',
          300: '#AFAFC2',
          400: '#9494AD',
          500: '#797998',
          600: '#5E5E80',
          700: '#464667',
          800: '#303049',
          900: '#1A1A2A',
        }
      }
    },
  },
  plugins: [],
};
