import { ref, onMounted } from 'vue'
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js'

Chart.register(ArcElement, Tooltip, Legend)

const canvasRef = ref(null)

onMounted(() => {
  const ctx = canvasRef.value.getContext('2d')
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Compliant', 'Non-Compliant', 'Partial'],
      datasets: [{
        data: [compliantCount.value, nonCompliantCount.value, partiallyCompliantCount.value],
        backgroundColor: [
          'rgba(26, 175, 156, 0.8)',  // teal
          'rgba(255, 99, 132, 0.8)',  // red-ish
          'rgba(255, 205, 86, 0.8)'   // yellow-ish
        ],
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      animation: {
        animateScale: true,
        animateRotate: true,
        duration: 1000,
        easing: 'easeOutBack'
      },
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#fff'
          }
        }
      }
    }
  })
})
