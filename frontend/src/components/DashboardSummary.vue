<template>
  <div class="dashboard p-6 space-y-12">
    <!-- Section: Title & Breadcrumb -->
    <transition name="fade-slide" mode="out-in">
      <div key="dashboard-header" class="flex justify-between items-center">
        <div>
          <h2 class="text-3xl font-bold text-text-light">Dashboard</h2>
          <p class="text-muted-gray">Overview of compliance & risk</p>
        </div>
        <!-- Optional: theme toggle or extra controls -->
      </div>
    </transition>

    <!-- Section: KPI Cards -->
    <transition-group name="fade-slide" tag="div" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <div
        v-for="item in cards"
        :key="item.title"
        class="bg-card-dark p-6 rounded-lg shadow-lg transform transition-transform duration-300 hover:scale-105"
      >
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-muted-gray">{{ item.title }}</p>
            <p class="text-2xl font-bold mt-1">{{ item.value }}</p>
          </div>
          <!-- Simple icon; replace with SVG icons if preferred -->
          <div class="text-4xl">{{ item.icon }}</div>
        </div>
      </div>
    </transition-group>

    <!-- Section: Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Compliance Overview Chart -->
      <div class="bg-card-dark p-6 rounded-lg shadow-lg transform transition-transform duration-300 hover:scale-105">
        <div class="flex items-center mb-4">
          <h3 class="text-xl font-semibold text-text-light">Compliance Overview</h3>
          <span
            class="ml-2 text-muted-gray cursor-help"
            title="Shows counts of compliant vs non-compliant controls in real-time."
            aria-label="Shows counts of compliant vs non-compliant controls in real-time."
          >ℹ️</span>
        </div>
        <div class="relative h-64">
          <canvas
            ref="complianceChartCanvas"
            class="w-full h-full chart-canvas"
            role="img"
            aria-label="Compliance doughnut chart"
          ></canvas>
        </div>
      </div>

      <!-- Risk Matrix Heatmap -->
      <div class="bg-card-dark p-6 rounded-lg shadow-lg transform transition-transform duration-300 hover:scale-105">
        <div class="flex items-center mb-4">
          <h3 class="text-xl font-semibold text-text-light">Risk Matrix Heatmap</h3>
          <span
            class="ml-2 text-muted-gray cursor-help"
            title="Impact vs Likelihood matrix; hover cells for asset details."
            aria-label="Impact vs Likelihood matrix; hover cells for asset details."
          >ℹ️</span>
        </div>
        <div v-if="riskHeatmap" class="heatmap-container flex justify-center items-center">
          <!-- Base64 image from backend -->
          <img
            :src="`data:image/png;base64,${riskHeatmap}`"
            alt="Risk Matrix Heatmap"
            class="max-w-full h-auto rounded-lg shadow-md"
          />
        </div>
        <div v-else class="text-center py-12">
          <!-- Empty state -->
          <!-- If you have an illustration in assets, replace the <p> with <img src="..." alt="No data" /> -->
          <p class="text-lg text-muted-gray mb-2">No risk data to display.</p>
          <router-link to="/risk" class="text-primary-blue hover:underline">
            Add assets in 'Risk' section
          </router-link>
        </div>
      </div>
    </div>

    <!-- Section: Detailed Compliance Table -->
    <div class="bg-card-dark p-6 rounded-lg shadow-lg transform transition-transform duration-300 hover:scale-105">
      <div class="flex items-center mb-4">
        <h3 class="text-xl font-semibold text-text-light">Detailed Compliance Status</h3>
        <span
          class="ml-2 text-muted-gray cursor-help"
          title="List of all controls, their status, and details."
          aria-label="List of all controls, their status, and details."
        >ℹ️</span>
      </div>
      <div v-if="!hasComplianceData" class="text-center py-12">
        <p class="text-lg text-muted-gray mb-2">No compliance data available.</p>
        <router-link to="/compliance" class="text-primary-blue hover:underline">
          Assess compliance now
        </router-link>
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full table-auto text-left border-separate border-spacing-0">
          <thead class="bg-card-dark sticky top-0">
            <tr>
              <th class="py-3 px-4 text-text-light">Control ID</th>
              <th class="py-3 px-4 text-text-light">Name</th>
              <th class="py-3 px-4 text-text-light">Status</th>
              <th class="py-3 px-4 text-text-light">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="control in complianceResults"
              :key="control.id"
              class="odd:bg-card-hover even:bg-card-dark hover:bg-card-hover transition-colors"
            >
              <td class="py-3 px-4 text-text-light">{{ control.id }}</td>
              <td class="py-3 px-4 text-text-light">{{ control.name }}</td>
              <td class="py-3 px-4">
                <span
                  class="px-2 py-1 rounded-full text-sm font-medium"
                  :class="getStatusBadgeClass(control.status)"
                >
                  {{ control.status }}
                </span>
              </td>
              <td class="py-3 px-4">
                <details class="group">
                  <summary
                    class="cursor-pointer text-primary-blue hover:underline list-none"
                  >
                    View
                  </summary>
                  <div class="mt-2 text-text-light">
                    <p><strong>Description:</strong> {{ control.description }}</p>
                    <p v-if="control.remediation_suggestion">
                      <strong>Remediation:</strong> {{ control.remediation_suggestion }}
                    </p>
                  </div>
                </details>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Section: Detailed Risk Table -->
    <div class="bg-card-dark p-6 rounded-lg shadow-lg transform transition-transform duration-300 hover:scale-105">
      <div class="flex items-center mb-4">
        <h3 class="text-xl font-semibold text-text-light">Detailed Risk Assessment</h3>
        <span
          class="ml-2 text-muted-gray cursor-help"
          title="List of all assets, their risk scores, and details."
          aria-label="List of all assets, their risk scores, and details."
        >ℹ️</span>
      </div>
      <div v-if="!hasRiskData" class="text-center py-12">
        <p class="text-lg text-muted-gray mb-2">No asset risk data available.</p>
        <router-link to="/risk" class="text-primary-blue hover:underline">
          Add assets in 'Risk' section
        </router-link>
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full table-auto text-left border-separate border-spacing-0">
          <thead class="bg-card-dark sticky top-0">
            <tr>
              <th class="py-3 px-4 text-text-light">Asset Name</th>
              <th class="py-3 px-4 text-text-light">Impact</th>
              <th class="py-3 px-4 text-text-light">Likelihood</th>
              <th class="py-3 px-4 text-text-light">Risk Score</th>
              <th class="py-3 px-4 text-text-light">Level</th>
              <th class="py-3 px-4 text-text-light">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="asset in riskData"
              :key="asset.name"
              class="odd:bg-card-hover even:bg-card-dark hover:bg-card-hover transition-colors"
            >
              <td class="py-3 px-4 text-text-light">{{ asset.name }}</td>
              <td class="py-3 px-4 text-text-light">{{ asset.impact }}</td>
              <td class="py-3 px-4 text-text-light">{{ asset.likelihood }}</td>
              <td class="py-3 px-4 text-text-light">{{ asset.score }}</td>
              <td class="py-3 px-4">
                <span
                  class="px-2 py-1 rounded-full text-sm font-medium"
                  :class="getRiskLevelBadgeClass(asset.level)"
                >
                  {{ asset.level }}
                </span>
              </td>
              <td class="py-3 px-4">
                <details class="group">
                  <summary
                    class="cursor-pointer text-primary-blue hover:underline list-none"
                  >
                    View
                  </summary>
                  <div class="mt-2 text-text-light">
                    <p><strong>Treatment:</strong> {{ getTreatmentText(asset.level) }}</p>
                    <p v-if="asset.level !== 'Low'">
                      <strong>Recommendation:</strong> {{ getRecommendationText(asset.level) }}
                    </p>
                  </div>
                </details>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import axios from 'axios';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

const API_URL = import.meta.env.VITE_API_URL || '';

// Reactive state
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

// Derived flags
const hasComplianceData = ref(false);
const hasRiskData = ref(false);

// Fetch data from backend
const fetchDashboardData = async () => {
  try {
    // Compliance results
    const complianceRes = await axios.get(`${API_URL}/compliance-results`);
    const compData = complianceRes.data;
    complianceSummary.value = {
      total_controls: compData.total_controls,
      compliant_count: compData.compliant_count,
      non_compliant_count: compData.non_compliant_count,
      partially_compliant_count: compData.partially_compliant_count,
      compliance_percentage: compData.compliance_percentage,
    };
    complianceResults.value = compData.results || [];
    hasComplianceData.value = complianceResults.value.length > 0;

    // Risk assessment
    const riskRes = await axios.get(`${API_URL}/risk-assessment`);
    const riskPayload = riskRes.data;
    riskData.value = (riskPayload.risk_data || []).map(r => ({
      name: r.name,
      impact: r.impact,
      likelihood: r.likelihood,
      score: r.score,
      level: r.level,
    }));
    riskHeatmap.value = riskPayload.risk_heatmap || null;
    hasRiskData.value = riskData.value.length > 0;

    // Wait DOM update, then render chart
    await nextTick();
    renderComplianceChart();
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
    // Optionally: show toast or error UI
  }
};

// Render the compliance doughnut chart
const renderComplianceChart = () => {
  if (!complianceChartCanvas.value) return;
  const ctx = complianceChartCanvas.value.getContext('2d');
  if (complianceChart) {
    complianceChart.destroy();
    complianceChart = null;
  }
  // Calculate “Not Assessed”
  const total = complianceSummary.value.total_controls || 0;
  const assessedSum =
    (complianceSummary.value.compliant_count || 0) +
    (complianceSummary.value.non_compliant_count || 0) +
    (complianceSummary.value.partially_compliant_count || 0);
  const notAssessed = Math.max(0, total - assessedSum);

  complianceChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Compliant', 'Non-Compliant', 'Partially Compliant', 'Not Assessed'],
      datasets: [
        {
          data: [
            complianceSummary.value.compliant_count,
            complianceSummary.value.non_compliant_count,
            complianceSummary.value.partially_compliant_count,
            notAssessed,
          ],
          backgroundColor: [
            '#28a745', // green
            '#dc3545', // red
            '#ffc107', // yellow
            '#6c757d', // gray
          ],
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        animateRotate: true,
        animateScale: true,
        duration: 800,
        easing: 'easeOutBack',
      },
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#cbd5e0',
          },
        },
        tooltip: {
          callbacks: {
            label(context) {
              let label = context.label || '';
              if (label) label += ': ';
              if (context.parsed !== null) {
                label += context.parsed;
              }
              return label;
            },
          },
        },
      },
    },
  });
};

// KPI cards data
const cards = ref([]);
watch(
  complianceSummary,
  () => {
    cards.value = [
      {
        title: 'Total Controls',
        value: complianceSummary.value.total_controls,
        icon: '📋',
      },
      {
        title: 'Compliant',
        value: complianceSummary.value.compliant_count,
        icon: '✅',
      },
      {
        title: 'Non-Compliant',
        value: complianceSummary.value.non_compliant_count,
        icon: '⚠️',
      },
      {
        title: 'Compliance %',
        value: `${complianceSummary.value.compliance_percentage}%`,
        icon: '📊',
      },
    ];
  },
  { immediate: true }
);

// Badge classes for compliance status
const getStatusBadgeClass = (status) => {
  switch (status) {
    case 'Implemented':
      return 'bg-compliant-green text-black';
    case 'Not Implemented':
      return 'bg-noncompliant-red text-white';
    case 'Partially Implemented':
      return 'bg-partial-orange text-black';
    default:
      return 'bg-muted-gray text-white';
  }
};

// Badge classes for risk level
const getRiskLevelBadgeClass = (level) => {
  switch (level) {
    case 'Low':
      return 'bg-compliant-green text-black';
    case 'Medium':
      return 'bg-partial-orange text-black';
    case 'High':
      return 'bg-noncompliant-red text-white';
    default:
      return 'bg-muted-gray text-white';
  }
};

// Risk treatment / recommendation text
const getTreatmentText = (level) => {
  if (level === 'High') return 'Mitigate (Urgent)';
  if (level === 'Medium') return 'Mitigate / Monitor';
  return 'Accept / Monitor';
};
const getRecommendationText = (level) => {
  if (level === 'High') return 'Risk Level: High. Recommended Treatment: Mitigate (Urgent).';
  if (level === 'Medium') return 'Risk Level: Medium. Recommended Treatment: Mitigate / Monitor.';
  return '';
};

// On mounted, fetch data
onMounted(() => {
  fetchDashboardData();
});

// If complianceSummary or riskData changes, re-render compliance chart
watch([() => complianceSummary.value, () => riskData.value], () => {
  nextTick().then(() => {
    renderComplianceChart();
  });
});
</script>

<style scoped>
/* Fade-slide transition */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}
.fade-slide-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Heatmap container tilt effect */
.heatmap-container {
  perspective: 600px;
}
.heatmap-container img:hover {
  transform: rotateX(8deg) scale(1.02);
  transition: transform 0.3s ease;
}

/* Chart canvas tilt effect */
.chart-canvas:hover {
  transform: rotateX(5deg) scale(1.02);
  transition: transform 0.3s ease;
}

/* details summary style */
details > summary {
  list-style: none;
}
details > summary::-webkit-details-marker {
  display: none;
}
</style>
