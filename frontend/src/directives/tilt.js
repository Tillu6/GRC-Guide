import VanillaTilt from 'vanilla-tilt'

export default {
  mounted(el, binding) {
    const options = binding.value || {
      max: 15,
      speed: 400,
      glare: true,
      'max-glare': 0.2,
    }
    VanillaTilt.init(el, options)
  },
  unmounted(el) {
    el.vanillaTilt?.destroy()
  }
}

