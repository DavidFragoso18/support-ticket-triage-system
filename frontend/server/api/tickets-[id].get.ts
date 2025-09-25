// frontend/server/api/tickets-[id].get.ts
export default defineEventHandler(async (event) => {
  const { apiBase } = useRuntimeConfig().public
  const id = event.context.params?.id
  return await $fetch(`${apiBase}/tickets/${id}`)
})
