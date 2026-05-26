import type { Config } from 'tailwindcss';
const config: Config = {
  darkMode: ['class'],
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: { sans: ['Inter', 'ui-sans-serif', 'system-ui'] },
      boxShadow: { glow: '0 0 60px rgba(56, 189, 248, .22)', panel: '0 24px 80px rgba(0,0,0,.45)' },
      backgroundImage: {
        'aurora': 'radial-gradient(circle at 15% 15%, rgba(34,211,238,.28), transparent 26%), radial-gradient(circle at 85% 20%, rgba(168,85,247,.26), transparent 30%), radial-gradient(circle at 50% 100%, rgba(16,185,129,.16), transparent 30%)'
      },
      animation: { float: 'float 7s ease-in-out infinite', pulseglow: 'pulseglow 3s ease-in-out infinite' },
      keyframes: {
        float: { '0%,100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-14px)' } },
        pulseglow: { '0%,100%': { opacity: '.65' }, '50%': { opacity: '1' } }
      }
    }
  },
  plugins: [require('tailwindcss-animate')]
};
export default config;
