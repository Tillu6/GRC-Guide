<template>
  <div class="space-y-6">
    <h1 class="text-4xl font-extrabold text-center text-primary-blue mb-8">Risk Assessment</h1>
    <div class="mb-4">
      <button @click="addAsset" class="btn-primary">Add Asset</button>
    </div>
    <transition-group name="list" tag="div" class="space-y-4">
      <div v-for="(asset, idx) in assets" :key="asset.id" class="bg-card-dark p-4 rounded-lg shadow flex justify-between items-center">
        <div class="space-y-2">
          <p><strong>Name:</strong> <input v-model="asset.name" class="input-field" /></p>
          <p><strong>Impact (1-5):</strong> 
            <select v-model.number="asset.impact" class="input-field w-20">
              <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
            </select>
          </p>
          <p><strong>Likelihood (1-5):</strong> 
            <select v-model.number="asset.likelihood" class="input-field w-20">
              <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
            </select>
          </p>
        </div>
        <button @click="removeAsset(idx)" class="text-red-500 hover:text-red-700">Delete</button>
      </div>
    </transition-group>
    <div v-if="assets.length">
      <button @click="submitAssets" class="btn-primary">Assess Risk</button>
    </div>
    <div v-if="loading" class="mt-4 text-center">Loading...</div>
    <div v-if="result && result.risk_heatmap" class="mt-6 heatmap-container">
      <canvas ref="heatmapCanvas" class="chart-canvas w-full h-48"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { postAddAsset, fetchRiskAssessment } from '@/api'

const assets = reactive([])
const loading = ref(false)
const result = ref(null)

function addAsset() {
  assets.push({ id: Date.now().toString(), name: '', impact: 1, likelihood: 1 })
}

function removeAsset(idx) {
  assets.splice(idx, 1)
}

async function submitAssets() {
  loading.value = true
  try {
    // send each asset to backend
    for (const a of assets) {
      await postAddAsset({ name: a.name, impact: a.impact, likelihood: a.likelihood })
    }
    const res = await fetchRiskAssessment()
    result.value = res
    renderHeatmap(res)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

// render heatmap using Chart.js or custom drawing
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)
const heatmapCanvas = ref(null)

function renderHeatmap(res) {
  if (!heatmapCanvas.value) return
  const matrix = Array.from({ length: 5 }, () => Array(5).fill(0))
  res.risk_data.forEach(r => {
    matrix[r.impact - 1][r.likelihood - 1]++
  })
  // Clear previous chart if exists
  heatmapCanvas.value.getContext('2d').clearRect(0, 0, heatmapCanvas.value.width, heatmapCanvas.value.height)
  // For simplicity: draw colored rectangles manually
  const ctx = heatmapCanvas.value.getContext('2d')
  const cellSize = heatmapCanvas.value.width / 5
  for (let i = 0; i < 5; i++) {
    for (let j = 0; j < 5; j++) {
      const count = matrix[4 - i][j]  // flip y
      // choose color based on count (or level)
      const alpha = Math.min(0.8, 0.2 + count * 0.1)
      ctx.fillStyle = `rgba(26,175,156,${alpha})`
      ctx.fillRect(j * cellSize, i * cellSize, cellSize, cellSize)
      if (count > 0) {
        ctx.fillStyle = '#000'
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillText(count, j * cellSize + cellSize/2, i * cellSize + cellSize/2)
      }
    }
  }
}

</script>

<style scoped>
.list-enter-active, .list-leave-active {
  transition: all 0.3s ease;
}
.list-enter-from {
  opacity: 0;
  transform: translateX(20px);
}
.list-enter-to {
  opacity: 1;
  transform: translateX(0);
}
.list-leave-from {
  opacity: 1;
  transform: translateX(0);
}
.list-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
