// frontend/composables/useApi.ts
import { $fetch } from 'ohmyfetch'
import { useRuntimeConfig } from 'nuxt/app'

export function useApi() {
  const config = useRuntimeConfig()
  const base = '/api' // we call Nuxt server routes (which proxy to FastAPI)

  const get = <T>(path: string, params?: Record<string, any>) =>
    $fetch<T>(`${base}${path}`, { method: 'GET', params })

  const post = <T>(path: string, body?: any) =>
    $fetch<T>(`${base}${path}`, { method: 'POST', body })

  return { get, post }
}
