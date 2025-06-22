<template>
  <span :class="badgeClass" class="px-2 py-1 rounded-full text-sm">
    {{ status }}
  </span>
</template>

<script setup>
const props = defineProps({
  status: { type: String, required: true }
})
import { computed } from 'vue'
const badgeClass = computed(() => {
  switch (props.status) {
    case 'Implemented':
    case 'Compliant':
    case 'Low':
      return 'bg-green-600 text-white'
    case 'Partially Implemented':
    case 'Medium':
      return 'bg-yellow-600 text-white'
    case 'Not Implemented':
    case 'High':
      return 'bg-red-600 text-white'
    default:
      return 'bg-gray-600 text-white'
  }
})
</script>

<style scoped>
/* optionally adjust styling */
</style>
