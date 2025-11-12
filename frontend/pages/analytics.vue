<template>
  <div class="min-h-screen bg-white text-zinc-900 dark:bg-zinc-950 dark:text-zinc-100">
    <div class="mx-auto max-w-7xl p-6 space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <NuxtLink
            to="/tickets"
            class="inline-flex items-center gap-2 rounded-xl border border-zinc-300 px-3 py-2 text-sm hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-900"
          >← Back to tickets</NuxtLink>
          <h1 class="text-2xl font-semibold tracking-tight">Analytics Dashboard</h1>
        </div>

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
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Fetch all analytics data
const { data: overview, error: overviewError } = await useFetch<any>('/api/analytics/overview')
const { data: accuracy, error: accuracyError } = await useFetch<any>('/api/analytics/classification-accuracy')
const { data: intentDist, error: intentError } = await useFetch<any>('/api/analytics/intent-distribution')
const { data: sentimentDist, error: sentimentError } = await useFetch<any>('/api/analytics/sentiment-distribution')
const { data: priorityDist, error: priorityError } = await useFetch<any>('/api/analytics/priority-distribution')

const loading = ref(false)
const error = computed(() => overviewError.value || accuracyError.value || intentError.value || sentimentError.value || priorityError.value)

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
</script>
