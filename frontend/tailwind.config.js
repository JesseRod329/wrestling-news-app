/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      backdropBlur: {
        xxl: '40px',
      },
      colors: {
        'glass-white': 'rgba(255,255,255,0.1)',
      },
      keyframes: {
        shimmer: {
          "0%": { transform: "translateX(-100%)" },
          "100%": { transform: "translateX(100%)" },
        },
        fadeInUp: {
          "0%": { opacity: 0, transform: "translateY(20px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        },
      },
      animation: {
        shimmer: "shimmer 2.5s linear infinite",
        "fade-in-up": "fadeInUp 0.6s ease-out both",
      },
    },
  },
  plugins: [
    require('@tailwindcss/container-queries'),
  ],
}

