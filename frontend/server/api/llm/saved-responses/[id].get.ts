/**
 * Proxy for retrieving saved AI responses for a ticket
 */
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const id = getRouterParam(event, 'id')
  
  try {
    const response = await fetch(`${config.apiBase}/llm/saved-responses/${id}`)
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Failed to fetch saved responses:', error)
    throw createError({
      statusCode: 500,
      statusMessage: 'Failed to fetch saved responses'
    })
  }
})
