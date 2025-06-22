<template>
  <div class="recommendations-list p-6 space-y-8">
    <h1 class="text-4xl font-extrabold text-center text-primary-blue mb-8">Actionable Recommendations</h1>

    <div v-if="recommendations.length > 0" class="card">
      <h2 class="text-2xl font-semibold text-primary-blue mb-4">Identified GRC Recommendations</h2>
      <p class="text-muted-gray mb-6">Review the suggestions below to improve your compliance posture and mitigate risks.</p>

      <ul class="space-y-6">
        <li v-for="(rec, index) in recommendations" :key="index" class="bg-gray-800 p-5 rounded-lg border border-gray-700 shadow-md">
          <div class="flex items-center mb-3">
            <span :class="['px-3 py-1 rounded-full text-xs font-semibold', getRecommendationTypeClass(rec.type)]">
              {{ rec.type }}
            </span>
            <span class="ml-4 text-primary-blue font-bold text-lg">{{ rec.item }}</span>
          </div>
          <p class="text-gray-300 text-sm mb-2"><strong>Area:</strong> {{ rec.area }}</p>
          <p class="text-gray-200 leading-relaxed">{{ rec.suggestion }}</p>
        </li>
      </ul>
    </div>
    <div v-else class="card text-center text-lg text-muted-gray py-10">
      <p class="mb-4">No recommendations generated at this time.</p>
      <p>This could mean all controls are compliant and no high-risk assets have been identified. </p>
      <p>Please perform a <router-link to="/compliance" class="text-primary-blue hover:underline">Compliance Assessment</router-link> and define <router-link to="/risk" class="text-primary-blue hover:underline">Assets for Risk Assessment</router-link>.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const recommendations = ref([]);

const fetchRecommendations = async () => {
  try {
    const response = await axios.get(`${API_URL}/all-recommendations`);
    recommendations.value = response.data;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
  }
};

const getRecommendationTypeClass = (type) => {
  switch (type) {
    case 'Control Remediation': return 'bg-noncompliant-red text-white';
    case 'Control Improvement': return 'bg-partial-orange text-gray-900';
    case 'Risk Treatment': return 'bg-primary-blue text-white';
    default: return 'bg-muted-gray text-white';
  }
};

onMounted(fetchRecommendations);
</script>

<style scoped>
/* Specific styles */
</style>