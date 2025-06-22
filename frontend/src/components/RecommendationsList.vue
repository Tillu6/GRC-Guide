<template>
  <div class="space-y-6">
    <h1 class="text-4xl font-extrabold text-center text-primary-blue mb-8">Actionable Recommendations</h1>
    <div v-if="loading" class="text-center">Loading...</div>
    <div v-else-if="!recs.length">
      <EmptyStateIllustration message="No recommendations found." linkText="Go to Dashboard" linkTo="/" />
    </div>
    <div v-else>
      <ul class="space-y-4">
        <li v-for="(rec, idx) in recs" :key="idx" class="bg-card-dark p-4 rounded-lg shadow hover:scale-102 transition-transform">
          <p><strong>Type:</strong> {{ rec.type }}</p>
          <p><strong>Area:</strong> {{ rec.area }}</p>
          <p><strong>Item:</strong> {{ rec.item }}</p>
          <p><strong>Suggestion:</strong> {{ rec.suggestion }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import EmptyStateIllustration from './EmptyStateIllustration.vue'
import axios from 'axios'
const recs = ref([])
const loading = ref(true)
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
onMounted(async () => {
  try {
    const res = await axios.get(`${API_URL}/all-recommendations`)
    recs.value = res.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
</style>
