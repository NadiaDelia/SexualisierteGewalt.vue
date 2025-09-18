import { ref, onMounted, onBeforeUnmount } from 'vue'

/**
 * Composable für responsive Sketch-Dimensionen
 * @param {Object} options - Konfiguration für die Dimensionen
 * @param {number} options.widthFactor - Faktor für Breite (default: 0.6)
 * @param {number} options.heightFactor - Faktor für Höhe (default: 0.8)
 * @param {boolean} options.useFullscreen - Vollbild verwenden (default: false)
 */
export function useSketchDimensions(options = {}) {
  const {
    widthFactor = 0.6,
    heightFactor = 0.8,
    useFullscreen = false
  } = options

  const width = ref(0)
  const height = ref(0)

  const calculateDimensions = () => {
    if (useFullscreen) {
      width.value = window.innerWidth
      height.value = window.innerHeight
    } else {
      width.value = Math.round(window.innerWidth * widthFactor)
      height.value = Math.round(window.innerHeight * heightFactor)
    }
  }

  const handleResize = () => {
    calculateDimensions()
  }

  onMounted(() => {
    calculateDimensions()
    window.addEventListener('resize', handleResize)
  })

  onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize)
  })

  return {
    width,
    height
  }
}