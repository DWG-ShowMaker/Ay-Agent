/** @type {import('tailwindcss').Config} */
import typography from '@tailwindcss/typography'

export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            maxWidth: 'none',
            code: {
              color: '#eb4432',
              '&::before': {
                content: '""'
              },
              '&::after': {
                content: '""'
              }
            }
          }
        }
      }
    },
  },
  plugins: [
    typography
  ],
}
