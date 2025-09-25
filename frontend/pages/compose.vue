<template>
  <div class="mx-auto max-w-2xl p-6 space-y-6">
    <h1 class="text-2xl font-semibold">Compose Ticket</h1>

    <form class="space-y-4" @submit.prevent="submit">
      <div>
        <label class="block text-sm font-medium mb-1">Subject *</label>
        <input v-model="form.subject" required class="w-full border rounded px-3 py-2" placeholder="Short summary" />
      </div>

      <div>
        <label class="block text-sm font-medium mb-1">Body *</label>
        <textarea v-model="form.body" required rows="6" class="w-full border rounded px-3 py-2" placeholder="Describe the issue..."/>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium mb-1">Channel</label>
          <select v-model="form.channel" class="w-full border rounded px-3 py-2">
            <option value="email">email</option>
            <option value="web">web</option>
            <option value="chat">chat</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Customer ID</label>
          <input v-model="form.customer_id" class="w-full border rounded px-3 py-2" placeholder="cust_123" />
        </div>
      </div>

      <div class="flex items-center gap-3">
        <button :disabled="loading" class="bg-black text-white px-4 py-2 rounded">
          {{ loading ? 'Creating…' : 'Create Ticket' }}
        </button>
        <span v-if="error" class="text-red-600 text-sm">{{ error }}</span>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
const router = useRouter()
const { post } = useApi()

const form = reactive({
  subject: '',
  body: '',
  channel: 'email',
  customer_id: ''
})

const loading = ref(false)
const error = ref<string | null>(null)

async function submit() {
  error.value = null
  if (!form.subject || !form.body) {
    error.value = 'Subject and Body are required.'
    return
  }
  try {
    loading.value = true
    const res = await post<{ id: string }>('/tickets', form)
    await router.push(`/tickets/${res.id}`)
  } catch (e: any) {
    error.value = e?.data?.detail?.message || 'Failed to create ticket.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* minimal styles; feel free to replace with a UI kit later */
</style>
