<template>
  <div class="dashboard p-6 space-y-8">
    <h1 class="text-4xl font-extrabold text-center text-primary-blue mb-8">GRC Nexus Dashboard</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="card text-center">
        <h2 class="text-xl font-semibold text-primary-blue mb-2">Total Controls</h2>
        <p class="text-4xl font-bold">{{ complianceSummary.total_controls }}</p>
      </div>
      <div class="card text-center">
        <h2 class="text-xl font-semibold text-compliant-green mb-2">Compliant</h2>
        <p class="text-4xl font-bold">{{ complianceSummary.compliant_count }}</p>
      </div>
      <div class="card text-center">
        <h2 class="text-xl font-semibold text-noncompliant-red mb-2">Non-Compliant</h2>
        <p class="text-4xl font-bold">{{ complianceSummary.non_compliant_count }}</p>
      </div>
      <div class="card text-center">
        <h2 class="text-xl font-semibold text-primary-blue mb-2">Compliance %</h2>
        <p class="text-4xl font-bold">{{ complianceSummary.compliance_percentage }}%</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="card">
        <h2 class="text-2xl font-semibold text-primary-blue mb-4">Compliance Overview</h2>
        <canvas ref="complianceChartCanvas"></canvas>
      </div>

      <div class="card">
        <h2 class="text-2xl font-semibold text-primary-blue mb-4">Risk Matrix Heatmap</h2>
        <div v-if="riskHeatmap" class="flex justify-center items-center">
            <img :src="`data:image/png;base64,${riskHeatmap}`" alt="Risk Matrix Heatmap" class="max-w-full h-auto rounded-lg shadow-md">
        </div>
        <p v-else class="text-muted-gray text-center">No risk data to display heatmap. Add assets in 'Risk' section.</p>
      </div>
    </div>

    <div class="card">
      <h2 class="text-2xl font-semibold text-primary-blue mb-4">Detailed Compliance Status</h2>
      <div class="overflow-x-auto">
        <table class="min-w-full bg-card-dark rounded-lg shadow-lg-dark">
          <thead>
            <tr class="table-header">
              <th class="py-3 px-6 text-left">Control ID</th>
              <th class="py-3 px-6 text-left">Name</th>
              <th class="py-3 px-6 text-left">Status</th>
              <th class="py-3 px-6 text-left">Description</th>
            </tr>
          </thead>
          <tbody class="text-gray-200 text-sm font-light">
            <tr v-for="control in complianceResults" :key="control.id" class="table-row">
              <td class="py-4 px-6">{{ control.id }}</td>
              <td class="py-4 px-6">{{ control.name }}</td>
              <td :class="['py-4 px-6', getStatusClass(control.status)]">{{ control.status }}</td>
              <td class="py-4 px-6">{{ control.description }}</td>
            </tr>
            <tr v-if="complianceResults.length === 0">
                <td colspan="4" class="py-4 px-6 text-center text-muted-gray">No compliance data available. Please assess compliance.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

     <div class="card">
      <h2 class="text-2xl font-semibold text-primary-blue mb-4">Detailed Risk Assessment</h2>
      <div class="overflow-x-auto">
        <table class="min-w-full bg-card-dark rounded-lg shadow-lg-dark">
          <thead>
            <tr class="table-header">
              <th class="py-3 px-6 text-left">Asset Name</th>
              <th class="py-3 px-6 text-left">Impact (1-5)</th>
              <th class="py-3 px-6 text-left">Likelihood (1-5)</th>
              <th class="py-3 px-6 text-left">Risk Score</th>
              <th class="py-3 px-6 text-left">Risk Level</th>
            </tr>
          </thead>
          <tbody class="text-gray-200 text-sm font-light">
            <tr v-for="asset in riskData" :key="asset.name" class="table-row">
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
            <tr v-if="riskData.length === 0">
                <td colspan="5" class="py-4 px-6 text-center text-muted-gray">No asset risk data available. Add assets in 'Risk' section.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

const API_URL = import.meta.env.VITE_API_URL;

const complianceSummary = ref({
  total_controls: 0,
  compliant_count: 0,
  non_compliant_count: 0,
  partially_compliant_count: 0,
  compliance_percentage: 0,
});
const complianceResults = ref([]);
const riskData = ref([]);
const riskHeatmap = ref(null);

const complianceChartCanvas = ref(null);
let complianceChart = null;

const fetchDashboardData = async () => {
  try {
    const complianceRes = await axios.get(`${API_URL}/compliance-results`);
    complianceSummary.value = {
      total_controls: complianceRes.data.total_controls,
      compliant_count: complianceRes.data.compliant_count,
      non_compliant_count: complianceRes.data.non_compliant_count,
      partially_compliant_count: complianceRes.data.partially_compliant_count,
      compliance_percentage: complianceRes.data.compliance_percentage,
    };
    complianceResults.value = complianceRes.data.results;

    const riskRes = await axios.get(`${API_URL}/risk-assessment`);
    riskData.value = riskRes.data.risk_data;
    riskHeatmap.value = riskRes.data.risk_heatmap;

    renderComplianceChart();

  } catch (error) {
    console.error('Error fetching dashboard data:', error);
  }
};

const renderComplianceChart = () => {
  if (complianceChart) {
    complianceChart.destroy(); // Destroy existing chart if it exists
  }

  const ctx = complianceChartCanvas.value.getContext('2d');
  complianceChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Compliant', 'Non-Compliant', 'Partially Compliant', 'Not Assessed'],
      datasets: [{
        data: [
          complianceSummary.value.compliant_count,
          complianceSummary.value.non_compliant_count,
          complianceSummary.value.partially_compliant_count,
          complianceSummary.value.total_controls - (complianceSummary.value.compliant_count + complianceSummary.value.non_compliant_count + complianceSummary.value.partially_compliant_count)
        ],
        backgroundColor: [
          '#28a745', // compliant-green
          '#dc3545', // noncompliant-red
          '#ffc107', // partial-orange
          '#6c757d', // muted-gray
        ],
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            color: '#cbd5e0' // Light text for dark background
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              let label = context.label || '';
              if (label) {
                label += ': ';
              }
              if (context.parsed !== null) {
                label += context.parsed;
              }
              return label;
            }
          }
        }
      }
    }
  });
};

const getStatusClass = (status) => {
  switch (status) {
    case 'Implemented': return 'status-implemented';
    case 'Not Implemented': return 'status-not-implemented';
    case 'Partially Implemented': return 'status-partially-implemented';
    default: return 'status-not-assessed';
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

onMounted(() => {
  fetchDashboardData();
});

watch([complianceSummary, riskData], () => {
  renderComplianceChart();
}, { deep: true });

</script>

<style scoped>
/* Scoped styles */
</style>