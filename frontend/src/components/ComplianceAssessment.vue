<template>
  <div class="compliance-assessment p-6 space-y-8">
    <h1 class="text-4xl font-extrabold text-center text-primary-blue mb-8">Compliance Assessment</h1>

    <div class="card">
      <h2 class="text-2xl font-semibold text-primary-blue mb-4">Assess Your Controls</h2>
      <p class="text-muted-gray mb-6">Review each control below and indicate its current implementation status.</p>

      <form @submit.prevent="submitCompliance" class="space-y-6">
        <div v-for="control in controls" :key="control.id" class="border border-gray-700 p-4 rounded-lg bg-gray-800">
          <h3 class="text-xl font-semibold text-gray-100 mb-2">{{ control.name }} ({{ control.id }})</h3>
          <p class="text-gray-300 mb-3">{{ control.description }}</p>
          <p class="text-primary-blue text-sm mb-3"><strong>Check Criteria:</strong> {{ control.check_criteria }}</p>
          
          <div class="flex items-center space-x-4">
            <label class="inline-flex items-center">
              <input type="radio" :name="`status-${control.id}`" :value="'Implemented'" v-model="formStatuses[control.id]" class="form-radio text-compliant-green h-4 w-4">
              <span class="ml-2 text-compliant-green">Implemented</span>
            </label>
            <label class="inline-flex items-center">
              <input type="radio" :name="`status-${control.id}`" :value="'Not Implemented'" v-model="formStatuses[control.id]" class="form-radio text-noncompliant-red h-4 w-4">
              <span class="ml-2 text-noncompliant-red">Not Implemented</span>
            </label>
            <label class="inline-flex items-center">
              <input type="radio" :name="`status-${control.id}`" :value="'Partially Implemented'" v-model="formStatuses[control.id]" class="form-radio text-partial-orange h-4 w-4">
              <span class="ml-2 text-partial-orange">Partially Implemented</span>
            </label>
          </div>
        </div>

        <button type="submit" class="btn-primary w-full py-3">Submit Assessment</button>
      </form>

      <div v-if="submissionMessage" :class="['mt-6 p-4 rounded-md text-center', submissionStatus === 'success' ? 'bg-green-600 text-white' : 'bg-red-600 text-white']">
        {{ submissionMessage }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const controls = ref([]);
const formStatuses = ref({});
const submissionMessage = ref('');
const submissionStatus = ref('');

const fetchControls = async () => {
  try {
    const response = await axios.get(`${API_URL}/controls`);
    controls.value = response.data;
    // Initialize formStatuses with current or default 'Not Assessed' status
    controls.value.forEach(control => {
      formStatuses.value[control.id] = 'Not Implemented'; // Default for new assessments
    });
  } catch (error) {
    console.error('Error fetching controls:', error);
  }
};

const submitCompliance = async () => {
  try {
    const formattedStatuses = Object.keys(formStatuses.value).map(controlId => ({
      id: controlId,
      status: formStatuses.value[controlId]
    }));
    await axios.post(`${API_URL}/assess-compliance`, formattedStatuses);
    submissionMessage.value = 'Compliance assessment submitted successfully!';
    submissionStatus.value = 'success';
    // Optionally refetch data for dashboard or redirect
  } catch (error) {
    console.error('Error submitting compliance:', error);
    submissionMessage.value = 'Failed to submit assessment. Please try again.';
    submissionStatus.value = 'error';
  } finally {
    setTimeout(() => {
      submissionMessage.value = '';
    }, 5000); // Clear message after 5 seconds
  }
};

onMounted(fetchControls);
</script>

<style scoped>
/* Specific styles for this component */
</style>