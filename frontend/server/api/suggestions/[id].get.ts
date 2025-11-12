// frontend/server/api/suggestions-[id].get.ts
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event); const apiBase = config.apiBase || config.public.apiBase
  const id = event.context.params?.id
  return await $fetch(`${apiBase}/suggestions/${id}`)
})
