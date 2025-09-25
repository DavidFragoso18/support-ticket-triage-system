// frontend/server/api/resolutions.get.ts
export default defineEventHandler(async (event) => {
  const { apiBase } = useRuntimeConfig().public
  const query = getQuery(event)
  return await $fetch(`${apiBase}/resolutions`, { query })
})
