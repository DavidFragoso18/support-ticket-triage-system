// https://nuxt.com/docs/api/configuration/nuxt-config
// frontend/nuxt.config.ts
export default defineNuxtConfig({
  devtools: { enabled: true },
  ssr: false, // SPA for now
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000', // FastAPI
    },
  },
})
