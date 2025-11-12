// frontend/server/api/resolutions.get.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event); const apiBase = config.apiBase || config.public.apiBase
  const query = getQuery(event)
  return await $fetch(`${apiBase}/resolutions`, { query })
})
