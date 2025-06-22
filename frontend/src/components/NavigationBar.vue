<template>
  <nav class="bg-card-dark p-4 shadow-lg-dark border-b border-gray-700">
    <div class="container mx-auto flex justify-between items-center">
      <router-link to="/" class="text-2xl font-bold text-primary-blue flex items-center">
        <img src="/logo.svg" alt="GRC Nexus Logo" class="h-8 w-8 mr-2">
        GRC Nexus
      </router-link>
      <div class="space-x-4">
        <router-link to="/" class="text-lg hover:text-primary-blue transition-colors duration-200">Dashboard</router-link>
        <router-link to="/compliance" class="text-lg hover:text-primary-blue transition-colors duration-200">Compliance</router-link>
        <router-link to="/risk" class="text-lg hover:text-primary-blue transition-colors duration-200">Risk</router-link>
        <router-link to="/recommendations" class="text-lg hover:text-primary-blue transition-colors duration-200">Recommendations</router-link>
        <button @click="exportReport" class="btn-primary">Export Report</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const exportReport = async () => {
  try {
    // Open the report in a new tab
    window.open(`${API_URL.replace('/api', '')}/report`, '_blank');
  } catch (error) {
    console.error('Error generating report:', error);
    alert('Failed to generate report. Please try again.');
  }
};
</script>

<style scoped>
/* Scoped styles specific to this component if needed */
</style>