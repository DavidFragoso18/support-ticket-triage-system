// frontend/nuxt.config.ts
export default defineNuxtConfig({
  devtools: { enabled: true },

  // ssr: false, // commented out
  experimental: {
    payloadExtraction: false, // Disable payload extraction to avoid Suspense issues
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000', // FastAPI
    },
  },

  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/tailwind.css'],
  tailwindcss: { viewer: false },
})