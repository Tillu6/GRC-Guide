<template>
  <div class="space-y-6">
    <h1 class="text-4xl font-extrabold text-center text-primary-blue mb-8">Compliance Assessment</h1>
    <div v-if="loading" class="animate-pulse space-y-4">
      <div class="h-6 bg-gray-700 rounded w-1/3 mx-auto"></div>
      <div v-for="n in 5" :key="n" class="h-10 bg-gray-700 rounded w-full"></div>
    </div>
    <div v-else>
      <div v-for="control in controls" :key="control.id" class="bg-card-dark p-4 rounded-lg shadow mb-4 transition-transform hover:scale-102">
        <p class="font-semibold">{{ control.id }}: {{ control.name }}</p>
        <p class="text-sm text-muted-gray mb-2">{{ control.description }}</p>
        <div class="flex items-center space-x-4">
          <label class="flex items-center space-x-2">
            <input type="radio" :name="control.id" value="Implemented" v-model="statuses[control.id]" />
            <span>Implemented</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" :name="control.id" value="Partially Implemented" v-model="statuses[control.id]" />
            <span>Partially</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="radio" :name="control.id" value="Not Implemented" v-model="statuses[control.id]" />
            <span>Not Implemented</span>
          </label>
        </div>
      </div>
      <div class="text-center">
        <button @click="submit" class="btn-primary">Submit Assessment</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchControls, postAssessCompliance } from '@/api'

const controls = ref([])
const statuses = ref({})
const loading = ref(true)

onMounted(async () => {
  try {
    const data = await fetchControls()
    controls.value = data
    // initialize statuses
    data.forEach(c => { statuses.value[c.id] = 'Not Implemented' })
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

async function submit() {
  const payload = controls.value.map(c => ({ id: c.id, status: statuses.value[c.id] }))
  try {
    await postAssessCompliance(payload)
    alert('Assessment submitted!')
  } catch (e) {
    console.error(e)
    alert('Failed to submit')
  }
}
</script>

<style scoped>
/* you can add transitions on radio group changes if desired */
</style>
