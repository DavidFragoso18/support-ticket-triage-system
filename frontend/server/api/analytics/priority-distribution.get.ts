// frontend/server/api/analytics/priority-distribution.get.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const apiBase = config.apiBase || config.public.apiBase
  return await $fetch(`${apiBase}/analytics/priority-distribution`)
})
