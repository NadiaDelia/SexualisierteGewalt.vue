<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import p5 from 'p5'

const props = defineProps({
  // CSV-Zeilen (gefiltert)
  data: { type: Array, default: () => [] },
  width: { type: Number, default: 800 },
  height: { type: Number, default: 600 },
  background: { type: [Number, Array, String], default: 0 },
  showLabels: { type: Boolean, default: true },

  // Spaltennamen – hier standardmäßig auf "beschuldigte_*"
  leftField:  { type: String, default: 'beschuldigte_f' },
  rightField: { type: String, default: 'beschuldigte_m' },

  // Labels
  leftLabel:  { type: String, default: 'Frauen' },
  rightLabel: { type: String, default: 'Männer' },

  // Physik-Parameter
  mouseRadius:   { type: Number, default: 150 },
  repelRadius:   { type: Number, default: 80 },
  attractPower:  { type: Number, default: 1.5 },
  fadeDelayMin:  { type: Number, default: 50 },
  fadeDelayJitter:{ type: Number, default: 20 },
})

const mountRef = ref(null)
let p5Instance = null

const sketch = (p) => {
  let particles = []
  let particleQueue = []
  let sumLeft = 0
  let sumRight = 0

  p.setup = () => {
    p.createCanvas(props.width, props.height)
    p.frameRate(60)
    applyData(props.data)
  }

  p.draw = () => {
    p.background(props.background)
    
    // Update & Draw
    for (let i = 0; i < particles.length; i++) {
      particles[i].update(p, particles, props)
      particles[i].display(p)
    }

    // Gleichzeitiges Einblenden L/R
    const addPerFrame = 5
    for (let k = 0; k < addPerFrame; k++) {
      let iL = particleQueue.findIndex(pt => pt.gender === 'frau')
      if (iL !== -1) {
        const pt = particleQueue.splice(iL, 1)[0]
        particles.push(new Particle(p, pt.x, pt.y, props))
      }
      let iR = particleQueue.findIndex(pt => pt.gender === 'mann')
      if (iR !== -1) {
        const pt = particleQueue.splice(iR, 1)[0]
        particles.push(new Particle(p, pt.x, pt.y, props))
      }
    p.fill(0)

    // Labels
    if (props.showLabels) {
      p.textFont('PxGroteskPan') // kommt aus deinem globalen @font-face
      p.textSize(100)
      p.textAlign(p.LEFT, p.BOTTOM)
      p.text(props.leftLabel,  p.width * 0.05, p.height * 0.7)
      p.text(props.rightLabel, p.width * 0.55, p.height * 0.7)
    }

    // Zahlen, wenn Queue leer
    if (particleQueue.length === 0) {
      p.textFont('PxGroteskPan')
      p.textSize(100)
      p.textAlign(p.LEFT, p.BOTTOM)
      p.text(sumLeft,  p.width * 0.05, p.height * 0.55)
      p.text(sumRight, p.width * 0.55, p.height * 0.55)
    }

    
    }
  }

  // API
  p.updateData = (rows) => applyData(rows)
  p.resizeTo = (w, h) => p.resizeCanvas(w, h)

  function applyData(rows) {
    // Schutz: Canvas muss existieren
    if (!p.width || !p.height) return;
    const leftKey  = props.leftField
    const rightKey = props.rightField

    sumLeft = 0
    sumRight = 0
    particleQueue = []
    particles = []

    for (const row of (rows || [])) {
      const f = Number(row?.[leftKey])  || 0
      const m = Number(row?.[rightKey]) || 0

      sumLeft  += f
      sumRight += m

      for (let j = 0; j < f; j++) {
        const x = p.random(p.width * 0.02, p.width * 0.48)
        const y = p.random(p.height * 0.02, p.height * 0.98)
        particleQueue.push({ x, y, gender: 'frau' })
      }
      for (let j = 0; j < m; j++) {
        const x = p.random(p.width * 0.52, p.width * 0.98)
        const y = p.random(p.height * 0.02, p.height * 0.98)
        particleQueue.push({ x, y, gender: 'mann' })
      }
    }
  }

  class Particle {
    constructor(p, x, y, props) {
      this.pos = p.createVector(x, y)
      this.home = p.createVector(x, y)
      this.r = 12
      this.alpha = 255
      this.targetAlpha = 255
      this.fadeRate = 0.08
      this.growing = true
      this.initialDelay = props.fadeDelayMin + Math.floor(p.random(props.fadeDelayJitter))
      this.col = p.color(255)
    }

    update(p, all, props) {
      // Einblenden
      if (this.growing) {
        if (this.initialDelay > 0) { this.initialDelay--; return }
        this.alpha = p.lerp(this.alpha, this.targetAlpha, this.fadeRate)
        if (this.alpha > 250) { this.alpha = this.targetAlpha; this.growing = false }
      }

      // Kräfte
      const dMouse = p.dist(this.pos.x, this.pos.y, p.mouseX, p.mouseY)
      let fx = 0, fy = 0

      if (dMouse < props.mouseRadius) {
        // Anziehung zur Maus
        const ax = (p.mouseX - this.pos.x)
        const ay = (p.mouseY - this.pos.y)
        const len = Math.max(1e-6, Math.hypot(ax, ay))
        fx += (ax / len) * props.attractPower
        fy += (ay / len) * props.attractPower

        // Abstossung zu nahen Partikeln
        for (const other of all) {
          if (other === this) continue
          const dx = this.pos.x - other.pos.x
          const dy = this.pos.y - other.pos.y
          const dist = Math.hypot(dx, dy)
          if (dist > 0 && dist < props.repelRadius) {
            // näher = stärkere Abstoßung
            const m = 3.0 / dist
            fx += (dx / dist) * m
            fy += (dy / dist) * m
          }
        }
      } else {
        // sanft zur Home-Position zurück
        fx += (this.home.x - this.pos.x) * 0.04
        fy += (this.home.y - this.pos.y) * 0.04
      }

      this.pos.x += fx
      this.pos.y += fy

      // Ränder
      if (this.pos.x < this.r) this.pos.x = this.r
      else if (this.pos.x > p.width - this.r) this.pos.x = p.width - this.r
      if (this.pos.y < this.r) this.pos.y = this.r
      else if (this.pos.y > p.height - this.r) this.pos.y = p.height - this.r
    }

    display(p) {
      p.push()
      p.translate(this.pos.x, this.pos.y)
      p.rotate(p.PI / 4)
      p.stroke(255, 255, 255, this.alpha) // weiß
      p.strokeWeight(6)
      p.strokeCap(p.SQUARE)
      const size = 2.5 * this.r
      p.line(-size / 2, 0, size / 2, 0)
      p.line(0, -size / 2, 0, size / 2)
      p.pop()
    }
  }
}



onMounted(() => {
  // Container leeren, falls noch alte Canvas vorhanden
  if (mountRef.value) {
    while (mountRef.value.firstChild) {
      mountRef.value.removeChild(mountRef.value.firstChild)
    }
  }
  // Nur erzeugen, wenn Daten vorhanden sind
  if (props.data && props.data.length > 0) {
    p5Instance = new p5(sketch, mountRef.value)
  }
})


onBeforeUnmount(() => {
  if (p5Instance) {
    p5Instance.remove()
    p5Instance = null
  }
  // Container leeren
  if (mountRef.value) {
    while (mountRef.value.firstChild) {
      mountRef.value.removeChild(mountRef.value.firstChild)
    }
  }
})



watch(() => props.data, (rows) => {
  // p5-Instanz nur erzeugen, wenn Daten vorhanden sind
  if (!rows || rows.length === 0) return
  if (p5Instance) {
    p5Instance.remove()
    p5Instance = null
  }
  if (mountRef.value) {
    while (mountRef.value.firstChild) {
      mountRef.value.removeChild(mountRef.value.firstChild)
    }
    p5Instance = new p5(sketch, mountRef.value)
  }
}, { deep: true })

watch([() => props.width, () => props.height], ([w, h]) => {
  p5Instance?.resizeTo?.(w, h)
})
</script>

<template>
  <div ref="mountRef" style="display:block; width:100%; height:100%"></div>
</template>
