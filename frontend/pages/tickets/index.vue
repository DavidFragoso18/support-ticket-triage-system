<template>
  <div class="min-h-screen bg-white text-zinc-900 dark:bg-zinc-950 dark:text-zinc-100">
    <div class="mx-auto max-w-6xl p-6 space-y-6">
      <!-- Header -->
      <div class="flex flex-wrap items-center justify-between gap-4">
        <h1 class="text-2xl font-semibold tracking-tight">Tickets</h1>

        <div class="flex items-center gap-3">
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
              <label class="mb-2 block text-xs font-medium text-zinc-500">Intent</label>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="opt in intentOptions" :key="opt"
                  @click="toggleFilter(filters.intent, opt)"
                  class="rounded-full border px-3 py-1 text-xs"
                  :class="filters.intent.includes(opt)
                    ? 'border-zinc-900 bg-zinc-900 text-white dark:border-white dark:bg-white dark:text-zinc-900'
                    : 'border-zinc-300 text-zinc-700 hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800'"
                >
                  {{ opt.replace('_',' ') }}
                </button>
              </div>
            </div>

            <!-- Sentiment -->
            <div>
              <label class="mb-2 block text-xs font-medium text-zinc-500">Sentiment</label>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="opt in sentimentOptions" :key="opt"
                  @click="toggleFilter(filters.sentiment, opt)"
                  class="rounded-full border px-3 py-1 text-xs"
                  :class="filters.sentiment.includes(opt)
                    ? 'border-zinc-900 bg-zinc-900 text-white dark:border-white dark:bg-white dark:text-zinc-900'
                    : 'border-zinc-300 text-zinc-700 hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800'"
                >
                  {{ opt }}
                </button>
              </div>
            </div>

            <!-- Priority -->
            <div>
              <label class="mb-2 block text-xs font-medium text-zinc-500">Priority</label>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="opt in priorityOptions" :key="opt"
                  @click="toggleFilter(filters.priority, opt)"
                  class="rounded-full border px-3 py-1 text-xs"
                  :class="filters.priority.includes(opt)
                    ? 'border-zinc-900 bg-zinc-900 text-white dark:border-white dark:bg-white dark:text-zinc-900'
                    : 'border-zinc-300 text-zinc-700 hover:bg-zinc-100 dark:border-zinc-700 dark:text-zinc-300 dark:hover:bg-zinc-800'"
                >
                  {{ opt }}
                </button>
              </div>
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
                  <PriorityBadge :priority="t.classification?.priority" />
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
                <PriorityBadge :priority="t.classification?.priority" />
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

/** FILTER OPTIONS */
const intentOptions = [
  'billing','auth_login','bug_issue','usage_howto','refund_cancellation','outage_status','feature_request','shipping_delivery','account_management'
]
const sentimentOptions = ['negative','neutral','positive']
const priorityOptions = ['P1','P2','P3']

/** STATE */
const pageSize = ref(10)
const page = ref<number>(parseInt((route.query.page as string) || '1'))
const filters = reactive({
  intent: ([] as string[]).concat(toArray(route.query.intent)),
  sentiment: ([] as string[]).concat(toArray(route.query.sentiment)),
  priority: ([] as string[]).concat(toArray(route.query.priority)),
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
      if (filters.intent.length) params.intent = filters.intent
      if (filters.sentiment.length) params.sentiment = filters.sentiment
      if (filters.priority.length) params.priority = filters.priority
      return await get<any>('/tickets', params)
    } catch (e: any) {
      error.value = e?.data?.detail?.message || 'Failed to load tickets.'
      return { items: [], total: 0, page: page.value, page_size: pageSize.value }
    }
  },
  { immediate: true, watch: [page, filters] }
)

const items = computed(() => data.value?.items || [])
const total = computed(() => data.value?.total || 0)
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))
const activeFilterCount = computed(() => filters.intent.length + filters.sentiment.length + filters.priority.length)

/** ACTIONS */
function toggleFilter(arr: string[], value: string) {
  const i = arr.indexOf(value)
  if (i === -1) arr.push(value)
  else arr.splice(i, 1)
}
function refreshList() {
  router.replace({
    query: {
      page: String(page.value),
      ...(filters.intent.length ? { intent: filters.intent } : {}),
      ...(filters.sentiment.length ? { sentiment: filters.sentiment } : {}),
      ...(filters.priority.length ? { priority: filters.priority } : {}),
    },
  })
  refresh()
}
function resetFilters() {
  filters.intent = []
  filters.sentiment = []
  filters.priority = []
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
</script>

<script lang="ts">
export default {
  components: {
    PriorityBadge: {
        props: { priority: { type: String, default: '' } },
        template: `
        <span :class="badgeClass" class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ring-1">
        {{ priority || '—' }}
        </span>
        `,
        computed: {
            badgeClass(): string {
                switch (this.priority) {
                    case 'P1': return 'bg-rose-50 text-rose-700 ring-rose-200 dark:bg-rose-900/20 dark:text-rose-300 dark:ring-rose-800'
                    case 'P2': return 'bg-amber-50 text-amber-700 ring-amber-200 dark:bg-amber-900/20 dark:text-amber-300 dark:ring-amber-800'
                    case 'P3': return 'bg-sky-50 text-sky-700 ring-sky-200 dark:bg-sky-900/20 dark:text-sky-300 dark:ring-sky-800'
                    default:   return 'bg-zinc-100 text-zinc-700 ring-zinc-200 dark:bg-zinc-800 dark:text-zinc-300 dark:ring-zinc-700'
                }
            }
        }
    }
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
</style>
