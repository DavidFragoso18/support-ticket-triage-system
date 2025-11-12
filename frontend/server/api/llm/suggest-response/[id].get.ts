/**
 * Proxy for LLM response suggestion endpoint
 */
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const id = getRouterParam(event, 'id')
  const query = getQuery(event)
  
  const url = new URL(`${config.apiBase}/llm/suggest-response/${id}`)
  
  // Add tone parameter if provided
  if (query.tone) {
    url.searchParams.set('tone', query.tone as string)
  }
  
  try {
    const response = await fetch(url.toString())
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Failed to fetch response suggestion:', error)
    throw createError({
      statusCode: 500,
      statusMessage: 'Failed to generate response suggestion'
    })
  }
})
