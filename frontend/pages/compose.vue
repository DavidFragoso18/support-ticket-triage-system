<template>
  <div class="min-h-screen bg-white text-zinc-900 dark:bg-zinc-950 dark:text-zinc-100">
    <div class="mx-auto max-w-4xl p-6 space-y-6">
      <!-- Header -->
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center gap-4">
          <NuxtLink
            to="/tickets"
            class="inline-flex items-center gap-2 rounded-xl border border-zinc-300 px-3 py-2 text-sm hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-900"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
              <path d="M7.825 13 18 13 18 11 7.825 11 12.125 6.7 10.7 5.3 4 12 10.7 18.7 12.125 17.3Z"/>
            </svg>
            Back to tickets
          </NuxtLink>
          <h1 class="text-2xl font-semibold tracking-tight flex items-center gap-2">
            🦈 GYM SHARK - New Ticket
          </h1>
        </div>

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
      </div>

      <!-- Form -->
      <div class="rounded-2xl border border-zinc-200 bg-white/70 p-6 dark:border-zinc-800 dark:bg-zinc-900/60">
        <form @submit.prevent="submitTicket" class="space-y-6">
          <!-- Subject -->
          <div>
            <label for="subject" class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
              Subject *
            </label>
            <input
              id="subject"
              v-model="form.subject"
              type="text"
              required
              placeholder="Brief description of the issue"
              class="w-full rounded-xl border border-zinc-300 px-4 py-3 text-sm focus:border-zinc-500 focus:outline-none focus:ring-2 focus:ring-zinc-500/20 dark:border-zinc-700 dark:bg-zinc-900 dark:focus:border-zinc-400"
            />
          </div>

          <!-- Customer ID -->
          <div>
            <label for="customer_id" class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
              Customer ID *
            </label>
            <input
              id="customer_id"
              v-model="form.customer_id"
              type="text"
              required
              placeholder="Customer identifier"
              class="w-full rounded-xl border border-zinc-300 px-4 py-3 text-sm focus:border-zinc-500 focus:outline-none focus:ring-2 focus:ring-zinc-500/20 dark:border-zinc-700 dark:bg-zinc-900 dark:focus:border-zinc-400"
            />
          </div>

          <!-- Channel -->
          <div>
            <label for="channel" class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
              Channel *
            </label>
            <select
              id="channel"
              v-model="form.channel"
              required
              class="w-full rounded-xl border border-zinc-300 px-4 py-3 text-sm focus:border-zinc-500 focus:outline-none focus:ring-2 focus:ring-zinc-500/20 dark:border-zinc-700 dark:bg-zinc-900 dark:focus:border-zinc-400"
            >
              <option value="">Select a channel</option>
              <option value="email">Email</option>
              <option value="chat">Chat</option>
              <option value="phone">Phone</option>
              <option value="social">Social Media</option>
              <option value="web">Web Form</option>
            </select>
          </div>

          <!-- Language -->
          <div>
            <label for="language" class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
              Language
            </label>
            <select
              id="language"
              v-model="form.language"
              class="w-full rounded-xl border border-zinc-300 px-4 py-3 text-sm focus:border-zinc-500 focus:outline-none focus:ring-2 focus:ring-zinc-500/20 dark:border-zinc-700 dark:bg-zinc-900 dark:focus:border-zinc-400"
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
              <option value="pt">Portuguese</option>
            </select>
          </div>

          <!-- Body -->
          <div>
            <label for="body" class="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
              Message *
            </label>
            <textarea
              id="body"
              v-model="form.body"
              required
              rows="8"
              placeholder="Detailed description of the issue or request..."
              class="w-full rounded-xl border border-zinc-300 px-4 py-3 text-sm focus:border-zinc-500 focus:outline-none focus:ring-2 focus:ring-zinc-500/20 dark:border-zinc-700 dark:bg-zinc-900 dark:focus:border-zinc-400"
            ></textarea>
          </div>

          <!-- Submit buttons -->
          <div class="flex items-center justify-end gap-3">
            <NuxtLink
              to="/tickets"
              class="inline-flex items-center gap-2 rounded-xl border border-zinc-300 px-4 py-2 text-sm hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-900"
            >
              Cancel
            </NuxtLink>
            <button
              type="submit"
              :disabled="isSubmitting"
              class="inline-flex items-center gap-2 rounded-xl bg-zinc-900 px-4 py-2 text-sm font-medium text-white hover:bg-zinc-800 disabled:opacity-50 disabled:cursor-not-allowed dark:bg-white dark:text-zinc-900 dark:hover:bg-zinc-200"
            >
              <svg v-if="isSubmitting" class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                <path d="M21 5.5L12.5 14 7 8.5 5.5 10l7 7L22.5 7 21 5.5Z"/>
              </svg>
              {{ isSubmitting ? 'Creating ticket...' : 'Create ticket' }}
            </button>
          </div>
        </form>

        <!-- Success message -->
        <div v-if="successMessage" class="mt-6 rounded-xl bg-green-50 border border-green-200 p-4 dark:bg-green-900/20 dark:border-green-800">
          <div class="flex items-center gap-3">
            <svg class="h-5 w-5 text-green-600 dark:text-green-400" viewBox="0 0 24 24" fill="currentColor">
              <path d="M21 5.5L12.5 14 7 8.5 5.5 10l7 7L22.5 7 21 5.5Z"/>
            </svg>
            <p class="text-sm text-green-800 dark:text-green-200">{{ successMessage }}</p>
          </div>
        </div>

        <!-- Error message -->
        <div v-if="errorMessage" class="mt-6 rounded-xl bg-red-50 border border-red-200 p-4 dark:bg-red-900/20 dark:border-red-800">
          <div class="flex items-center gap-3">
            <svg class="h-5 w-5 text-red-600 dark:text-red-400" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
            <p class="text-sm text-red-800 dark:text-red-200">{{ errorMessage }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const { apiBase } = useRuntimeConfig().public

// Theme management
const isDark = ref(false)
const toggleTheme = () => {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
}

// Initialize theme
onMounted(() => {
  isDark.value = document.documentElement.classList.contains('dark') || 
    (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
  document.documentElement.classList.toggle('dark', isDark.value)
})

// Form state
const form = ref({
  subject: '',
  body: '',
  channel: '',
  customer_id: '',
  language: 'en'
})

const isSubmitting = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

// Submit ticket
const submitTicket = async () => {
  isSubmitting.value = true
  successMessage.value = ''
  errorMessage.value = ''

  try {
    const response = await $fetch(`${apiBase}/tickets`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form.value)
    })

    successMessage.value = `Ticket created successfully! Ticket ID: ${response.id}`
    
    // Reset form
    form.value = {
      subject: '',
      body: '',
      channel: '',
      customer_id: '',
      language: 'en'
    }

    // Redirect to tickets after a delay
    setTimeout(() => {
      navigateTo('/tickets')
    }, 2000)

  } catch (error) {
    console.error('Error creating ticket:', error)
    errorMessage.value = error.data?.detail || 'Failed to create ticket. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

// SEO
useHead({
  title: 'Create New Ticket - GYM SHARK Support',
  meta: [
    { name: 'description', content: 'Create a new support ticket for GYM SHARK customer service' }
  ]
})
</script>