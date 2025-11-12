<template>
  <div class="min-h-screen bg-white text-zinc-900 dark:bg-zinc-950 dark:text-zinc-100">
    <!-- WebSocket Notification Toast -->
    <Transition name="slide-down">
      <div
        v-if="showNotification"
        class="fixed top-4 right-4 z-50 max-w-sm rounded-xl border shadow-lg"
        :class="{
          'bg-blue-50 border-blue-200 dark:bg-blue-950 dark:border-blue-800': notificationType === 'info',
          'bg-green-50 border-green-200 dark:bg-green-950 dark:border-green-800': notificationType === 'success',
          'bg-yellow-50 border-yellow-200 dark:bg-yellow-950 dark:border-yellow-800': notificationType === 'warning',
          'bg-red-50 border-red-200 dark:bg-red-950 dark:border-red-800': notificationType === 'error'
        }"
      >
        <div class="p-4 flex items-start gap-3">
          <div class="flex-1">
            <p class="text-sm font-medium" :class="{
              'text-blue-900 dark:text-blue-100': notificationType === 'info',
              'text-green-900 dark:text-green-100': notificationType === 'success',
              'text-yellow-900 dark:text-yellow-100': notificationType === 'warning',
              'text-red-900 dark:text-red-100': notificationType === 'error'
            }">{{ notificationMessage }}</p>
          </div>
          <button
            @click="showNotification = false"
            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>
      </div>
    </Transition>

    <!-- WebSocket Connection Status -->
    <div class="fixed bottom-4 left-4 z-40">
      <div v-if="isConnected" class="flex items-center gap-2 px-3 py-1.5 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-full text-xs">
        <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
        <span class="text-green-700 dark:text-green-300">Live</span>
      </div>
      <div v-else class="flex items-center gap-2 px-3 py-1.5 bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-full text-xs">
        <span class="w-2 h-2 bg-red-500 rounded-full"></span>
        <span class="text-red-700 dark:text-red-300">Disconnected</span>
      </div>
    </div>

    <div class="mx-auto max-w-6xl p-6 space-y-6">
      <!-- Header -->
      <div class="flex flex-wrap items-center justify-between gap-4">
        <h1 class="text-2xl font-semibold tracking-tight flex items-center gap-2">
          🦈 GYM SHARK - Tickets
        </h1>

        <div class="flex items-center gap-3">
          <!-- How It Works Link -->
          <NuxtLink
            to="/how-it-works"
            class="inline-flex items-center gap-2 rounded-xl border border-zinc-300 px-3 py-2 text-sm hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-900"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
            </svg>
            <span class="hidden sm:inline">How It Works</span>
          </NuxtLink>

          <!-- Analytics Link -->
          <NuxtLink
            to="/analytics"
            class="inline-flex items-center gap-2 rounded-xl border border-zinc-300 px-3 py-2 text-sm hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-900"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M3 13h2v8H3v-8zm4-6h2v14H7V7zm4-4h2v18h-2V3zm4 9h2v9h-2v-9zm4-3h2v12h-2V9z"/>
            </svg>
            <span class="hidden sm:inline">Analytics</span>
          </NuxtLink>
          
          <!-- Theme toggle -->
          <button
            class="inline-flex items-center gap-2 rounded-xl border border-zinc-300 px-3 py-2 text-sm hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-900"
            @click="toggleTheme"
            :aria-label="`Switch to ${isDark ? 'light' : 'dark'} mode`"
          >
            <svg v-if="!isDark" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 18a6 6 0 1 0 0-12 6 6 0 0 0 0 12Zm0 4a1 1 0 0 1-1-1v-1.1a1 1 0 1 1 2 0V21a1 1 0 0 1-1 1Zm0-18a1 1 0 0 1-1-1V2.1a1 1 0 1 1 2 0V3a1 1 0 0 1-1 1Zm9 9a1 1 0 0 1-1 1h-1.1a1 1 0 1 1 0-2H20a1 1 0 0 1 1 1ZM5.1 12a1 1 0 1 1 0-2H6.2a1 1 0 1 1 0 2H5.1ZM17.66 6.34a1 1 0 0 1 0-1.41l.78-.78a1 1 0 0 1 1.41 1.41l-.78.78a1 1 0 0 1-1.41 0ZM4.15 19.85a1 1 0 0 1 0-1.41l.78-.78a1 1 0 1 1 1.41 1.41l-.78.78a1 1 0 0 1-1.41 0ZM6.34 6.34a1 1 0 0 1-1.41 0l-.78-.78A1 1 0 0 1 5.56 3.4l.78.78a1 1 0 0 1 0 1.41Zm12.51 12.1a1 1 0 0 1-1.41 0l-.78-.78a1 1 0 1 1 1.41-1.41l.78.78a1 1 0 0 1 0 1.41Z"/>
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M21.64 13A9 9 0 1 1 11 2.36 7 7 0 1 0 21.64 13Z"/>
            </svg>
            <span class="hidden sm:inline">{{ isDark ? 'Dark' : 'Light' }}</span>
          </button>

          <NuxtLink
            to="/compose"
            class="inline-flex items-center gap-2 rounded-xl bg-zinc-900 px-4 py-2 text-sm font-medium text-white hover:bg-zinc-800 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor"><path d="M11 11V5a1 1 0 1 1 2 0v6h6a1 1 0 1 1 0 2h-6v6a1 1 0 1 1-2 0v-6H5a1 1 0 1 1 0-2h6Z"/></svg>
            New ticket
          </NuxtLink>
        </div>
      </div>

      <!-- Semantic Search Bar -->
      <div class="rounded-2xl border border-zinc-200 bg-white/70 p-4 dark:border-zinc-800 dark:bg-zinc-900/60">
        <div class="flex flex-col md:flex-row gap-3">
          <!-- Search Input -->
          <div class="flex-1 relative">
            <input
              v-model="searchQuery"
              @input="debouncedSearch"
              @keyup.enter="search"
              type="text"
              placeholder="🔍 Search tickets semantically (e.g., 'login issues', 'payment problems')..."
              class="w-full rounded-xl border border-zinc-300 pl-4 pr-10 py-2.5 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20 dark:border-zinc-700 dark:bg-zinc-900 dark:focus:border-blue-400"
            />
            <button
              v-if="searchQuery"
              @click="clearSearch"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>

          <!-- Search Mode Selector -->
          <div class="flex items-center gap-2">
            <select
              v-model="searchMode"
              @change="searchQuery && search()"
              class="rounded-xl border border-zinc-300 px-3 py-2.5 text-sm bg-white dark:bg-zinc-900 dark:border-zinc-700 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
            >
              <option value="hybrid">🎯 Hybrid</option>
              <option value="semantic">🧠 Semantic</option>
              <option value="keyword">📝 Keyword</option>
            </select>
            
            <button
              @click="search"
              :disabled="!searchQuery || isSearching"
              class="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="isSearching">Searching...</span>
              <span v-else>Search</span>
            </button>
          </div>
        </div>

        <!-- Search Results Summary -->
        <div v-if="searchResults.length > 0" class="mt-3 flex items-center justify-between text-xs text-zinc-500">
          <span>Found {{ searchResults.length }} tickets matching "{{ searchQuery }}"</span>
          <button
            @click="clearSearch"
            class="text-blue-600 hover:text-blue-700 dark:text-blue-400 font-medium"
          >
            Clear search
          </button>
        </div>
        
        <div v-if="searchError" class="mt-3 text-sm text-red-600 dark:text-red-400">
          {{ searchError }}
        </div>
      </div>

      <!-- Filters dropdown -->
      <details class="group rounded-2xl border border-zinc-200 bg-white/70 p-0 dark:border-zinc-800 dark:bg-zinc-900/60">
        <summary
          class="flex cursor-pointer list-none items-center justify-between gap-3 rounded-2xl px-4 py-3 hover:bg-zinc-50 group-open:rounded-b-none dark:hover:bg-zinc-800"
        >
          <div class="flex items-center gap-3">
            <span class="font-medium">Filters</span>
            <span v-if="activeFilterCount" class="rounded-full bg-zinc-900 px-2 py-0.5 text-xs text-white dark:bg-white dark:text-zinc-900">
              {{ activeFilterCount }}
            </span>
          </div>
          <svg class="h-4 w-4 transition-transform group-open:rotate-180" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 10.94l3.71-3.71a.75.75 0 1 1 1.06 1.06l-4.24 4.24a.75.75 0 0 1-1.06 0L5.21 8.29a.75.75 0 0 1 .02-1.08Z" clip-rule="evenodd" />
          </svg>
        </summary>

        <div class="border-t border-zinc-200 p-4 dark:border-zinc-800 group-open:rounded-b-2xl">
          <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
            <!-- Intent -->
            <div>
              <label for="intent-filter" class="mb-2 block text-xs font-medium text-zinc-500">Intent</label>
              <select
                id="intent-filter"
                v-model="filters.intent"
                class="w-full rounded-xl border border-zinc-300 px-3 py-2 text-sm focus:border-zinc-500 focus:outline-none focus:ring-2 focus:ring-zinc-500/20 dark:border-zinc-700 dark:bg-zinc-900 dark:focus:border-zinc-400"
              >
                <option value="">All intents</option>
                <option v-for="opt in intentOptions" :key="opt" :value="opt">
                  {{ opt.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) }}
                </option>
              </select>
            </div>

            <!-- Sentiment -->
            <div>
              <label for="sentiment-filter" class="mb-2 block text-xs font-medium text-zinc-500">Sentiment</label>
              <select
                id="sentiment-filter"
                v-model="filters.sentiment"
                class="w-full rounded-xl border border-zinc-300 px-3 py-2 text-sm focus:border-zinc-500 focus:outline-none focus:ring-2 focus:ring-zinc-500/20 dark:border-zinc-700 dark:bg-zinc-900 dark:focus:border-zinc-400"
              >
                <option value="">All sentiments</option>
                <option v-for="opt in sentimentOptions" :key="opt" :value="opt">
                  {{ opt.charAt(0).toUpperCase() + opt.slice(1) }}
                </option>
              </select>
            </div>

            <!-- Priority -->
            <div>
              <label for="priority-filter" class="mb-2 block text-xs font-medium text-zinc-500">Priority</label>
              <select
                id="priority-filter"
                v-model="filters.priority"
                class="w-full rounded-xl border border-zinc-300 px-3 py-2 text-sm focus:border-zinc-500 focus:outline-none focus:ring-2 focus:ring-zinc-500/20 dark:border-zinc-700 dark:bg-zinc-900 dark:focus:border-zinc-400"
              >
                <option value="">All priorities</option>
                <option v-for="opt in priorityOptions" :key="opt" :value="opt">
                  {{ opt }}
                </option>
              </select>
            </div>
          </div>

          <div class="mt-4 flex items-center gap-3">
            <button class="text-xs text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300" @click="resetFilters">Reset</button>
            <div class="ml-auto flex items-center gap-2">
              <button class="rounded-xl border border-zinc-300 px-3 py-2 text-sm hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-800" @click="refreshList">Apply</button>
            </div>
            <span v-if="error" class="text-sm text-rose-600">{{ error }}</span>
          </div>
        </div>
      </details>

      <!-- List (table on md+, cards on mobile) -->
      <div class="rounded-2xl border border-zinc-200 dark:border-zinc-800">
        <!-- TABLE -->
        <div class="hidden md:block">
          <table class="min-w-full text-sm">
            <thead>
              <tr class="bg-zinc-50 text-left dark:bg-zinc-900/40">
                <th class="px-4 py-3 font-medium text-zinc-500">Subject</th>
                <th class="px-4 py-3 font-medium text-zinc-500">Intent</th>
                <th class="px-4 py-3 font-medium text-zinc-500">Sentiment</th>
                <th class="px-4 py-3 font-medium text-zinc-500">Priority</th>
                <th class="px-4 py-3 font-medium text-zinc-500">Created</th>
                <th class="px-4 py-3"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="pending" class="border-t border-zinc-200 dark:border-zinc-800">
                <td class="px-4 py-4" colspan="6">
                  <div class="h-5 w-3/4 animate-pulse rounded bg-zinc-100 dark:bg-zinc-800"></div>
                </td>
              </tr>
              <tr v-else-if="!items.length" class="border-t border-zinc-200 dark:border-zinc-800">
                <td class="px-4 py-6 text-zinc-500" colspan="6">No tickets found.</td>
              </tr>
              <tr
                v-for="t in items" :key="t.id"
                class="border-t border-zinc-200 hover:bg-zinc-50 dark:border-zinc-800 dark:hover:bg-zinc-900/40"
              >
                <td class="px-4 py-3">
                  <div class="font-medium line-clamp-1">{{ t.subject }}</div>
                  <div class="text-zinc-500 line-clamp-1">{{ t.body }}</div>
                </td>
                <td class="px-4 py-3">
                  <span class="badge" :class="intentBadge(t.classification?.intent)">{{ t.classification?.intent || '—' }}</span>
                </td>
                <td class="px-4 py-3">
                  <span class="badge" :class="sentimentBadge(t.classification?.sentiment)">{{ t.classification?.sentiment || '—' }}</span>
                </td>
                <td class="px-4 py-3">
                  <span :class="priorityBadgeClass(t.classification?.priority)" class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ring-1">
                    {{ t.classification?.priority || '—' }}
                  </span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap">{{ formatDate(t.created_at) }}</td>
                <td class="px-4 py-3 text-right">
                  <NuxtLink :to="`/tickets/${t.id}`" class="text-sm text-zinc-900 underline hover:no-underline dark:text-zinc-100">Open</NuxtLink>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- CARDS -->
        <div class="md:hidden">
          <div v-if="pending" class="space-y-3 p-3">
            <div class="rounded-xl border border-zinc-200 p-4 dark:border-zinc-800">
              <div class="h-5 w-2/3 animate-pulse rounded bg-zinc-100 dark:bg-zinc-800"></div>
              <div class="mt-2 h-4 w-full animate-pulse rounded bg-zinc-100 dark:bg-zinc-800"></div>
            </div>
          </div>

          <div v-else-if="!items.length" class="p-4 text-zinc-500">
            No tickets found.
          </div>

          <div v-else class="divide-y divide-zinc-200 dark:divide-zinc-800">
            <article v-for="t in items" :key="t.id" class="p-4">
              <header class="mb-2 flex items-start justify-between gap-3">
                <h2 class="text-base font-semibold leading-snug">{{ t.subject }}</h2>
                <span :class="priorityBadgeClass(t.classification?.priority)" class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ring-1">
                  {{ t.classification?.priority || '—' }}
                </span>
              </header>
              <p class="text-sm text-zinc-500 line-clamp-2">{{ t.body }}</p>
              <div class="mt-3 flex flex-wrap items-center gap-2 text-xs">
                <span class="badge" :class="intentBadge(t.classification?.intent)">{{ t.classification?.intent || '—' }}</span>
                <span class="badge" :class="sentimentBadge(t.classification?.sentiment)">{{ t.classification?.sentiment || '—' }}</span>
                <span class="text-zinc-400">•</span>
                <time class="text-zinc-500">{{ formatDate(t.created_at) }}</time>
              </div>
              <footer class="mt-3">
                <NuxtLink :to="`/tickets/${t.id}`" class="text-sm text-zinc-900 underline hover:no-underline dark:text-zinc-100">Open</NuxtLink>
              </footer>
            </article>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div class="flex flex-col items-center justify-between gap-3 sm:flex-row">
        <div class="text-sm text-zinc-500">Page {{ page }} / {{ totalPages }} · {{ total }} total</div>
        <div class="flex items-center gap-2">
          <button class="rounded-xl border border-zinc-300 px-3 py-2 text-sm hover:bg-zinc-50 disabled:opacity-40 dark:border-zinc-700 dark:hover:bg-zinc-900" :disabled="page <= 1" @click="prevPage">Prev</button>
          <button class="rounded-xl border border-zinc-300 px-3 py-2 text-sm hover:bg-zinc-50 disabled:opacity-40 dark:border-zinc-700 dark:hover:bg-zinc-900" :disabled="page >= totalPages" @click="nextPage">Next</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const router = useRouter()
const { get } = useApi()

/** THEME */
const isDark = ref<boolean>(false)
onMounted(() => {
  const saved = localStorage.getItem('theme') // 'dark' | 'light'
  isDark.value = saved ? saved === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches
  document.documentElement.classList.toggle('dark', isDark.value)
})
function toggleTheme() {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

/** WEBSOCKET REAL-TIME UPDATES */
const { isConnected, on } = useWebSocket()
const showNotification = ref(false)
const notificationMessage = ref('')
const notificationType = ref<'info' | 'success' | 'warning' | 'error'>('info')

// Debug: Watch connection status
watch(isConnected, (connected) => {
  console.log('🔌 WebSocket connection status:', connected ? 'CONNECTED' : 'DISCONNECTED')
})

// Handle new ticket creation
on('ticket_update', (message: any) => {
  console.log('🎯 Received ticket_update:', message)
  if (message.event === 'ticket_created') {
    console.log('📨 New ticket created:', message.data)
    // Refresh the list to show new ticket
    refresh()
    // Show notification
    showNotification.value = true
    notificationMessage.value = `New ticket: ${message.data.subject}`
    notificationType.value = 'info'
    setTimeout(() => { showNotification.value = false }, 3000)
  }
})

/** SEMANTIC SEARCH */
const { searchQuery, searchMode, searchResults, isSearching, searchError, search, debouncedSearch, clearSearch } = useTicketSearch()

// Handle high-priority alerts
on('high_priority_alert', (message: any) => {
  console.log('🚨 High priority ticket:', message.data)
  refresh()
  showNotification.value = true
  notificationMessage.value = `🚨 High priority ticket: ${message.data.subject}`
  notificationType.value = 'warning'
  setTimeout(() => { showNotification.value = false }, 5000)
})

// Handle ticket claimed
on('ticket_claimed', (message: any) => {
  console.log('👤 Ticket claimed:', message.ticket_id)
  refresh()
})

// Handle ticket released
on('ticket_released', (message: any) => {
  console.log('🔓 Ticket released:', message.ticket_id)
  refresh()
})

/** FILTER OPTIONS */
const intentOptions = [
  'billing','refund_cancellation','account_management','auth_login','bug_issue','usage_howto','feature_request'
]
const sentimentOptions = ['negative','neutral','positive']
const priorityOptions = ['P1','P2','P3']

/** STATE */
const pageSize = ref(10)
const page = ref<number>(parseInt((route.query.page as string) || '1'))
const filters = reactive({
  intent: (route.query.intent as string) || '',
  sentiment: (route.query.sentiment as string) || '',
  priority: (route.query.priority as string) || '',
})
const error = ref<string | null>(null)

/** DATA FETCH */
const { data, pending, refresh } = useAsyncData(
  () => `tickets-${page.value}-${JSON.stringify(filters)}`,
  async () => {
    error.value = null
    try {
      const params: any = {
        page: page.value,
        page_size: pageSize.value,
      }
      if (filters.intent) params.intent = [filters.intent]
      if (filters.sentiment) params.sentiment = [filters.sentiment]
      if (filters.priority) params.priority = [filters.priority]
      return await get<any>('/tickets', params)
    } catch (e: any) {
      error.value = e?.data?.detail?.message || 'Failed to load tickets.'
      return { items: [], total: 0, page: page.value, page_size: pageSize.value }
    }
  },
  { immediate: true, watch: [page, filters] }
)

const items = computed(() => {
  // If search results exist, show them instead of regular tickets
  if (searchResults.value.length > 0) {
    return searchResults.value.map((result: any) => result.ticket)
  }
  return data.value?.items || []
})
const total = computed(() => {
  if (searchResults.value.length > 0) {
    return searchResults.value.length
  }
  return data.value?.total || 0
})
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))
const activeFilterCount = computed(() => {
  let count = 0
  if (filters.intent) count++
  if (filters.sentiment) count++
  if (filters.priority) count++
  return count
})

/** ACTIONS */
function refreshList() {
  router.replace({
    query: {
      page: String(page.value),
      ...(filters.intent ? { intent: filters.intent } : {}),
      ...(filters.sentiment ? { sentiment: filters.sentiment } : {}),
      ...(filters.priority ? { priority: filters.priority } : {}),
    },
  })
  refresh()
}
function resetFilters() {
  filters.intent = ''
  filters.sentiment = ''
  filters.priority = ''
  page.value = 1
  refreshList()
}
function nextPage() {
  if (page.value < totalPages.value) {
    page.value += 1
    refreshList()
  }
}
function prevPage() {
  if (page.value > 1) {
    page.value -= 1
    refreshList()
  }
}

/** HELPERS */
function toArray(q: unknown): string[] {
  if (q == null) return []
  return Array.isArray(q) ? q.map(String) : [String(q)]
}
function formatDate(iso: string) {
  try { return new Date(iso).toLocaleString() } catch { return '—' }
}

/** BADGE CLASSES */
function intentBadge(val?: string) {
  if (!val) return 'badge-muted'
  if (val === 'feature_request') return 'badge-sky'
  if (val === 'bug_issue') return 'badge-rose'
  if (val === 'billing' || val === 'refund_cancellation') return 'badge-amber'
  return 'badge-muted'
}
function sentimentBadge(val?: string) {
  if (val === 'positive') return 'badge-emerald'
  if (val === 'negative') return 'badge-rose'
  if (val === 'neutral')  return 'badge-muted'
  return 'badge-muted'
}
function priorityBadgeClass(priority?: string): string {
  switch (priority) {
    case 'P1': return 'bg-rose-50 text-rose-700 ring-rose-200 dark:bg-rose-900/20 dark:text-rose-300 dark:ring-rose-800'
    case 'P2': return 'bg-amber-50 text-amber-700 ring-amber-200 dark:bg-amber-900/20 dark:text-amber-300 dark:ring-amber-800'
    case 'P3': return 'bg-sky-50 text-sky-700 ring-sky-200 dark:bg-sky-900/20 dark:text-sky-300 dark:ring-sky-800'
    default:   return 'bg-zinc-100 text-zinc-700 ring-zinc-200 dark:bg-zinc-800 dark:text-zinc-300 dark:ring-zinc-700'
  }
}
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden;
}
.line-clamp-2 {
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}
/* tiny badge utilities using Tailwind tokens */
.badge { @apply inline-flex items-center rounded-full px-2 py-0.5 text-xs ring-1; }
.badge-muted   { @apply bg-zinc-100 text-zinc-700 ring-zinc-200 dark:bg-zinc-800 dark:text-zinc-300 dark:ring-zinc-700; }
.badge-rose    { @apply bg-rose-50 text-rose-700 ring-rose-200 dark:bg-rose-900/20 dark:text-rose-300 dark:ring-rose-800; }
.badge-amber   { @apply bg-amber-50 text-amber-700 ring-amber-200 dark:bg-amber-900/20 dark:text-amber-300 dark:ring-amber-800; }
.badge-sky     { @apply bg-sky-50 text-sky-700 ring-sky-200 dark:bg-sky-900/20 dark:text-sky-300 dark:ring-sky-800; }
.badge-emerald { @apply bg-emerald-50 text-emerald-700 ring-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-300 dark:ring-emerald-800; }

/* Notification transition */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}
.slide-down-enter-from {
  transform: translateY(-100%);
  opacity: 0;
}
.slide-down-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}
</style>