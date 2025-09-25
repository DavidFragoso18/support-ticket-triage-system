// frontend/server/api/tickets.get.ts
export default defineEventHandler(async (event) => {
  const { apiBase } = useRuntimeConfig().public
  const query = getQuery(event)
  return await $fetch(`${apiBase}/tickets`, { query })
})
