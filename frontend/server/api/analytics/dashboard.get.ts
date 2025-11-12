export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  const days = query.days || 7
  
  const config = useRuntimeConfig()
  const backendUrl = config.apiBase || 'http://backend:8000'
  
  try {
    const response = await $fetch(`${backendUrl}/analytics/dashboard?days=${days}`)
    return response
  } catch (error) {
    console.error('Failed to fetch analytics dashboard:', error)
    throw createError({
      statusCode: 500,
      message: 'Failed to fetch analytics dashboard'
    })
  }
})
