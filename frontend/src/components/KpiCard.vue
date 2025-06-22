<template>
  <div
    v-tilt
    class="bg-card-dark p-6 rounded-lg shadow-lg transform transition-transform duration-300 hover:scale-105"
  >
    <div class="flex items-center justify-between">
      <div>
        <p class="text-sm text-muted-gray">{{ title }}</p>
        <p class="text-2xl font-bold mt-1">{{ value }}</p>
      </div>
      <div class="text-4xl">{{ icon }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
  icon: String
})
</script>

<style scoped>
/* Additional card-specific styles if needed */
</style>
