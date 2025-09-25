<template>
  <div class="min-h-screen bg-white text-zinc-900 dark:bg-zinc-950 dark:text-zinc-100">
    <div class="mx-auto max-w-2xl p-6 space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <NuxtLink
            to="/"
            class="inline-flex items-center gap-2 rounded-xl border border-zinc-300 px-3 py-2 text-sm hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-900"
          >
            ← Back
          </NuxtLink>
          <h1 class="text-2xl font-semibold tracking-tight">Compose Ticket</h1>
        </div>

        <!-- Theme toggle (same as index) -->
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

      <!-- Form card -->
      <form class="space-y-5 rounded-2xl border border-zinc-200 p-5 dark:border-zinc-800 bg-white/70 dark:bg-zinc-900/60"
            @submit.prevent="submit" @keydown.ctrl.enter.prevent="submit">
        <div>
          <label class="mb-1 block text-sm font-medium text-zinc-600 dark:text-zinc-300">
            Subject <span class="text-rose-500">*</span>
          </label>
          <input
            v-model.trim="form.subject"
            :class="inputClass"
            placeholder="Short summary"
            required
            maxlength="140"
          />
          <div class="mt-1 text-xs text-zinc-500">{{ form.subject.length }}/140</div>
        </div>

        <div>
          <label class="mb-1 block text-sm font-medium text-zinc-600 dark:text-zinc-300">
            Body <span class="text-rose-500">*</span>
          </label>
          <textarea
            v-model.trim="form.body"
            :class="inputClass + ' min-h-[10rem]'"
            placeholder="Describe the issue…"
            required
          />
          <p class="mt-1 text-xs text-zinc-500">Tip: press <kbd class="rounded border px-1 text-[11px]">Ctrl</kbd>+<kbd class="rounded border px-1 text-[11px]">Enter</kbd> to submit</p>
        </div>

        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label class="mb-1 block text-sm font-medium text-zinc-600 dark:text-zinc-300">Channel</label>
            <select v-model="form.channel" :class="inputClass">
              <option value="email">email</option>
              <option value="web">web</option>
              <option value="chat">chat</option>
            </select>
          </div>

          <div>
            <label class="mb-1 block text-sm font-medium text-zinc-600 dark:text-zinc-300">Customer ID</label>
            <input v-model.trim="form.customer_id" :class="inputClass" placeholder="cust_123" />
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-3 pt-2">
          <button
            :disabled="loading"
            class="inline-flex items-center gap-2 rounded-xl bg-zinc-900 px-4 py-2 text-sm font-medium text-white hover:bg-zinc-800 disabled:opacity-50 dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
          >
            <svg v-if="loading" class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/>
            </svg>
            {{ loading ? 'Creating…' : 'Create Ticket' }}
          </button>

          <button type="button"
            class="rounded-xl border border-zinc-300 px-4 py-2 text-sm hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-800"
            @click="clearForm"
            :disabled="loading">
            Clear
          </button>

          <span v-if="error" class="text-sm text-rose-600">{{ error }}</span>
          <span v-if="success" class="text-sm text-emerald-600">Created!</span>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
const router = useRouter()
const { post } = useApi()

/** THEME (same as index) */
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

/** FORM */
const form = reactive({
  subject: '',
  body: '',
  channel: 'email',
  customer_id: ''
})
const loading = ref(false)
const error = ref<string | null>(null)
const success = ref(false)

const inputClass =
  'w-full rounded-xl border border-zinc-300 bg-white px-3 py-2 text-sm outline-none ring-zinc-900/10 ' +
  'focus:ring-4 dark:border-zinc-700 dark:bg-zinc-800 dark:focus:ring-zinc-300/10'

async function submit() {
  error.value = null
  success.value = false

  if (!form.subject || !form.body) {
    error.value = 'Subject and body are required.'
    return
  }

  try {
    loading.value = true
    const res = await post<{ id: string }>('/tickets', form)
    success.value = true
    await router.push(`/tickets/${res.id}`)
  } catch (e: any) {
    error.value = e?.data?.detail?.message || 'Failed to create ticket.'
  } finally {
    loading.value = false
  }
}

function clearForm() {
  form.subject = ''
  form.body = ''
  form.channel = 'email'
  form.customer_id = ''
  error.value = null
  success.value = false
}
</script>

<style scoped>
/* Small kbd styling (works in light/dark) */
kbd { @apply border-zinc-300 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-200; }
</style>

