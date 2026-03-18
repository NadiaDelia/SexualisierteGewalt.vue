import { ref, onMounted, onBeforeUnmount } from 'vue'

/**
 * Composable für responsive Sketch-Dimensionen
 * @param {Object} options
 * @param {number} options.widthFactor    - Faktor für Breite (default: 0.6)
 * @param {number} options.heightFactor   - Faktor für Höhe (default: 0.8)
 * @param {boolean} options.useFullscreen - Vollbild verwenden (default: false)
 * @param {number} options.marginLeft     - Linker Rand des Containers in px (nur Desktop, default: 0)
 *                                          Wird von der Breite abgezogen, damit der Canvas nicht überläuft.
 * @param {number} options.reserveHeight  - Pixel die für Überschrift + Buttons freigehalten werden (nur Desktop, default: 0)
 *                                          Verhindert, dass Buttons auf kleinen Bildschirmen in den nächsten Screen rutschen.
 */
export function useSketchDimensions(options = {}) {
  const {
    widthFactor = 0.6,
    heightFactor = 0.8,
    useFullscreen = false,
    marginLeft = 0,
    reserveHeight = 0
  } = options

  const width = ref(0)
  const height = ref(0)

  const calculateDimensions = () => {
    if (useFullscreen) {
      width.value = window.innerWidth
      height.value = window.innerHeight
    } else {
      const isDesktop = window.innerWidth > 768
      const isSmallDesktop = isDesktop && window.innerHeight <= 780
      if (isSmallDesktop) {
        // Auf kleinen Desktop-Bildschirmen: Canvas zentriert, gleiche Breite wie .text-overlay-content (max 800px)
        width.value = Math.min(window.innerWidth - 80, 800)
        const natural = Math.round(window.innerHeight * heightFactor)
        height.value = reserveHeight > 0 ? Math.min(natural, window.innerHeight - reserveHeight) : natural
      } else {
        // Auf Desktop: linken Rand abziehen, damit Canvas nicht in split-right überläuft
        const effMargin = isDesktop ? marginLeft : 0
        width.value = Math.round((window.innerWidth - effMargin) * widthFactor)
        // Auf Desktop: Platz für Überschrift + Buttons reservieren
        const natural = Math.round(window.innerHeight * heightFactor)
        if (isDesktop && reserveHeight > 0) {
          height.value = Math.min(natural, window.innerHeight - reserveHeight)
        } else {
          height.value = natural
        }
      }
    }
  }

  onMounted(() => {
    calculateDimensions()
    window.addEventListener('resize', calculateDimensions)
  })

  onBeforeUnmount(() => {
    window.removeEventListener('resize', calculateDimensions)
  })

  return {
    width,
    height
  }
}