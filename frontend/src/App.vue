<template>
  <div class="min-h-screen flex flex-col bg-bg-dark text-text-light">
    <NavigationBar />
    <main class="flex-grow p-8 max-w-7xl mx-auto w-full">
      <router-view></router-view>
    </main>
    <footer class="p-4 bg-card-dark text-center text-sm border-t border-gray-700">
      &copy; {{ currentYear }} GRC Nexus. All rights reserved.
    </footer>
  </div>
</template>

<script setup>
import NavigationBar from './components/NavigationBar.vue'
import { ref } from 'vue'

const currentYear = ref(new Date().getFullYear())
</script>

<style>
/* Base styles imported from style.css */
</style>