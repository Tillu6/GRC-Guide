<template>
  <svg v-if="!dark" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
    <!-- sun icon -->
    <path d="M10 5a1 1 0 011 1v1a1 1 0 11-2 0V6a1 1 0 011-1zM10 12a2 2 0 100-4 2 2 0 000 4zm4-2a1 1 0 011-1h1a1 1 0 110 2h-1a1 1 0 01-1-1zm-8 0a1 1 0 01-1-1H5a1 1 0 110 2h1a1 1 0 011-1zm6.364-3.364a1 1 0 010 1.414L14.95 8.95a1 1 0 11-1.414-1.414l.414-.414a1 1 0 011.414 0zM7.05 11.05a1 1 0 011.414 1.414l-.414.414a1 1 0 11-1.414-1.414l.414-.414zm6.364 2.828a1 1 0 011.414 0l.414.414a1 1 0 11-1.414 1.414l-.414-.414a1 1 0 010-1.414zM7.464 6.636a1 1 0 010 1.414l-.414.414a1 1 0 11-1.414-1.414l.414-.414a1 1 0 011.414 0zM10 16a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1z"/>
  </svg>
  <svg v-else xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
    <!-- moon icon -->
    <path d="M17.293 13.293a8 8 0 11-10.586-10.586 7 7 0 1010.586 10.586z"/>
  </svg>
</template>
<script setup>
const props = defineProps({ dark: Boolean })
</script>
<style scoped></style>
