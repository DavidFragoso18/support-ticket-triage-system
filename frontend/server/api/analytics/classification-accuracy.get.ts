// frontend/server/api/analytics/classification-accuracy.get.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const apiBase = config.apiBase || config.public.apiBase
  return await $fetch(`${apiBase}/analytics/classification-accuracy`)
})
