<!-- src/components/NavigationBar.vue -->
<template>
  <nav
    class="bg-card-dark p-1 shadow-md border-b border-gray-700"
    role="navigation"
    aria-label="Main navigation"
  >
    <div class="max-w-7xl mx-auto flex justify-between items-center">
      <!-- Logo only, no duplicate elsewhere -->
      <router-link
        to="/"
        class="flex items-center"
        aria-label="Go to Dashboard"
      >
        <!-- Very tiny logo: -->
        <AnimatedLogo size="w-2 h-2" class="flex-shrink-0" />
        <!-- Optional label, hidden on small screens -->
        <span class="ml-1 text-xs font-semibold text-primary-blue hidden md:inline">GRC Nexus</span>
      </router-link>

      <!-- Desktop links -->
      <div class="hidden md:flex space-x-3 items-center">
        <NavLink to="/" label="Dashboard" />
        <NavLink to="/compliance" label="Compliance" />
        <NavLink to="/risk" label="Risk" />
        <NavLink to="/recommendations" label="Recommendations" />

        <!-- Export report: icon-only -->
        <button
          @click="exportReport"
          class="btn-primary p-1 focus:outline-none focus:ring-2 focus:ring-primary-blue"
          aria-label="Export report"
        >
          <DownloadIcon class="w-4 h-4 animate-bounce-slow" aria-hidden="true" />
        </button>

        <!-- Theme toggle -->
        <button
          @click="toggleTheme"
          class="p-1 rounded focus:outline-none focus:ring-2 focus:ring-primary-blue hover:bg-card-dark/50"
          :aria-label="isDark.value ? 'Switch to light mode' : 'Switch to dark mode'"
        >
          <ThemeIcon :dark="isDark.value" class="w-4 h-4" aria-hidden="true" />
        </button>
      </div>

      <!-- Mobile menu button -->
      <button
        class="md:hidden p-1 focus:outline-none focus:ring-2 focus:ring-primary-blue"
        @click="toggleMobile"
        :aria-label="mobileOpen ? 'Close menu' : 'Open menu'"
        :aria-expanded="mobileOpen.toString()"
      >
        <svg
          v-if="!mobileOpen"
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 text-text-light"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16" />
        </svg>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 text-text-light"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Mobile menu -->
    <transition name="slide-fade">
      <div
        v-if="mobileOpen"
        class="md:hidden bg-card-dark border-t border-gray-700"
        role="menu"
      >
        <NavLink to="/" label="Dashboard" class="block py-1 px-2 text-sm" />
        <NavLink to="/compliance" label="Compliance" class="block py-1 px-2 text-sm" />
        <NavLink to="/risk" label="Risk" class="block py-1 px-2 text-sm" />
        <NavLink to="/recommendations" label="Recommendations" class="block py-1 px-2 text-sm" />

        <button
          @click="exportReport"
          class="btn-primary block mx-2 my-1 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-primary-blue"
          aria-label="Export report"
        >
          Export Report
        </button>
        <button
          @click="toggleTheme"
          class="ml-2 mb-2 p-1 rounded focus:outline-none focus:ring-2 focus:ring-primary-blue hover:bg-card-dark/50"
          :aria-label="isDark.value ? 'Switch to light mode' : 'Switch to dark mode'"
        >
          <ThemeIcon :dark="isDark.value" class="w-4 h-4" aria-hidden="true" />
        </button>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import AnimatedLogo from './AnimatedLogo.vue'
import { useTheme } from '@/composables/useTheme'
import DownloadIcon from '@/components/icons/DownloadIcon.vue'
import ThemeIcon from '@/components/icons/ThemeIcon.vue'

const { isDark, toggleTheme } = useTheme()
const mobileOpen = ref(false)
const route = useRoute()

function toggleMobile() {
  mobileOpen.value = !mobileOpen.value
}
function exportReport() {
  const base = import.meta.env.VITE_API_URL?.endsWith('/api')
    ? import.meta.env.VITE_API_URL.slice(0, -4)
    : import.meta.env.VITE_API_URL || window.location.origin
  window.open(`${base}/report`, '_blank')
}

// Close menu on route change
watch(() => route.fullPath, () => {
  if (mobileOpen.value) mobileOpen.value = false
})
// Lock body scroll when menu open
function lockBodyScroll() { document.body.classList.add('overflow-hidden') }
function unlockBodyScroll() { document.body.classList.remove('overflow-hidden') }
watch(mobileOpen, open => open ? lockBodyScroll() : unlockBodyScroll())
onBeforeUnmount(() => unlockBodyScroll())
</script>

<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: max-height 0.3s ease, opacity 0.3s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  max-height: 0;
  opacity: 0;
}
.slide-fade-enter-to,
.slide-fade-leave-from {
  max-height: 300px;
  opacity: 1;
}
</style>
