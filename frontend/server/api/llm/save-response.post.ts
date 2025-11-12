/**
 * Proxy for saving AI-generated responses
 */
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const body = await readBody(event)
  
  try {
    const response = await fetch(`${config.apiBase}/llm/save-response`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    })
    
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Failed to save AI response:', error)
    throw createError({
      statusCode: 500,
      statusMessage: 'Failed to save AI response'
    })
  }
})
