// frontend/nuxt.config.ts
export default defineNuxtConfig({
  devtools: {
    enabled: true,

    timeline: {
      enabled: true,
    },
  },

  // ssr: false, // commented out
  experimental: {
    payloadExtraction: false, // Disable payload extraction to avoid Suspense issues
  },

  runtimeConfig: {
    // Private runtime config (server-side only)
    apiBase: process.env.API_BASE_URL || 'http://backend:8000',
    // Public runtime config (client-side)
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
    },
  },

  modules: ['@nuxtjs/tailwindcss'],
  css: ['~/assets/css/tailwind.css'],
  tailwindcss: { viewer: false },
})