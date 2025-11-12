<template>
  <div class="pipeline-container">
    <!-- Pipeline Flow -->
    <div class="relative">
      <!-- Connection Lines -->
      <svg class="absolute inset-0 w-full h-full pointer-events-none" style="z-index: 0;">
        <defs>
          <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
            <polygon points="0 0, 10 3, 0 6" fill="#3B82F6" />
          </marker>
        </defs>
        <!-- Lines connecting steps -->
        <line v-for="i in 7" :key="i"
          :x1="`${(i - 1) * 12.5 + 6.25}%`" y1="50%"
          :x2="`${i * 12.5 + 6.25}%`" y2="50%"
          :stroke="currentStep > i ? '#3B82F6' : '#E5E7EB'"
          stroke-width="3"
          :class="{'animated-line': currentStep === i + 1}"
          marker-end="url(#arrowhead)" />
      </svg>

      <!-- Steps -->
      <div class="grid grid-cols-8 gap-2 relative" style="z-index: 1;">
        <div v-for="step in steps" :key="step.number"
          class="flex flex-col items-center cursor-pointer transform hover:scale-105 transition-transform"
          @click="$emit('step-click', step.number)">
          <!-- Step Circle -->
          <div 
            :class="[
              'w-16 h-16 rounded-full flex items-center justify-center mb-2 shadow-lg',
              currentStep === step.number 
                ? 'bg-blue-600 text-white ring-4 ring-blue-200 scale-110' 
                : currentStep > step.number
                ? 'bg-blue-500 text-white'
                : 'bg-gray-200 text-gray-400'
            ]"
            class="transition-all duration-300">
            <span class="text-2xl">{{ step.icon }}</span>
          </div>
          
          <!-- Step Label -->
          <div class="text-center">
            <div 
              :class="[
                'text-xs font-semibold mb-1',
                currentStep === step.number ? 'text-blue-600' : 'text-gray-600'
              ]">
              Step {{ step.number }}
            </div>
            <div 
              :class="[
                'text-xs font-medium',
                currentStep === step.number ? 'text-gray-900' : 'text-gray-500'
              ]">
              {{ step.label }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Current Step Details -->
    <div class="mt-8 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 min-h-[120px]">
      <div class="flex items-start gap-4">
        <div class="text-5xl">{{ currentStepData.icon }}</div>
        <div class="flex-1">
          <h3 class="text-xl font-bold text-gray-900 mb-2">
            {{ currentStepData.label }}
          </h3>
          <p class="text-gray-700">
            {{ currentStepData.description }}
          </p>
        </div>
        
        <!-- Animated Processing Indicator -->
        <div v-if="currentStep <= 7" class="flex items-center gap-2">
          <div class="flex space-x-1">
            <div v-for="i in 3" :key="i"
              class="w-2 h-2 bg-blue-600 rounded-full animate-bounce"
              :style="{ animationDelay: `${i * 0.1}s` }">
            </div>
          </div>
          <span class="text-sm text-gray-600">Processing...</span>
        </div>
        <div v-else class="flex items-center gap-2 text-green-600">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <span class="text-sm font-semibold">Complete!</span>
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="mt-4 w-full bg-gray-200 rounded-full h-2">
        <div 
          class="bg-gradient-to-r from-blue-600 to-purple-600 h-2 rounded-full transition-all duration-500"
          :style="{ width: `${(currentStep / 8) * 100}%` }">
        </div>
      </div>
    </div>

    <!-- Step Navigation -->
    <div class="mt-6 flex items-center justify-between">
      <button
        @click="$emit('step-click', Math.max(1, currentStep - 1))"
        :disabled="currentStep === 1"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all',
          currentStep === 1 
            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
            : 'bg-blue-600 text-white hover:bg-blue-700'
        ]">
        ← Previous
      </button>
      
      <div class="text-sm text-gray-600">
        Step {{ currentStep }} of 8
      </div>
      
      <button
        @click="$emit('step-click', Math.min(8, currentStep + 1))"
        :disabled="currentStep === 8"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all',
          currentStep === 8
            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
            : 'bg-blue-600 text-white hover:bg-blue-700'
        ]">
        Next →
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  currentStep: number
}>()

defineEmits<{
  (e: 'step-click', step: number): void
}>()

const steps = [
  { number: 1, icon: '📧', label: 'Submit' },
  { number: 2, icon: '🎯', label: 'Intent' },
  { number: 3, icon: '😊', label: 'Sentiment' },
  { number: 4, icon: '⚡', label: 'Priority' },
  { number: 5, icon: '🔢', label: 'Embed' },
  { number: 6, icon: '🔍', label: 'Similar' },
  { number: 7, icon: '💡', label: 'Suggest' },
  { number: 8, icon: '📊', label: 'Display' },
]

const stepDescriptions = [
  { label: 'Ticket Submission', description: 'Customer submits a support ticket through email, chat, phone, or web form with subject and detailed description.' },
  { label: 'Intent Classification', description: 'AI analyzes the ticket using zero-shot classification to determine if it\'s a refund, billing, technical, or general inquiry.' },
  { label: 'Sentiment Analysis', description: 'AI evaluates the emotional tone (negative, neutral, positive) to understand customer frustration level.' },
  { label: 'Priority Assignment', description: 'Business rules combine intent and sentiment to automatically assign priority: urgent, high, medium, or low.' },
  { label: 'Vector Embedding', description: 'Ticket content is converted to a 384-dimensional vector that captures semantic meaning for similarity search.' },
  { label: 'Similar Ticket Search', description: 'Using cosine similarity, the system finds previously submitted tickets with similar issues to provide context.' },
  { label: 'Smart Suggestions', description: 'System recommends relevant KB articles and resolution templates based on classified intent and similar tickets.' },
  { label: 'Agent Dashboard', description: 'All information is displayed in an intuitive dashboard with filters, search, and actionable insights for agents.' },
]

const currentStepData = computed(() => ({
  ...steps[props.currentStep - 1],
  ...stepDescriptions[props.currentStep - 1],
}))
</script>

<style scoped>
.pipeline-container {
  position: relative;
}

@keyframes dash {
  to {
    stroke-dashoffset: 0;
  }
}

.animated-line {
  stroke-dasharray: 10;
  stroke-dashoffset: 100;
  animation: dash 1s linear infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-0.5rem);
  }
}

.animate-bounce {
  animation: bounce 1s infinite;
}
</style>
