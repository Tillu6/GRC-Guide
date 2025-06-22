import { ref, onMounted } from 'vue'

export function useTheme() {
  const theme = ref('light')
  onMounted(() => {
    const saved = localStorage.getItem('theme') || 'light'
    theme.value = saved
    document.documentElement.classList.toggle('dark', saved === 'dark')
  })
  function toggleTheme() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
    document.documentElement.classList.toggle('dark', theme.value === 'dark')
    localStorage.setItem('theme', theme.value)
  }
  return { theme, isDark: theme, toggleTheme }
}
