// frontend/server/api/tickets.post.ts
export default defineEventHandler(async (event) => {
  const { apiBase } = useRuntimeConfig().public
  const body = await readBody(event)
  return await $fetch(`${apiBase}/tickets`, { method: 'POST', body })
})
