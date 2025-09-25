// frontend/composables/useApi.ts
export function useApi() {
  const base = '/api' // we call Nuxt server routes (which proxy to FastAPI)

  const get = <T>(path: string, params?: Record<string, any>) =>
    $fetch<T>(`${base}${path}`, { method: 'GET', query: params })

  const post = <T>(path: string, body?: any) =>
    $fetch<T>(`${base}${path}`, { method: 'POST', body })

  return { get, post }
}