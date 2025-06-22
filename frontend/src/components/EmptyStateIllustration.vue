<template>
  <div class="text-center py-16">
    <img
      v-if="illustrationSrc"
      :src="illustrationSrc"
      alt="No data available"
      class="mx-auto w-40 mb-4 opacity-50"
    />
    <p class="text-lg text-text-light mb-2">{{ message }}</p>
    <router-link
      :to="linkTo"
      class="text-primary-blue hover:underline"
      aria-label="Navigate to {{ linkText }}"
    >
      {{ linkText }}
    </router-link>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  message: { type: String, required: true },
  linkText: { type: String, required: true },
  linkTo: { type: String, required: true },
  // If placed in public/, path is '/no-data-illustration.svg'
  illustration: { type: String, default: '/no-data-illustration.svg' }
})
// If you want to allow dynamic import from assets:
const illustrationSrc = computed(() => {
  // If illustration prop starts with '/', assume public path
  return props.illustration
})
</script>
