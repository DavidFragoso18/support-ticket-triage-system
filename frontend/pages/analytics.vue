<template>
  <div class="min-h-screen bg-white text-zinc-900 dark:bg-zinc-950 dark:text-zinc-100">
    <div class="mx-auto max-w-7xl p-6 space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between flex-wrap gap-4">
        <div class="flex items-center gap-3">
          <NuxtLink
            to="/tickets"
            class="inline-flex items-center gap-2 rounded-xl border border-zinc-300 px-3 py-2 text-sm hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-900"
          >← Back to tickets</NuxtLink>
          <h1 class="text-2xl font-semibold tracking-tight">Analytics Dashboard</h1>
        </div>

        <div class="flex items-center gap-2">
          <!-- Date Range Selector -->
          <select 
            v-model="selectedDays"
            class="rounded-xl border border-zinc-300 px-3 py-2 text-sm bg-white dark:bg-zinc-900 dark:border-zinc-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option v-for="option in dayOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>

          <!-- Theme Toggle -->
          <button
            class="inline-flex items-center gap-2 rounded-xl border border-zinc-300 px-3 py-2 text-sm hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-900"
            @click="toggleTheme"
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
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="space-y-4">
        <div class="h-32 w-full animate-pulse rounded-2xl bg-zinc-100 dark:bg-zinc-800"></div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="h-48 animate-pulse rounded-2xl bg-zinc-100 dark:bg-zinc-800"></div>
          <div class="h-48 animate-pulse rounded-2xl bg-zinc-100 dark:bg-zinc-800"></div>
          <div class="h-48 animate-pulse rounded-2xl bg-zinc-100 dark:bg-zinc-800"></div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="rounded-2xl border border-rose-200 bg-rose-50 p-6 text-rose-700 dark:border-rose-900/40 dark:bg-rose-900/20">
        Failed to load analytics data. Please try again.
      </div>

      <!-- Dashboard Content -->
      <div v-else class="space-y-6">
        <!-- Overview Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="rounded-2xl border border-zinc-200 p-5 dark:border-zinc-800 bg-gradient-to-br from-blue-50 to-blue-100/50 dark:from-blue-900/20 dark:to-blue-800/10">
            <div class="text-sm font-medium text-blue-700 dark:text-blue-400">Total Tickets</div>
            <div class="mt-2 text-3xl font-bold text-blue-900 dark:text-blue-100">{{ overview?.total_tickets || 0 }}</div>
            <div class="mt-1 text-xs text-blue-600 dark:text-blue-400">+{{ overview?.tickets_today || 0 }} today</div>
          </div>

          <div class="rounded-2xl border border-zinc-200 p-5 dark:border-zinc-800 bg-gradient-to-br from-emerald-50 to-emerald-100/50 dark:from-emerald-900/20 dark:to-emerald-800/10">
            <div class="text-sm font-medium text-emerald-700 dark:text-emerald-400">Avg Confidence</div>
            <div class="mt-2 text-3xl font-bold text-emerald-900 dark:text-emerald-100">{{ (overview?.avg_confidence * 100 || 0).toFixed(1) }}%</div>
            <div class="mt-1 text-xs text-emerald-600 dark:text-emerald-400">Model predictions</div>
          </div>

          <div class="rounded-2xl border border-zinc-200 p-5 dark:border-zinc-800 bg-gradient-to-br from-amber-50 to-amber-100/50 dark:from-amber-900/20 dark:to-amber-800/10">
            <div class="text-sm font-medium text-amber-700 dark:text-amber-400">Low Confidence</div>
            <div class="mt-2 text-3xl font-bold text-amber-900 dark:text-amber-100">{{ overview?.low_confidence_count || 0 }}</div>
            <div class="mt-1 text-xs text-amber-600 dark:text-amber-400">Need review</div>
          </div>

          <div class="rounded-2xl border border-zinc-200 p-5 dark:border-zinc-800 bg-gradient-to-br from-purple-50 to-purple-100/50 dark:from-purple-900/20 dark:to-purple-800/10">
            <div class="text-sm font-medium text-purple-700 dark:text-purple-400">Human Feedback</div>
            <div class="mt-2 text-3xl font-bold text-purple-900 dark:text-purple-100">{{ overview?.feedback_count || 0 }}</div>
            <div class="mt-1 text-xs text-purple-600 dark:text-purple-400">Total submissions</div>
          </div>
        </div>

        <!-- Classification Accuracy -->
        <div class="rounded-2xl border border-zinc-200 p-6 dark:border-zinc-800 bg-white/70 dark:bg-zinc-900/60">
          <h2 class="text-lg font-semibold mb-4">Model Performance</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-sm font-medium">Intent Accuracy</span>
                <span class="text-lg font-bold text-blue-600 dark:text-blue-400">{{ (accuracy?.intent_accuracy * 100 || 0).toFixed(1) }}%</span>
              </div>
              <div class="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-2.5">
                <div class="bg-blue-600 h-2.5 rounded-full" :style="{ width: `${(accuracy?.intent_accuracy * 100 || 0)}%` }"></div>
              </div>
              <div class="text-xs text-zinc-500">
                Accepted: {{ accuracy?.intent_accepted || 0 }} / Corrected: {{ accuracy?.intent_corrected || 0 }}
              </div>
            </div>

            <div class="space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-sm font-medium">Sentiment Accuracy</span>
                <span class="text-lg font-bold text-emerald-600 dark:text-emerald-400">{{ (accuracy?.sentiment_accuracy * 100 || 0).toFixed(1) }}%</span>
              </div>
              <div class="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-2.5">
                <div class="bg-emerald-600 h-2.5 rounded-full" :style="{ width: `${(accuracy?.sentiment_accuracy * 100 || 0)}%` }"></div>
              </div>
              <div class="text-xs text-zinc-500">
                Accepted: {{ accuracy?.sentiment_accepted || 0 }} / Corrected: {{ accuracy?.sentiment_corrected || 0 }}
              </div>
            </div>

            <div class="space-y-2">
              <div class="flex justify-between items-center">
                <span class="text-sm font-medium">Priority Accuracy</span>
                <span class="text-lg font-bold text-purple-600 dark:text-purple-400">{{ (accuracy?.priority_accuracy * 100 || 0).toFixed(1) }}%</span>
              </div>
              <div class="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-2.5">
                <div class="bg-purple-600 h-2.5 rounded-full" :style="{ width: `${(accuracy?.priority_accuracy * 100 || 0)}%` }"></div>
              </div>
              <div class="text-xs text-zinc-500">
                Accepted: {{ accuracy?.priority_accepted || 0 }} / Corrected: {{ accuracy?.priority_corrected || 0 }}
              </div>
            </div>
          </div>

          <div class="mt-6 pt-6 border-t border-zinc-200 dark:border-zinc-800">
            <div class="flex items-center justify-between">
              <div>
                <div class="text-sm font-medium">Overall Model Accuracy</div>
                <div class="text-xs text-zinc-500 mt-1">Based on {{ accuracy?.total_feedback || 0 }} human feedback submissions</div>
              </div>
              <div class="text-3xl font-bold" :class="{
                'text-emerald-600 dark:text-emerald-400': (accuracy?.overall_accuracy || 0) >= 0.8,
                'text-amber-600 dark:text-amber-400': (accuracy?.overall_accuracy || 0) >= 0.6 && (accuracy?.overall_accuracy || 0) < 0.8,
                'text-rose-600 dark:text-rose-400': (accuracy?.overall_accuracy || 0) < 0.6
              }">
                {{ (accuracy?.overall_accuracy * 100 || 0).toFixed(1) }}%
              </div>
            </div>
          </div>
        </div>

        <!-- Distribution Charts -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Intent Distribution -->
          <div class="rounded-2xl border border-zinc-200 p-6 dark:border-zinc-800 bg-white/70 dark:bg-zinc-900/60">
            <h3 class="text-base font-semibold mb-4">Intent Distribution</h3>
            <div class="space-y-3">
              <div v-for="item in intentDist" :key="item.intent" class="space-y-1">
                <div class="flex justify-between text-sm">
                  <span class="font-medium">{{ formatIntentLabel(item.intent) }}</span>
                  <span class="text-zinc-500">{{ item.count }}</span>
                </div>
                <div class="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-2">
                  <div class="bg-blue-500 h-2 rounded-full" :style="{ width: `${item.percentage}%` }"></div>
                </div>
              </div>
              <div v-if="!intentDist?.length" class="text-sm text-zinc-500 text-center py-4">
                No data available
              </div>
            </div>
          </div>

          <!-- Sentiment Distribution -->
          <div class="rounded-2xl border border-zinc-200 p-6 dark:border-zinc-800 bg-white/70 dark:bg-zinc-900/60">
            <h3 class="text-base font-semibold mb-4">Sentiment Distribution</h3>
            <div class="space-y-3">
              <div v-for="item in sentimentDist" :key="item.sentiment" class="space-y-1">
                <div class="flex justify-between text-sm">
                  <span class="font-medium capitalize">{{ item.sentiment }}</span>
                  <span class="text-zinc-500">{{ item.count }}</span>
                </div>
                <div class="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-2">
                  <div class="h-2 rounded-full" :class="{
                    'bg-emerald-500': item.sentiment === 'positive',
                    'bg-zinc-400': item.sentiment === 'neutral',
                    'bg-rose-500': item.sentiment === 'negative'
                  }" :style="{ width: `${item.percentage}%` }"></div>
                </div>
              </div>
              <div v-if="!sentimentDist?.length" class="text-sm text-zinc-500 text-center py-4">
                No data available
              </div>
            </div>
          </div>

          <!-- Priority Distribution -->
          <div class="rounded-2xl border border-zinc-200 p-6 dark:border-zinc-800 bg-white/70 dark:bg-zinc-900/60">
            <h3 class="text-base font-semibold mb-4">Priority Distribution</h3>
            <div class="space-y-3">
              <div v-for="item in priorityDist" :key="item.priority" class="space-y-1">
                <div class="flex justify-between text-sm">
                  <span class="font-medium">{{ item.priority }}</span>
                  <span class="text-zinc-500">{{ item.count }}</span>
                </div>
                <div class="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-2">
                  <div class="h-2 rounded-full" :class="{
                    'bg-rose-500': item.priority === 'P1',
                    'bg-amber-500': item.priority === 'P2',
                    'bg-blue-500': item.priority === 'P3',
                    'bg-zinc-400': item.priority === 'P4'
                  }" :style="{ width: `${item.percentage}%` }"></div>
                </div>
              </div>
              <div v-if="!priorityDist?.length" class="text-sm text-zinc-500 text-center py-4">
                No data available
              </div>
            </div>
          </div>
        </div>

        <!-- Ticket Trends -->
        <div class="rounded-2xl border border-zinc-200 p-6 dark:border-zinc-800 bg-white/70 dark:bg-zinc-900/60">
          <h2 class="text-lg font-semibold mb-4">Ticket Trends</h2>
          <div class="space-y-2">
            <div class="grid grid-cols-7 gap-1">
              <div v-for="(trend, index) in trends" :key="index" class="space-y-1">
                <!-- Date label -->
                <div class="text-xs text-center text-zinc-500">{{ formatDate(trend.date) }}</div>
                
                <!-- Bar chart -->
                <div class="relative h-32 flex items-end justify-center">
                  <div class="flex flex-col-reverse gap-0.5 w-full">
                    <!-- Total tickets bar -->
                    <div 
                      class="bg-blue-500 rounded-t transition-all duration-300 hover:bg-blue-600"
                      :style="{ height: `${Math.max((trend.total_tickets / Math.max(...trends.map((t: any) => t.total_tickets), 1)) * 100, 2)}%` }"
                      :title="`${trend.total_tickets} total tickets`"
                    ></div>
                  </div>
                </div>
                
                <!-- Count label -->
                <div class="text-xs text-center font-semibold">{{ trend.total_tickets }}</div>
              </div>
            </div>

            <!-- Legend -->
            <div class="flex items-center justify-center gap-4 pt-4 text-xs">
              <div class="flex items-center gap-1.5">
                <div class="w-3 h-3 bg-blue-500 rounded"></div>
                <span>Total Tickets</span>
              </div>
              <div class="flex items-center gap-1.5">
                <div class="w-3 h-3 bg-rose-500 rounded"></div>
                <span>High Priority</span>
              </div>
              <div class="flex items-center gap-1.5">
                <div class="w-3 h-3 bg-emerald-500 rounded"></div>
                <span>Resolved</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Top Agents Performance -->
        <div class="rounded-2xl border border-zinc-200 p-6 dark:border-zinc-800 bg-white/70 dark:bg-zinc-900/60">
          <h2 class="text-lg font-semibold mb-4">Top Agent Performance</h2>
          
          <div v-if="topAgents.length > 0" class="space-y-4">
            <div v-for="(agent, index) in topAgents" :key="agent.agent_id" 
              class="rounded-xl border border-zinc-200 p-4 dark:border-zinc-700 hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors">
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-3">
                  <!-- Rank badge -->
                  <div class="flex items-center justify-center w-8 h-8 rounded-full font-bold text-sm" :class="{
                    'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400': index === 0,
                    'bg-zinc-200 text-zinc-600 dark:bg-zinc-700 dark:text-zinc-300': index === 1,
                    'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400': index === 2,
                    'bg-zinc-100 text-zinc-500 dark:bg-zinc-800 dark:text-zinc-400': index > 2
                  }">
                    #{{ index + 1 }}
                  </div>
                  
                  <!-- Agent info -->
                  <div>
                    <div class="font-semibold">{{ agent.agent_id }}</div>
                    <div class="text-xs text-zinc-500">
                      {{ agent.tickets_claimed }} claimed · {{ agent.tickets_resolved }} resolved
                    </div>
                  </div>
                </div>
                
                <!-- Resolution rate -->
                <div class="text-right">
                  <div class="text-lg font-bold" :class="{
                    'text-emerald-600 dark:text-emerald-400': (agent.tickets_resolved / agent.tickets_claimed) >= 0.8,
                    'text-amber-600 dark:text-amber-400': (agent.tickets_resolved / agent.tickets_claimed) >= 0.5 && (agent.tickets_resolved / agent.tickets_claimed) < 0.8,
                    'text-zinc-600 dark:text-zinc-400': (agent.tickets_resolved / agent.tickets_claimed) < 0.5
                  }">
                    {{ agent.tickets_claimed > 0 ? Math.round((agent.tickets_resolved / agent.tickets_claimed) * 100) : 0 }}%
                  </div>
                  <div class="text-xs text-zinc-500">Resolution rate</div>
                </div>
              </div>

              <!-- Performance metrics -->
              <div class="grid grid-cols-2 gap-3 text-sm">
                <div class="flex items-center gap-2 text-zinc-600 dark:text-zinc-400">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>Avg: {{ formatDuration(agent.avg_resolution_time_seconds) }}</span>
                </div>
                
                <div class="flex items-center gap-2 text-zinc-600 dark:text-zinc-400">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                  </svg>
                  <span>{{ agent.avg_feedback_rating.toFixed(1) }} / 5.0</span>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-8 text-zinc-500">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-2 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <p>No agent activity in the selected time period</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Date range for analytics
const selectedDays = ref(7)
const dayOptions = [
  { value: 7, label: 'Last 7 days' },
  { value: 14, label: 'Last 14 days' },
  { value: 30, label: 'Last 30 days' },
  { value: 90, label: 'Last 90 days' }
]

// Fetch comprehensive dashboard data
const { data: dashboardData, error: dashboardError, refresh: refreshDashboard } = await useFetch<any>(
  () => `/api/analytics/dashboard?days=${selectedDays.value}`
)

const loading = ref(false)
const error = computed(() => dashboardError.value)

// Extract data from dashboard response
const overview = computed(() => dashboardData.value?.overview)
const accuracy = computed(() => dashboardData.value?.model_accuracy)
const intentDist = computed(() => dashboardData.value?.intent_distribution || [])
const sentimentDist = computed(() => dashboardData.value?.sentiment_distribution || [])
const priorityDist = computed(() => dashboardData.value?.priority_distribution || [])
const trends = computed(() => dashboardData.value?.trends || [])
const topAgents = computed(() => dashboardData.value?.top_agents || [])

// Watch for days change and refresh
watch(selectedDays, () => {
  refreshDashboard()
})

// Theme toggle
const isDark = ref<boolean>(false)
onMounted(() => {
  isDark.value = document.documentElement.classList.contains('dark')
})

function toggleTheme() {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

// Helper functions
function formatIntentLabel(intent: string): string {
  return intent
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function formatDuration(seconds: number): string {
  if (seconds < 60) return `${Math.round(seconds)}s`
  if (seconds < 3600) return `${Math.round(seconds / 60)}m`
  return `${(seconds / 3600).toFixed(1)}h`
}

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}
</script>
