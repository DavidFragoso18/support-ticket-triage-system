// frontend/server/api/suggestions-[id].get.ts
export default defineEventHandler(async (event) => {
  const { apiBase } = useRuntimeConfig().public
  const id = event.context.params?.id
  return await $fetch(`${apiBase}/suggestions/${id}`)
})
