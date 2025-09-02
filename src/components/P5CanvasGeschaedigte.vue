<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import p5 from 'p5'

const props = defineProps({
  data: { type: Array, default: () => [] },   // gefilterte CSV-Zeilen [{straftat, geschaedigte_f, geschaedigte_m}, ...]
  background: { type: [Number, Array, String], default: 0 },
  showLabels: { type: Boolean, default: true },
  fontFamily: { type: String, default: 'PxGroteskPan' }, // über CSS @font-face geladen
})

const mountRef = ref(null)
let p5Instance = null
const canvasWidth = ref(Math.floor(window.innerWidth * 0.6))
const canvasHeight = ref(Math.floor(window.innerHeight * 0.8))

const sketch = (p) => {
  // Sketch-State
  let particles = []
  let particleQueue = []
  let selectedData = []
  let gesF = 0
  let gesM = 0

  p.setup = () => {
    p.createCanvas(canvasWidth.value, canvasHeight.value)
    p.frameRate(60)
    applyData(props.data)
  }

  p.draw = () => {
    p.background(props.background)
  if (props.fontFamily) p.textFont(props.fontFamily)

    // Labels
    if (props.showLabels) {
      p.fill(255)
      p.textSize(100)
      p.textAlign(p.LEFT, p.BOTTOM)
      p.text('Frauen', p.width * 0.05, p.height * 0.7)
      p.text('Männer', p.width * 0.55, p.height * 0.7)
    }

    // Zahlen, wenn Queue leer
    if (particleQueue.length === 0) {
      p.fill(255)
      p.textSize(100)
      p.textAlign(p.LEFT, p.BOTTOM)
      p.text(gesF, p.width * 0.05, p.height * 0.55)
      p.text(gesM, p.width * 0.55, p.height * 0.55)
    }

    // Partikel animieren
    for (let i = 0; i < particles.length; i++) {
      particles[i].update(p)
      particles[i].display(p)
    }

    // Gleichzeitiges Einblenden L/R
    const addPerFrame = 5
    for (let k = 0; k < addPerFrame; k++) {
      let iF = particleQueue.findIndex(pt => pt.gender === 'frau')
      if (iF !== -1) {
        const pt = particleQueue.splice(iF, 1)[0]
        particles.push(new Particle(pt.x, pt.y))
      }
      let iM = particleQueue.findIndex(pt => pt.gender === 'mann')
      if (iM !== -1) {
        const pt = particleQueue.splice(iM, 1)[0]
        particles.push(new Particle(pt.x, pt.y))
      }
    }
  }

  // Public API für reactive Updates / Resize
  p.updateData = (rows) => applyData(rows)
  p.resizeTo = (w, h) => p.resizeCanvas(w, h)

  function applyData(rows) {
    // Schutz: Canvas muss existieren und Masse müssen Zahlen sein
    if (!p || typeof p.width !== 'number' || typeof p.height !== 'number' || p.width === 0 || p.height === 0) return;
    selectedData = rows || []
    gesF = 0
    gesM = 0
    particleQueue = []
    particles = []

    for (let i = 0; i < selectedData.length; i++) {
      const row = selectedData[i]
      const f = Number(row?.geschaedigte_f) || 0
      const m = Number(row?.geschaedigte_m) || 0

      gesF += f
      for (let j = 0; j < f; j++) {
        const x = p.random(p.width * 0.02, p.width * 0.48)
        const y = p.random(p.height * 0.02, p.height * 0.98)
        particleQueue.push({ x, y, gender: 'frau' })
      }

      gesM += m
      for (let j = 0; j < m; j++) {
        const x = p.random(p.width * 0.52, p.width * 1.00)
        const y = p.random(p.height * 0.02, p.height * 0.98)
        particleQueue.push({ x, y, gender: 'mann' })
      }
    }
  }

  class Particle {
    constructor(x, y) {
      this.pos = p.createVector(x, y)
      this.home = p.createVector(x, y)
      this.r = 12
      this.alpha = 255
      this.targetAlpha = 255
      this.fadeRate = 0.08
      this.growing = true
      this.initialDelay = 50 + Math.floor(p.random(20))
      this.vel = p.createVector(0, 0)
      this.perturbed = false
      this.perturbTimer = 0
      this.col = p.color(255)
    }
    update(p) {
      // Einblenden
      if (this.growing) {
        if (this.initialDelay > 0) { this.initialDelay--; return }
        this.alpha = p.lerp(this.alpha, this.targetAlpha, this.fadeRate)
        if (this.alpha > 250) { this.alpha = this.targetAlpha; this.growing = false }
      }

      // Mausdistanz (instance-sicher)
      const distToMouse = p.dist(this.pos.x, this.pos.y, p.mouseX, p.mouseY)

      // kurzer „Stoß“
      if (distToMouse < 80 && !this.perturbed) {
        const dir = p.createVector(this.pos.x - p.mouseX, this.pos.y - p.mouseY)
        dir.normalize()
        dir.mult(10 + p.random(3))
        this.vel = dir
        this.perturbed = true
        this.perturbTimer = 10 + Math.floor(p.random(10))
      }

      if (this.perturbed) {
        this.pos.add(this.vel)
        this.vel.mult(0.7)
        this.perturbTimer--
        if (this.perturbTimer <= 0) this.perturbed = false
      } else {
        // sanft zur Home-Position
        const homeDir = p.createVector(this.home.x - this.pos.x, this.home.y - this.pos.y)
        homeDir.mult(0.04)
        this.pos.add(homeDir)
      }

      // Ränder
      if (this.pos.x < this.r) { this.pos.x = this.r; this.vel.x *= -0.5 }
      else if (this.pos.x > p.width - this.r) { this.pos.x = p.width - this.r; this.vel.x *= -0.5 }
      if (this.pos.y < this.r) { this.pos.y = this.r; this.vel.y *= -0.5 }
      else if (this.pos.y > p.height - this.r) { this.pos.y = p.height - this.r; this.vel.y *= -0.5 }
    }
    display(p) {
      p.push()
      p.translate(this.pos.x, this.pos.y)
      p.rotate(p.PI / 4)
      p.stroke(p.red(this.col), p.green(this.col), p.blue(this.col), this.alpha)
      p.strokeWeight(6)
      p.strokeCap(p.SQUARE)
      const size = 2.5 * this.r
      p.line(-size / 2, 0, size / 2, 0)
      p.line(0, -size / 2, 0, size / 2)
      p.pop()
    }
  }
}

function handleResize() {
  canvasWidth.value = Math.floor(window.innerWidth * 0.6)
  canvasHeight.value = Math.floor(window.innerHeight * 0.8)
  if (p5Instance && typeof p5Instance.resizeTo === 'function') {
    p5Instance.resizeTo(canvasWidth.value, canvasHeight.value)
    // Nach Resize: Daten neu anwenden
    if (typeof p5Instance.updateData === 'function') {
      p5Instance.updateData(props.data)
    }
  }
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
  p5Instance = new p5(sketch, mountRef.value)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  p5Instance?.remove()
  p5Instance = null
})

// Reaktive Updates
watch(() => props.data, (rows) => {
  if (
    p5Instance &&
    typeof p5Instance.updateData === 'function' &&
    typeof p5Instance.width === 'number' &&
    typeof p5Instance.height === 'number' &&
    p5Instance.width > 0 &&
    p5Instance.height > 0
  ) {
    p5Instance.updateData(rows)
  }
}, { deep: true })
</script>

<template>
  <div ref="mountRef"
    :style="`display:block; width:${canvasWidth}px; height:${canvasHeight}px;`"
  ></div>
</template>

<style scoped>
/* Nichts nötig – Styling der Schrift kommt global über @font-face */
</style>
