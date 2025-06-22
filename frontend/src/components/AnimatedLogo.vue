<!-- src/components/AnimatedLogo.vue -->
<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 100 100"
    :class="[
      sizeClass,
      'text-neon-teal',
      'shadow-neon-md',
      'transition-shadow duration-300',
      'cursor-pointer'
    ]"
    role="img"
    aria-label="GRC Nexus Logo"
  >
    <!-- Static pentagon -->
    <polygon
      points="50,5 95,35 78,90 22,90 5,35"
      fill="currentColor"
      stroke="currentColor"
      stroke-width="2"
    />
    <!-- Animated checkmark -->
    <polyline
      ref="checkmarkRef"
      class="checkmark"
      points="30,55 45,70 75,35"
      fill="none"
      stroke="#ffffff"
      stroke-width="6"
      stroke-linecap="round"
      stroke-linejoin="round"
    />
  </svg>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'w-2 h-2'
  }
})
const sizeClass = computed(() => props.size)
const checkmarkRef = ref(null)

onMounted(() => {
  const el = checkmarkRef.value
  if (el && el.getTotalLength) {
    try {
      const length = el.getTotalLength()
      el.style.strokeDasharray = length
      el.style.strokeDashoffset = length
    } catch {}
  }
})
</script>

<style scoped>
@keyframes draw-check {
  to { stroke-dashoffset: 0; }
}
@keyframes check-pulse {
  0%,100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}
.checkmark {
  animation:
    draw-check 0.4s ease-out forwards,
    check-pulse 2s ease-in-out 0.5s infinite alternate;
  transform-origin: center;
}
/* Hover glow on checkmark */
svg:hover .checkmark {
  filter: drop-shadow(0 0 4px #ffffff) drop-shadow(0 0 8px #ffffff);
}
</style>
