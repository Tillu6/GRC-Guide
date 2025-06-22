<template>
  <div class="risk-assessment p-6 space-y-8">
    <h1 class="text-4xl font-extrabold text-center text-primary-blue mb-8">Risk Assessment</h1>

    <div class="card">
      <h2 class="text-2xl font-semibold text-primary-blue mb-4">Define Your Assets</h2>
      <p class="text-muted-gray mb-6">Add assets to your environment and assess their potential impact and likelihood of risk events.</p>

      <form @submit.prevent="addAsset" class="space-y-4 mb-8">
        <div>
          <label for="assetName" class="block text-gray-300 text-sm font-bold mb-2">Asset Name:</label>
          <input type="text" id="assetName" v-model="newAsset.name" required class="input-field w-full">
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="assetImpact" class="block text-gray-300 text-sm font-bold mb-2">Impact (1-5):</label>
            <input type="number" id="assetImpact" v-model="newAsset.impact" min="1" max="5" required class="input-field w-full">
          </div>
          <div>
            <label for="assetLikelihood" class="block text-gray-300 text-sm font-bold mb-2">Likelihood (1-5):</label>
            <input type="number" id="assetLikelihood" v-model="newAsset.likelihood" min="1" max="5" required class="input-field w-full">
          </div>
        </div>
        <button type="submit" class="btn-primary w-full py-3">Add Asset</button>
      </form>

      <div v-if="submissionMessage" :class="['mt-4 p-3 rounded-md text-center', submissionStatus === 'success' ? 'bg-green-600 text-white' : 'bg-red-600 text-white']">
        {{ submissionMessage }}
      </div>
    </div>

    <div class="card" v-if="assets.length > 0">
      <h2 class="text-2xl font-semibold text-primary-blue mb-4">Current Assets & Risk Summary</h2>
      <div class="overflow-x-auto mb-6">
        <table class="min-w-full bg-gray-800 rounded-lg shadow-lg-dark">
          <thead>
            <tr class="table-header">
              <th class="py-3 px-6 text-left">Asset Name</th>
              <th class="py-3 px-6 text-left">Impact</th>
              <th class="py-3 px-6 text-left">Likelihood</th>
              <th class="py-3 px-6 text-left">Risk Score</th>
              <th class="py-3 px-6 text-left">Risk Level</th>
            </tr>
          </thead>
          <tbody class="text-gray-200 text-sm font-light">
            <tr v-for="asset in assets" :key="asset.name" class="table-row">
              <td class="py-4 px-6">{{ asset.name }}</td>
              <td class="py-4 px-6">{{ asset.impact }}</td>
              <td class="py-4 px-6">{{ asset.likelihood }}</td>
              <td class="py-4 px-6">{{ asset.score }}</td>
              <td class="py-4 px-6">
                <span :class="['px-3 py-1 rounded-full text-xs font-semibold', getRiskLevelClass(asset.level)]">
                  {{ asset.level }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

       <div class="mt-6 flex justify-center">
            <img v-if="riskHeatmap" :src="`data:image/png;base64,${riskHeatmap}`" alt="Risk Matrix Heatmap" class="max-w-full h-auto rounded-lg shadow-md">
            <p v-else class="text-muted-gray text-center">No risk heatmap to display. Add assets to see the visualization.</p>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const newAsset = ref({
  name: '',
  impact: 1,
  likelihood: 1
});
const assets = ref([]);
const submissionMessage = ref('');
const submissionStatus = ref('');
const riskHeatmap = ref(null);


const fetchAssetsAndRisk = async () => {
  try {
    const response = await axios.get(`${API_URL}/risk-assessment`);
    assets.value = response.data.risk_data;
    riskHeatmap.value = response.data.risk_heatmap;
  } catch (error) {
    console.error('Error fetching assets and risk data:', error);
  }
};

const addAsset = async () => {
  try {
    await axios.post(`${API_URL}/add-asset`, newAsset.value);
    submissionMessage.value = `Asset '${newAsset.value.name}' added successfully!`;
    submissionStatus.value = 'success';
    newAsset.value = { name: '', impact: 1, likelihood: 1 }; // Reset form
    await fetchAssetsAndRisk(); // Refresh asset list and heatmap
  } catch (error) {
    console.error('Error adding asset:', error);
    submissionMessage.value = 'Failed to add asset. Please try again.';
    submissionStatus.value = 'error';
  } finally {
    setTimeout(() => {
      submissionMessage.value = '';
    }, 5000); // Clear message after 5 seconds
  }
};

const getRiskLevelClass = (level) => {
  switch (level) {
    case 'Low': return 'bg-compliant-green text-white';
    case 'Medium': return 'bg-partial-orange text-gray-900';
    case 'High': return 'bg-noncompliant-red text-white';
    default: return 'bg-muted-gray text-white';
  }
};

onMounted(fetchAssetsAndRisk);
</script>

<style scoped>
/* Specific styles */
</style>