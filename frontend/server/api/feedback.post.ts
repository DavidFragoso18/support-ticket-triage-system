// frontend/server/api/feedback.post.ts
export default defineEventHandler(async (event) => {
  // Use server-side runtime config (private apiBase) for SSR
  const config = useRuntimeConfig(event)
  const apiBase = config.apiBase || config.public.apiBase
  const body = await readBody(event)
  return await $fetch(`${apiBase}/feedback`, {
    method: 'POST',
    body,
  })
})
