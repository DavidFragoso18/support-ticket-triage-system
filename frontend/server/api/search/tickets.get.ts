export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  
  const config = useRuntimeConfig()
  const backendUrl = config.apiBase || 'http://backend:8000'
  
  try {
    const response = await $fetch(`${backendUrl}/search/tickets`, {
      params: query
    })
    return response
  } catch (error) {
    console.error('Failed to search tickets:', error)
    throw createError({
      statusCode: 500,
      message: 'Failed to search tickets'
    })
  }
})
