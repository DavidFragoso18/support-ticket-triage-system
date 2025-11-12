// frontend/server/api/analytics/sentiment-distribution.get.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const apiBase = config.apiBase || config.public.apiBase
  return await $fetch(`${apiBase}/analytics/sentiment-distribution`)
})
