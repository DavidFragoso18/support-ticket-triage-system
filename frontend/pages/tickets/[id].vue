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

          <!-- AI Response Suggestion -->
          <div class="mt-4 border-t border-zinc-200 pt-4 dark:border-zinc-800">
            <div class="flex items-start justify-between gap-4 mb-3">
              <div>
                <h3 class="text-sm font-semibold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-purple-600 dark:text-purple-400" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2a1 1 0 0 1 .894.553l2.5 5 5.5.798a1 1 0 0 1 .555 1.706l-4 3.898.944 5.5a1 1 0 0 1-1.45 1.054L12 18.3l-4.943 2.609a1 1 0 0 1-1.45-1.054l.944-5.5-4-3.898a1 1 0 0 1 .555-1.706l5.5-.798 2.5-5A1 1 0 0 1 12 2Z"/>
                  </svg>
                  AI Response Suggestion
                </h3>
                <p class="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">
                  Generate intelligent response using similar tickets and KB articles
                </p>
              </div>
              <div class="flex items-center gap-2">
                <select v-model="responseTone" class="rounded-lg border border-zinc-300 px-2 py-1 text-xs dark:border-zinc-700 dark:bg-zinc-800">
                  <option value="professional">Professional</option>
                  <option value="friendly">Friendly</option>
                  <option value="technical">Technical</option>
                  <option value="empathetic">Empathetic</option>
                </select>
                <button
                  @click="generateResponse"
                  :disabled="generatingResponse"
                  class="inline-flex items-center gap-1.5 rounded-lg border border-purple-200 px-3 py-1.5 text-sm text-purple-700 hover:bg-purple-50 disabled:opacity-50 dark:border-purple-800 dark:text-purple-400 dark:hover:bg-purple-900/20"
                >
                  <svg v-if="generatingResponse" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2a1 1 0 0 1 .894.553l2.5 5 5.5.798a1 1 0 0 1 .555 1.706l-4 3.898.944 5.5a1 1 0 0 1-1.45 1.054L12 18.3l-4.943 2.609a1 1 0 0 1-1.45-1.054l.944-5.5-4-3.898a1 1 0 0 1 .555-1.706l5.5-.798 2.5-5A1 1 0 0 1 12 2Z"/>
                  </svg>
                  {{ generatingResponse ? 'Generating...' : 'Generate Response' }}
                </button>
              </div>
            </div>
            
            <!-- Response Preview -->
            <div v-if="suggestedResponse" class="space-y-3">
              <div class="rounded-lg border border-purple-200 bg-purple-50/50 p-4 dark:border-purple-800 dark:bg-purple-900/10">
                <div class="flex items-start justify-between gap-3 mb-2">
                  <div class="text-xs text-purple-700 dark:text-purple-400 font-medium">
                    Suggested Response ({{ responseInfo?.tone }} tone, {{ responseInfo?.context_used }} sources)
                  </div>
                  <button
                    @click="suggestedResponse = null"
                    class="text-purple-600 hover:text-purple-800 dark:text-purple-400 dark:hover:text-purple-300"
                    title="Clear suggestion"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M18.3 5.71a1 1 0 0 0-1.42 0L12 10.59 7.12 5.71a1 1 0 1 0-1.42 1.42L10.59 12l-4.89 4.88a1 1 0 1 0 1.42 1.42L12 13.41l4.88 4.89a1 1 0 0 0 1.42-1.42L13.41 12l4.89-4.88a1 1 0 0 0 0-1.42Z"/>
                    </svg>
                  </button>
                </div>
                <textarea
                  v-model="suggestedResponse"
                  rows="8"
                  class="w-full rounded-lg border border-purple-200 bg-white px-3 py-2 text-sm dark:border-purple-700 dark:bg-zinc-900"
                  placeholder="Response suggestion will appear here..."
                ></textarea>
                <div class="flex gap-2 mt-3">
                  <button
                    @click="copyResponse"
                    class="inline-flex items-center gap-1.5 rounded-lg border border-zinc-300 px-3 py-1.5 text-sm hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-800"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M16 1H4a2 2 0 0 0-2 2v14h2V3h12V1zm3 4H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zm0 16H8V7h11v14z"/>
                    </svg>
                    {{ copiedResponse ? 'Copied!' : 'Copy to Clipboard' }}
                  </button>
                  <button
                    @click="saveResponse"
                    :disabled="savingResponse"
                    class="inline-flex items-center gap-1.5 rounded-lg border border-emerald-300 px-3 py-1.5 text-sm text-emerald-700 hover:bg-emerald-50 disabled:opacity-50 dark:border-emerald-800 dark:text-emerald-400 dark:hover:bg-emerald-900/20"
                  >
                    <svg v-if="savingResponse" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <svg v-else-if="responseSaved" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M14.72 8.79l-4.29 4.3-1.65-1.65a1 1 0 1 0-1.41 1.41l2.35 2.36a1 1 0 0 0 1.41 0l5-5a1 1 0 0 0-1.41-1.42Z"/>
                      <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8Z"/>
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M17 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14c1.1 0 2-.9 2-2V7l-4-4zm-5 16c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm3-10H5V5h10v4z"/>
                    </svg>
                    {{ responseSaved ? 'Saved!' : savingResponse ? 'Saving...' : 'Save Response' }}
                  </button>
                  <button
                    class="inline-flex items-center gap-1.5 rounded-lg bg-purple-600 px-3 py-1.5 text-sm text-white hover:bg-purple-700"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4h2v4h14v-4h2zm-1-4l-1.41-1.41L13 15.17V3h-2v12.17l-5.58-5.59L4 11l8 8 8-8z"/>
                    </svg>
                    Send Response (Coming Soon)
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Error Display -->
            <div v-if="responseError" class="rounded-lg border border-rose-200 bg-rose-50 p-3 text-sm text-rose-700 dark:border-rose-900/40 dark:bg-rose-900/20 dark:text-rose-400">
              {{ responseError }}
            </div>
          </div>

          <!-- Saved AI Responses History -->
          <div v-if="savedResponses && savedResponses.length > 0" class="mt-4 border-t border-zinc-200 pt-4 dark:border-zinc-800">
            <div class="flex items-center justify-between mb-3">
              <h3 class="text-sm font-semibold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-purple-600 dark:text-purple-400" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zm-7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2zM7 7h10v2H7V7zm0 4h10v2H7v-2zm0 4h7v2H7v-2z"/>
                </svg>
                Saved AI Responses ({{ savedResponses.length }})
              </h3>
              <button
                @click="refreshSavedResponses"
                class="text-xs text-purple-600 hover:text-purple-700 dark:text-purple-400"
              >
                Refresh
              </button>
            </div>
            
            <div class="space-y-2">
              <div
                v-for="(response, idx) in savedResponses"
                :key="response.id"
                class="rounded-lg border border-zinc-200 p-3 dark:border-zinc-700"
              >
                <div class="flex items-start justify-between gap-3 mb-2">
                  <div class="flex items-center gap-2 text-xs">
                    <span class="inline-flex items-center gap-1 rounded-full bg-purple-100 px-2 py-0.5 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2a1 1 0 0 1 .894.553l2.5 5 5.5.798a1 1 0 0 1 .555 1.706l-4 3.898.944 5.5a1 1 0 0 1-1.45 1.054L12 18.3l-4.943 2.609a1 1 0 0 1-1.45-1.054l.944-5.5-4-3.898a1 1 0 0 1 .555-1.706l5.5-.798 2.5-5A1 1 0 0 1 12 2Z"/>
                      </svg>
                      {{ response.tone }}
                    </span>
                    <span class="text-zinc-500 dark:text-zinc-400">
                      {{ response.model }}
                    </span>
                    <span v-if="response.was_edited" class="inline-flex items-center gap-1 text-amber-600 dark:text-amber-400">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04a1 1 0 0 0 0-1.41l-2.34-2.34a1 1 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                      </svg>
                      Edited
                    </span>
                    <span v-if="response.was_sent" class="inline-flex items-center gap-1 text-emerald-600 dark:text-emerald-400">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                      </svg>
                      Sent
                    </span>
                  </div>
                  <span class="text-xs text-zinc-400">
                    {{ formatDate(response.created_at) }}
                  </span>
                </div>
                <p class="text-sm text-zinc-700 dark:text-zinc-300 line-clamp-3">
                  {{ response.response_text }}
                </p>
                <button
                  @click="expandedResponseId = expandedResponseId === response.id ? null : response.id"
                  class="mt-2 text-xs text-purple-600 hover:text-purple-700 dark:text-purple-400"
                >
                  {{ expandedResponseId === response.id ? 'Show less' : 'Show full response' }}
                </button>
                
                <!-- Expanded view -->
                <div v-if="expandedResponseId === response.id" class="mt-3 pt-3 border-t border-zinc-200 dark:border-zinc-700">
                  <pre class="text-sm text-zinc-700 dark:text-zinc-300 whitespace-pre-wrap font-sans">{{ response.response_text }}</pre>
                  <div class="mt-3 flex gap-2">
                    <button
                      @click="copyToClipboard(response.response_text)"
                      class="inline-flex items-center gap-1.5 rounded-lg border border-zinc-300 px-2 py-1 text-xs hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-800"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M16 1H4a2 2 0 0 0-2 2v14h2V3h12V1zm3 4H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2zm0 16H8V7h11v14z"/>
                      </svg>
                      Copy
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Feedback section -->
          <div v-if="ticket.classification" class="mt-4 border-t border-zinc-200 pt-4 dark:border-zinc-800">
            <div class="flex items-center justify-between gap-4">
              <div class="text-sm text-zinc-600 dark:text-zinc-400">
                Is this classification correct?
              </div>
              <div class="flex items-center gap-2">
                <button
                  @click="submitFeedback('accepted')"
                  :disabled="feedbackSubmitting"
                  class="inline-flex items-center gap-1.5 rounded-lg border border-emerald-200 px-3 py-1.5 text-sm text-emerald-700 hover:bg-emerald-50 disabled:opacity-50 dark:border-emerald-800 dark:text-emerald-400 dark:hover:bg-emerald-900/20"
                  title="Accept classification"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M14.72 8.79l-4.29 4.3-1.65-1.65a1 1 0 1 0-1.41 1.41l2.35 2.36a1 1 0 0 0 1.41 0l5-5a1 1 0 0 0-1.41-1.42Z"/>
                    <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8Z"/>
                  </svg>
                  Accept
                </button>
                <button
                  @click="showCorrectionModal = true"
                  :disabled="feedbackSubmitting"
                  class="inline-flex items-center gap-1.5 rounded-lg border border-amber-200 px-3 py-1.5 text-sm text-amber-700 hover:bg-amber-50 disabled:opacity-50 dark:border-amber-800 dark:text-amber-400 dark:hover:bg-amber-900/20"
                  title="Correct classification"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34a.9959.9959 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                  </svg>
                  Correct
                </button>
                <button
                  @click="submitFeedback('rejected')"
                  :disabled="feedbackSubmitting"
                  class="inline-flex items-center gap-1.5 rounded-lg border border-rose-200 px-3 py-1.5 text-sm text-rose-700 hover:bg-rose-50 disabled:opacity-50 dark:border-rose-800 dark:text-rose-400 dark:hover:bg-rose-900/20"
                  title="Reject classification"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                  </svg>
                  Reject
                </button>
              </div>
            </div>
            <div v-if="feedbackSuccess" class="mt-2 text-sm text-emerald-600 dark:text-emerald-400">
              ✓ Feedback submitted successfully!
            </div>
            <div v-if="feedbackError" class="mt-2 text-sm text-rose-600 dark:text-rose-400">
              ✗ {{ feedbackError }}
            </div>
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
                <div class="flex-1">
                  <div class="font-medium">{{ s.title }}</div>
                  <div class="text-xs text-zinc-500 mt-1">
                    {{ s.type === 'kb_article' ? 'KB Article' : 'Resolution Template' }} · score: {{ s.score?.toFixed?.(3) }}
                  </div>
                </div>
                <button
                  @click="applySuggestion(s)"
                  :disabled="applyingId === s.id"
                  class="shrink-0 rounded-lg bg-emerald-600 px-3 py-1.5 text-sm text-white hover:bg-emerald-700 disabled:opacity-50"
                >
                  {{ applyingId === s.id ? 'Applying...' : 'Apply' }}
                </button>
              </div>
              <p class="mt-2 text-sm text-zinc-600 dark:text-zinc-300">{{ s.preview }}</p>
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

      <!-- Correction Modal -->
      <div v-if="showCorrectionModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" @click.self="showCorrectionModal = false">
        <div class="w-full max-w-md rounded-2xl border border-zinc-200 bg-white p-6 shadow-xl dark:border-zinc-800 dark:bg-zinc-900">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold">Correct Classification</h3>
            <button @click="showCorrectionModal = false" class="text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
          </div>

          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-1">Intent</label>
              <select v-model="correctedIntent" class="w-full rounded-lg border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-800">
                <option value="">-- Keep original --</option>
                <option value="general_inquiry">General Inquiry</option>
                <option value="bug_issue">Bug/Issue</option>
                <option value="feature_request">Feature Request</option>
                <option value="billing">Billing</option>
                <option value="refund_cancellation">Refund/Cancellation</option>
                <option value="account_access">Account Access</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium mb-1">Sentiment</label>
              <select v-model="correctedSentiment" class="w-full rounded-lg border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-800">
                <option value="">-- Keep original --</option>
                <option value="positive">Positive</option>
                <option value="neutral">Neutral</option>
                <option value="negative">Negative</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium mb-1">Priority</label>
              <select v-model="correctedPriority" class="w-full rounded-lg border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-800">
                <option value="">-- Keep original --</option>
                <option value="P1">P1 - Critical</option>
                <option value="P2">P2 - High</option>
                <option value="P3">P3 - Normal</option>
                <option value="P4">P4 - Low</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium mb-1">Notes (optional)</label>
              <textarea v-model="correctionNotes" rows="3" class="w-full rounded-lg border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-800" placeholder="Add any notes..."></textarea>
            </div>

            <div class="flex gap-2 justify-end">
              <button @click="showCorrectionModal = false" class="rounded-lg border border-zinc-300 px-4 py-2 text-sm hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-800">
                Cancel
              </button>
              <button @click="submitCorrection" :disabled="feedbackSubmitting" class="rounded-lg bg-amber-600 px-4 py-2 text-sm text-white hover:bg-amber-700 disabled:opacity-50">
                Submit Correction
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Similar Tickets -->
      <div v-if="similarTickets && similarTickets.length > 0" class="rounded-2xl border border-zinc-200 p-5 dark:border-zinc-800 bg-white/70 dark:bg-zinc-900/60">
        <h3 class="text-lg font-semibold flex items-center gap-2 mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600 dark:text-blue-400" viewBox="0 0 24 24" fill="currentColor">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm-1 2l5 5h-5V4zM8 18v-1h8v1H8zm0-4v-1h8v1H8zm0-4v-1h5v1H8z"/>
          </svg>
          Similar Tickets
        </h3>
        
        <div v-if="similarPending" class="space-y-3">
          <div v-for="i in 3" :key="i" class="animate-pulse rounded-lg border border-zinc-200 p-3 dark:border-zinc-700">
            <div class="h-4 w-3/4 bg-zinc-100 rounded dark:bg-zinc-800"></div>
            <div class="mt-2 h-3 w-1/2 bg-zinc-100 rounded dark:bg-zinc-800"></div>
          </div>
        </div>

        <div v-else class="space-y-3">
          <NuxtLink
            v-for="similar in similarTickets"
            :key="similar.id"
            :to="`/tickets/${similar.id}`"
            class="block rounded-lg border border-zinc-200 p-3 hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-800/50 transition-colors"
          >
            <div class="flex items-start justify-between gap-3">
              <div class="flex-1 min-w-0">
                <h4 class="font-medium text-sm text-zinc-900 dark:text-zinc-100 truncate">
                  {{ similar.subject }}
                </h4>
                <p class="mt-1 text-xs text-zinc-500 dark:text-zinc-400 line-clamp-2">
                  {{ similar.preview }}
                </p>
                <p class="mt-1 text-xs text-zinc-400">
                  {{ new Date(similar.created_at).toLocaleDateString() }}
                </p>
              </div>
              <div class="flex-shrink-0">
                <span class="inline-flex items-center gap-1 rounded-full bg-blue-100 px-2 py-0.5 text-xs font-medium text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                  {{ (similar.similarity * 100).toFixed(0) }}%
                </span>
              </div>
            </div>
          </NuxtLink>
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

// Similar Tickets
const similarReq = () => $fetch<any>(`/api/tickets/${id}/similar`, { server: true })
const { data: similarData, pending: similarPending } =
  useAsyncData(`similar-${id}`, similarReq, { immediate: true })

const similarTickets = computed(() => similarData.value?.similar_tickets || [])

// Saved AI Responses
const savedResponsesReq = () => $fetch<any>(`/api/llm/saved-responses/${id}`)
const { data: savedResponses, refresh: refreshSavedResponses } =
  useAsyncData(`saved-responses-${id}`, savedResponsesReq, { immediate: true })

const expandedResponseId = ref<string | null>(null)

/** LLM RESPONSE SUGGESTION */
const responseTone = ref('professional')
const suggestedResponse = ref<string | null>(null)
const responseInfo = ref<any>(null)
const generatingResponse = ref(false)
const responseError = ref<string | null>(null)
const copiedResponse = ref(false)
const savingResponse = ref(false)
const responseSaved = ref(false)
const originalResponse = ref<string | null>(null)

async function generateResponse() {
  generatingResponse.value = true
  responseError.value = null
  suggestedResponse.value = null
  responseSaved.value = false
  
  try {
    const data = await $fetch<any>(`/api/llm/suggest-response/${id}`, {
      query: { tone: responseTone.value }
    })
    
    suggestedResponse.value = data.response
    originalResponse.value = data.response  // Store original for edit tracking
    responseInfo.value = {
      tone: data.tone,
      context_used: data.context_used,
      model: data.model
    }
  } catch (error: any) {
    console.error('Failed to generate response:', error)
    responseError.value = error.data?.error || 'Failed to generate response suggestion. Make sure Ollama is running with a model loaded.'
  } finally {
    generatingResponse.value = false
  }
}

async function copyResponse() {
  if (suggestedResponse.value) {
    try {
      await navigator.clipboard.writeText(suggestedResponse.value)
      copiedResponse.value = true
      setTimeout(() => { copiedResponse.value = false }, 2000)
    } catch (error) {
      console.error('Failed to copy:', error)
    }
  }
}

async function saveResponse() {
  if (!suggestedResponse.value || !responseInfo.value) return
  
  savingResponse.value = true
  responseError.value = null
  
  try {
    const wasEdited = suggestedResponse.value !== originalResponse.value
    
    await $fetch('/api/llm/save-response', {
      method: 'POST',
      body: {
        ticket_id: id,
        response_text: suggestedResponse.value,
        tone: responseInfo.value.tone,
        context_used: responseInfo.value.context_used,
        model: responseInfo.value.model,
        agent_id: 'demo-agent',  // TODO: Replace with actual user ID
        was_edited: wasEdited
      }
    })
    
    responseSaved.value = true
    // Refresh saved responses list
    await refreshSavedResponses()
    setTimeout(() => { responseSaved.value = false }, 3000)
  } catch (error: any) {
    console.error('Failed to save response:', error)
    responseError.value = 'Failed to save response. Please try again.'
    setTimeout(() => { responseError.value = null }, 5000)
  } finally {
    savingResponse.value = false
  }
}

function copyToClipboard(text: string) {
  navigator.clipboard.writeText(text)
}

function formatDate(dateStr: string) {
  try {
    const date = new Date(dateStr)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    
    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffMins < 1440) return `${Math.floor(diffMins / 60)}h ago`
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch {
    return dateStr
  }
}

/** APPLY SUGGESTION */
const applyingId = ref<string | null>(null)

async function applySuggestion(suggestion: any) {
  applyingId.value = suggestion.id
  
  try {
    await $fetch('/api/resolutions/apply', {
      method: 'POST',
      body: {
        ticket_id: id,
        suggestion_id: suggestion.id,
        suggestion_type: suggestion.type,
        agent_id: 'current-user' // TODO: Replace with actual user ID
      }
    })
    
    // Refresh resolutions list to show the new resolution
    await resRefresh()
    
    // Show success feedback
    feedbackSuccess.value = true
    setTimeout(() => { feedbackSuccess.value = false }, 3000)
  } catch (error: any) {
    console.error('Failed to apply suggestion:', error)
    feedbackError.value = error.data?.detail?.message || 'Failed to apply suggestion'
    setTimeout(() => { feedbackError.value = null }, 5000)
  } finally {
    applyingId.value = null
  }
}

/** FEEDBACK */
const showCorrectionModal = ref(false)
const feedbackSubmitting = ref(false)
const feedbackSuccess = ref(false)
const feedbackError = ref<string | null>(null)
const correctedIntent = ref('')
const correctedSentiment = ref('')
const correctedPriority = ref('')
const correctionNotes = ref('')

async function submitFeedback(action: 'accepted' | 'rejected') {
  if (!ticket.value?.classification?.id) return
  
  feedbackSubmitting.value = true
  feedbackSuccess.value = false
  feedbackError.value = null

  try {
    await $fetch('/api/feedback', {
      method: 'POST',
      body: {
        classification_id: ticket.value.classification.id,
        action,
        agent_id: 'demo-agent', // In production, use actual user ID
      }
    })
    feedbackSuccess.value = true
    setTimeout(() => feedbackSuccess.value = false, 3000)
  } catch (error: any) {
    feedbackError.value = error.data?.message || 'Failed to submit feedback'
    setTimeout(() => feedbackError.value = null, 5000)
  } finally {
    feedbackSubmitting.value = false
  }
}

async function submitCorrection() {
  if (!ticket.value?.classification?.id) return
  
  feedbackSubmitting.value = true
  feedbackSuccess.value = false
  feedbackError.value = null

  try {
    await $fetch('/api/feedback', {
      method: 'POST',
      body: {
        classification_id: ticket.value.classification.id,
        action: 'corrected',
        corrected_intent: correctedIntent.value || undefined,
        corrected_sentiment: correctedSentiment.value || undefined,
        corrected_priority: correctedPriority.value || undefined,
        notes: correctionNotes.value || undefined,
        agent_id: 'demo-agent', // In production, use actual user ID
      }
    })
    feedbackSuccess.value = true
    showCorrectionModal.value = false
    // Reset form
    correctedIntent.value = ''
    correctedSentiment.value = ''
    correctedPriority.value = ''
    correctionNotes.value = ''
    setTimeout(() => feedbackSuccess.value = false, 3000)
  } catch (error: any) {
    feedbackError.value = error.data?.message || 'Failed to submit correction'
    setTimeout(() => feedbackError.value = null, 5000)
  } finally {
    feedbackSubmitting.value = false
  }
}

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
