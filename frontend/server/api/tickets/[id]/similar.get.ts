export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const id = getRouterParam(event, 'id')
  
  const url = `${config.apiBase}/tickets/${id}/similar`
  
  return $fetch(url)
})
