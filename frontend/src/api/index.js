import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export async function fetchComplianceResults() {
  const res = await axios.get(`${API_URL}/compliance-results`)
  return res.data
}
export async function fetchRiskAssessment() {
  const res = await axios.get(`${API_URL}/risk-assessment`)
  return res.data
}
// Add more endpoints as needed: get controls, post assess, post add-asset, etc.
export async function fetchControls() {
  const res = await axios.get(`${API_URL}/controls`)
  return res.data
}
export async function postAssessCompliance(statuses) {
  const res = await axios.post(`${API_URL}/assess-compliance`, statuses)
  return res.data
}
export async function postAddAsset(asset) {
  const res = await axios.post(`${API_URL}/add-asset`, asset)
  return res.data
}
