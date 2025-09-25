<template>
  <div class="min-h-screen bg-white text-zinc-900 dark:bg-zinc-950 dark:text-zinc-100">
    <div class="mx-auto max-w-4xl p-6 space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <NuxtLink
            to="/tickets"
            class="inline-flex items-center gap-2 rounded-xl border border-zinc-300 px-3 py-2 text-sm hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-900"
          >← Back to list</NuxtLink>
          <h1 class="text-2xl font-semibold tracking-tight">Ticket</h1>
        </div>

        <!-- Theme toggle (same as index/compose) -->
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
      </div>

      <!-- Ticket -->
      <div v-if="ticketPending" class="space-y-4">
        <div class="rounded-2xl border border-zinc-200 p-4 dark:border-zinc-800">
          <div class="h-6 w-2/3 animate-pulse rounded bg-zinc-100 dark:bg-zinc-800"></div>
          <div class="mt-2 h-4 w-1/2 animate-pulse rounded bg-zinc-100 dark:bg-zinc-800"></div>
          <div class="mt-4 h-20 w-full animate-pulse rounded bg-zinc-100 dark:bg-zinc-800"></div>
        </div>
      </div>

      <div v-else-if="ticketError" class="rounded-2xl border border-rose-200 bg-rose-50 p-4 text-rose-700 dark:border-rose-900/40 dark:bg-rose-900/20">
        Failed to load ticket.
      </div>

      <div v-else class="space-y-4">
        <div class="rounded-2xl border border-zinc-200 p-5 dark:border-zinc-800 bg-white/70 dark:bg-zinc-900/60">
          <div class="flex items-start justify-between gap-4">
            <div>
              <h2 class="text-lg font-semibold leading-tight">{{ ticket.subject }}</h2>
              <p class="mt-1 text-sm text-zinc-500">
                Channel: <strong class="text-zinc-700 dark:text-zinc-300">{{ ticket.channel || '—' }}</strong>
                <span class="text-zinc-400">·</span>
                Customer: <strong class="text-zinc-700 dark:text-zinc-300">{{ ticket.customer_id || '—' }}</strong>
                <span class="text-zinc-400">·</span>
                Created: <strong class="text-zinc-700 dark:text-zinc-300">{{ fmt(ticket.created_at) }}</strong>
              </p>
            </div>
            <PriorityBadge :priority="ticket.classification?.priority" />
          </div>

          <p class="mt-4 whitespace-pre-wrap text-[15px] leading-relaxed">
            {{ ticket.body }}
          </p>

          <div class="mt-4 flex flex-wrap items-center gap-2 text-xs">
            <span class="badge" :class="intentBadge(ticket.classification?.intent)">
              Intent: {{ ticket.classification?.intent || '—' }}
            </span>
            <span class="badge" :class="sentimentBadge(ticket.classification?.sentiment)">
              Sentiment: {{ ticket.classification?.sentiment || '—' }}
            </span>
            <span class="badge badge-muted">
              Confidence: {{ ticket.classification?.confidence?.toFixed?.(2) ?? '—' }}
            </span>
          </div>
        </div>

        <!-- Suggested replies -->
        <div class="rounded-2xl border border-zinc-200 p-5 dark:border-zinc-800 bg-white/70 dark:bg-zinc-900/60">
          <div class="mb-3 flex items-center justify-between">
            <h3 class="font-medium">Suggested replies</h3>
            <button class="text-sm underline underline-offset-2 hover:no-underline" @click="sugRefresh()">Refresh</button>
          </div>

          <div v-if="sugPending">
            <div class="h-5 w-1/2 animate-pulse rounded bg-zinc-100 dark:bg-zinc-800"></div>
          </div>
          <div v-else-if="sugError" class="text-rose-600">Failed to load suggestions.</div>
          <div v-else-if="!suggestions?.length" class="text-zinc-500">No suggestions.</div>
          <div v-else class="space-y-3">
            <div v-for="s in suggestions" :key="s.id" class="rounded-xl border border-zinc-200 p-4 dark:border-zinc-800">
              <div class="flex items-center justify-between gap-3">
                <div class="font-medium">{{ s.title }}</div>
                <div class="text-xs text-zinc-500">score: {{ s.score?.toFixed?.(3) }}</div>
              </div>
              <p class="mt-1 text-sm text-zinc-600 dark:text-zinc-300">{{ s.preview }}</p>
            </div>
          </div>
        </div>

        <!-- Past resolutions -->
        <div class="rounded-2xl border border-zinc-200 p-5 dark:border-zinc-800 bg-white/70 dark:bg-zinc-900/60">
          <div class="mb-3 flex items-center justify-between">
            <h3 class="font-medium">Past resolutions</h3>
            <button class="text-sm underline underline-offset-2 hover:no-underline" @click="resRefresh()">Refresh</button>
          </div>

          <div v-if="resPending">
            <div class="h-5 w-1/3 animate-pulse rounded bg-zinc-100 dark:bg-zinc-800"></div>
          </div>
          <div v-else-if="resError" class="text-rose-600">Failed to load resolutions.</div>

          <ul v-else-if="resolutions?.length" class="space-y-2">
            <li v-for="r in resolutions" :key="r.id" class="rounded-xl border border-zinc-200 p-4 dark:border-zinc-800">
              <span class="font-medium">{{ r.summary }}</span>
              <span class="text-zinc-400">—</span>
              <span class="text-zinc-700 dark:text-zinc-300">{{ r.details }}</span>
            </li>
          </ul>

          <div v-else class="text-zinc-500">No resolutions.</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const id = route.params.id as string

// Nuxt server proxies under /api
const ticketReq = () => $fetch<any>(`/api/tickets/${id}`, { server: true })
const sugReq    = () => $fetch<any[]>(`/api/suggestions/${id}`, { server: true })
const resReq    = () => $fetch<any[]>(`/api/resolutions`, { query: { ticket_id: id }, server: true })

// Ticket
const { data: ticket, pending: ticketPending, error: ticketError } =
  useAsyncData(`ticket-${id}`, ticketReq, { immediate: true })

// Suggestions
const { data: suggestions, pending: sugPending, error: sugError, refresh: sugRefresh } =
  useAsyncData(`sug-${id}`, sugReq, { immediate: true })

// Resolutions
const { data: resolutions, pending: resPending, error: resError, refresh: resRefresh } =
  useAsyncData(`res-${id}`, resReq, { immediate: true })

/** THEME (keep consistent across pages) */
const isDark = ref<boolean>(false)
onMounted(() => {
  const saved = localStorage.getItem('theme')
  isDark.value = saved ? saved === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches
  document.documentElement.classList.toggle('dark', isDark.value)
})
function toggleTheme() {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

/** HELPERS */
function fmt(iso?: string) { try { return new Date(iso!).toLocaleString() } catch { return '—' } }

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
        <span v-if="priority" :class="badgeClass" class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ring-1">
          {{ priority }}
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
/* badge utilities, same as index */
.badge { @apply inline-flex items-center rounded-full px-2 py-0.5 text-xs ring-1; }
.badge-muted   { @apply bg-zinc-100 text-zinc-700 ring-zinc-200 dark:bg-zinc-800 dark:text-zinc-300 dark:ring-zinc-700; }
.badge-rose    { @apply bg-rose-50 text-rose-700 ring-rose-200 dark:bg-rose-900/20 dark:text-rose-300 dark:ring-rose-800; }
.badge-amber   { @apply bg-amber-50 text-amber-700 ring-amber-200 dark:bg-amber-900/20 dark:text-amber-300 dark:ring-amber-800; }
.badge-sky     { @apply bg-sky-50 text-sky-700 ring-sky-200 dark:bg-sky-900/20 dark:text-sky-300 dark:ring-sky-800; }
.badge-emerald { @apply bg-emerald-50 text-emerald-700 ring-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-300 dark:ring-emerald-800; }
</style>
