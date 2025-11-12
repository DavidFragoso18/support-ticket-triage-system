/**
 * Composable for semantic ticket search
 */
export const useTicketSearch = () => {
  const searchQuery = ref('')
  const searchMode = ref<'semantic' | 'keyword' | 'hybrid'>('hybrid')
  const searchResults = ref<any[]>([])
  const isSearching = ref(false)
  const searchError = ref<string | null>(null)

  const search = async () => {
    if (!searchQuery.value || searchQuery.value.length < 3) {
      searchResults.value = []
      return
    }

    isSearching.value = true
    searchError.value = null

    try {
      const response: any = await $fetch(`/api/search/tickets`, {
        params: {
          q: searchQuery.value,
          mode: searchMode.value,
          limit: 20,
          threshold: 0.3
        }
      })

      searchResults.value = response.results || []
    } catch (error) {
      console.error('Search failed:', error)
      searchError.value = 'Search failed. Please try again.'
      searchResults.value = []
    } finally {
      isSearching.value = false
    }
  }

  const clearSearch = () => {
    searchQuery.value = ''
    searchResults.value = []
    searchError.value = null
  }

  // Debounced search - implement simple debounce
  let debounceTimer: ReturnType<typeof setTimeout> | null = null
  const debouncedSearch = () => {
    if (debounceTimer) clearTimeout(debounceTimer)
    debounceTimer = setTimeout(search, 500)
  }

  return {
    searchQuery,
    searchMode,
    searchResults,
    isSearching,
    searchError,
    search,
    debouncedSearch,
    clearSearch
  }
}
