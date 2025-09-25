<template>
  <div class="mx-auto max-w-4xl p-6 space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-semibold">Ticket</h1>
      <NuxtLink to="/compose" class="text-sm underline">New ticket</NuxtLink>
    </div>

    <div v-if="pendingTicket">Loading ticket…</div>
    <div v-else-if="ticketError" class="text-red-600">Failed to load ticket.</div>
    <div v-else class="space-y-4">
      <!-- Ticket Card -->
      <div class="border rounded p-4">
        <div class="flex items-center justify-between gap-4">
          <h2 class="text-lg font-medium">{{ ticket.subject }}</h2>
          <div class="flex items-center gap-2">
            <span v-if="ticket.classification?.low_confidence" class="text-xs px-2 py-1 bg-yellow-100 text-yellow-800 rounded">Needs review</span>
            <PriorityBadge :priority="ticket.classification?.priority" />
          </div>
        </div>
        <p class="text-sm text-gray-500 mt-1">
          Channel: <strong>{{ ticket.channel || '—' }}</strong> ·
          Customer: <strong>{{ ticket.customer_id || '—' }}</strong> ·
          Created: <strong>{{ new Date(ticket.created_at).toLocaleString() }}</strong>
        </p>
        <p class="mt-3 whitespace-pre-wrap">{{ ticket.body }}</p>

        <div class="mt-3 text-sm text-gray-700">
          <span class="mr-3">Intent: <strong>{{ ticket.classification?.intent || '—' }}</strong></span>
          <span class="mr-3">Sentiment: <strong>{{ ticket.classification?.sentiment || '—' }}</strong></span>
          <span>Confidence: <strong>{{ ticket.classification?.confidence?.toFixed?.(2) ?? '—' }}</strong></span>
        </div>
      </div>

      <!-- Suggestions -->
      <div class="border rounded p-4">
        <div class="flex items-center justify-between">
          <h3 class="font-medium">Suggested replies</h3>
          <button class="text-sm underline" @click="refetchSuggestions">Refresh</button>
        </div>

        <div v-if="pendingSug">Loading suggestions…</div>
        <div v-else-if="sugError" class="text-red-600">Failed to load suggestions.</div>
        <div v-else-if="!suggestions?.length" class="text-gray-600">No suggestions yet.</div>
        <div v-else class="space-y-3">
          <div v-for="s in suggestions" :key="s.id" class="border rounded p-3">
            <div class="flex items-center justify-between">
              <div class="font-medium">{{ s.title }}</div>
              <div class="text-xs text-gray-500">score: {{ s.score?.toFixed?.(3) }}</div>
            </div>
            <p class="text-sm mt-1">{{ s.preview }}</p>
            <div class="mt-2">
              <button class="text-sm bg-gray-100 px-2 py-1 rounded" @click="copy(s.preview)">Copy</button>
            </div>
          </div>
        </div>
      </div>

      <!-- (Optional) Resolutions -->
      <div class="border rounded p-4">
        <div class="flex items-center justify-between">
          <h3 class="font-medium">Past resolutions</h3>
          <button class="text-sm underline" @click="refetchResolutions">Refresh</button>
        </div>
        <div v-if="pendingRes">Loading…</div>
        <div v-else-if="resError" class="text-red-600">Failed to load resolutions.</div>
        <div v-else-if="!resolutions?.length" class="text-gray-600">No resolutions yet.</div>
        <ul v-else class="list-disc pl-5 space-y-1">
          <li v-for="r in resolutions" :key="r.id">
            <span class="font-medium">{{ r.summary }}</span> — {{ r.details }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const id = route.params.id as string
const { get } = useApi()

// ticket
const { data: ticket, pending: pendingTicket, error: ticketError, refresh: refetchTicket } =
  useAsyncData(`ticket-${id}`, () => get<any>(`/tickets/${id}`), { immediate: true })

// suggestions
const { data: suggestions, pending: pendingSug, error: sugError, refresh: refetchSuggestions } =
  useAsyncData(`sug-${id}`, () => get<any[]>(`/suggestions/${id}`), { immediate: true })

// resolutions (optional)
const { data: resolutions, pending: pendingRes, error: resError, refresh: refetchResolutions } =
  useAsyncData(`res-${id}`, () => get<any[]>(`/resolutions`, { ticket_id: id }), { immediate: true })

function copy(text: string) {
  navigator.clipboard?.writeText(text)
}
</script>

<script lang="ts">
export default {
  components: {
    PriorityBadge: {
      props: { priority: { type: String, default: '' } },
      template: `
        <span v-if="priority" :class="badgeClass" class="text-xs font-medium px-2 py-1 rounded">
          {{ priority }}
        </span>
      `,
      computed: {
        badgeClass(): string {
          switch (this.priority) {
            case 'P1': return 'bg-red-100 text-red-800'
            case 'P2': return 'bg-amber-100 text-amber-800'
            case 'P3': return 'bg-gray-100 text-gray-700'
            default: return 'bg-gray-100 text-gray-700'
          }
        }
      }
    }
  }
}
</script>
