// frontend/server/api/analytics/overview.get.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const apiBase = config.apiBase || config.public.apiBase
  return await $fetch(`${apiBase}/analytics/overview`)
})
