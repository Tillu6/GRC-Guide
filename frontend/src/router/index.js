import { createRouter, createWebHistory } from 'vue-router'
import DashboardSummary from '../components/DashboardSummary.vue'
import ComplianceAssessment from '../components/ComplianceAssessment.vue'
import RiskAssessment from '../components/RiskAssessment.vue'
import RecommendationsList from '../components/RecommendationsList.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: DashboardSummary },
  { path: '/compliance', name: 'Compliance Assessment', component: ComplianceAssessment },
  { path: '/risk', name: 'Risk Assessment', component: RiskAssessment },
  { path: '/recommendations', name: 'Recommendations', component: RecommendationsList },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router