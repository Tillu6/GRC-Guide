<!-- src/App.vue -->
<template>
  <div class="min-h-screen flex flex-col bg-bg-dark text-text-light">
    <NavigationBar />
    <main class="flex-grow">
      <router-view />
    </main>
    <footer class="p-2 bg-card-dark text-center text-xs border-t border-gray-700">
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
/* Global styles, Tailwind imports, etc. */
</style>
