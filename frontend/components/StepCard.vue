<template>
  <div 
    :class="[
      'step-card rounded-xl shadow-lg overflow-hidden cursor-pointer transition-all duration-300',
      active ? 'ring-4 ring-blue-500 scale-[1.02]' : 'hover:shadow-xl'
    ]"
    @click="$emit('click')">
    <!-- Header -->
    <div 
      :class="[
        'p-6 flex items-center gap-4',
        active ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white' : 'bg-gradient-to-r from-gray-100 to-gray-50 text-gray-700'
      ]">
      <div 
        :class="[
          'w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg',
          active ? 'bg-white text-blue-600' : 'bg-white text-gray-700'
        ]">
        {{ step }}
      </div>
      <div class="flex-1">
        <h3 class="text-xl font-bold">{{ title }}</h3>
      </div>
      <div :class="active ? 'text-white' : 'text-gray-400'">
        <slot name="icon" />
      </div>
    </div>

    <!-- Content (expanded when active) -->
    <transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="max-h-0 opacity-0"
      enter-to-class="max-h-[1000px] opacity-100"
      leave-active-class="transition-all duration-300 ease-in"
      leave-from-class="max-h-[1000px] opacity-100"
      leave-to-class="max-h-0 opacity-0">
      <div v-if="active" class="p-6 bg-white border-t">
        <slot name="content" />
      </div>
    </transition>

    <!-- Collapsed Preview -->
    <div v-if="!active" class="p-4 bg-gray-50 text-center">
      <span class="text-sm text-gray-500">Click to expand</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  step: number
  title: string
  active: boolean
}>()

defineEmits<{
  (e: 'click'): void
}>()
</script>

<style scoped>
.step-card {
  transition: all 0.3s ease;
}
</style>
