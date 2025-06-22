<template>
  <div class="relative flex items-center">
    <slot></slot>
    <svg @mouseenter="show=true" @mouseleave="show=false" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-1 text-text-light hover:text-primary-blue cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M12 2a10 10 0 100 20 10 10 0 000-20z" />
    </svg>
    <div v-if="show" class="absolute bottom-full mb-2 left-1/2 transform -translate-x-1/2 w-48 bg-card-dark text-text-light text-sm p-2 rounded shadow-lg z-10">
      {{ text }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps({ text: { type: String, required: true } })
const show = ref(false)
</script>

<style scoped>
/* optional arrow via ::after */
</style>
