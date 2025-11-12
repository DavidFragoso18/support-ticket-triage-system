// frontend/server/api/tickets.get.ts
export default defineEventHandler(async (event) => {
  // Use server-side runtime config (private apiBase) for SSR
  const config = useRuntimeConfig(event)
  const apiBase = config.apiBase || config.public.apiBase
  const query = getQuery(event)
  return await $fetch(`${apiBase}/tickets`, { query })
})
