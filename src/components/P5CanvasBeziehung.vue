<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import p5 from 'p5'

const props = defineProps({
  data: { type: Array, default: () => [] },
  width: { type: Number, default: 800 },
  height: { type: Number, default: 600 },
  background: { type: [Number, Array, String], default: 255 },
  fontFamily: { type: String, default: 'PxGroteskPan' },
  isMobile: { type: Boolean, default: false },
})

let mountRef = ref(null)
let p5Instance = null
let observer = null

// Beziehungstypen definieren
const beziehungsTypes = [
  { key: 'partner', label: 'Partner', field: 'beziehung_partner' },
  { key: 'verwandt', label: 'verwandt', field: 'beziehung_verwandt' },
  { key: 'bekannt', label: 'bekannt', field: 'beziehung_bekannt' },
  { key: 'arbeit', label: 'Arbeit', field: 'beziehung_arbeit' },
  { key: 'keine', label: 'keine', field: 'beziehung_keine' },
  { key: 'andere', label: 'andere', field: 'beziehung_andere' }
]

const sketch = (p) => {
  let particles = []
  let particleQueue = []
  let selectedData = []
  
  // Globale Zählvariablen
  let totals = {
    partner: 0, verwandt: 0, bekannt: 0,
    arbeit: 0, keine: 0, andere: 0
  }
  
  // Sichtbare Partikel-Zähler
  let visible = {
    partner: 0, verwandt: 0, bekannt: 0,
    arbeit: 0, keine: 0, andere: 0
  }

  const isTablet = window.matchMedia('(pointer: coarse) and (min-width: 740px)').matches
  let crossSize = props.isMobile ? (isTablet ? 14 : 10) : 14
  let crossStrokeWeight = props.isMobile ? (isTablet ? 6 : 4) : 6
  const attractPower = props.isMobile ? 2.0 : 1.5
  const homePower    = props.isMobile ? 0.04 : 0.04
  const repelPower   = props.isMobile ? 2.0 : 2.0
  let fpsCheckDone = false
  let fpsCheckFrame = 0

  p.touchMoved = () => false

  const getResponsiveWidth = () => props.isMobile
    ? Math.max(0, window.innerWidth - 40)
    : props.width

  const getResponsiveHeight = () => props.isMobile
    ? Math.max(300, window.innerHeight - 230)
    : props.height

  p.setup = () => {
    p.createCanvas(getResponsiveWidth(), getResponsiveHeight())
    p.frameRate(props.isMobile ? 30 : 60)
    selectedData = props.data || []
    applyData()
  }

  p.windowResized = () => {
    if (props.isMobile) {
      p.resizeCanvas(getResponsiveWidth(), getResponsiveHeight())
      applyData()
    }
  }

  p.draw = () => {
    p.background(props.background)
    p.textFont('PxGroteskPan')
    const dynamicTextSize = props.isMobile
      ? Math.max(16, Math.min(p.width * 0.09, 45))
      : 60
    p.textSize(dynamicTextSize)
    p.textAlign(p.LEFT, p.BOTTOM)
    p.fill(255)

    // Partikel zeichnen
    const mouseVec = p.createVector(p.mouseX, p.mouseY)
    for (let i = 0; i < particles.length; i++) {
      particles[i].update(p, mouseVec)
      particles[i].display(p)
    }

    // Partikel aus der Queue hinzufügen (alle Typen gleichzeitig)
    let addPerFrame = 5
    
    beziehungsTypes.forEach(type => {
      let typeQueue = particleQueue.filter(particle => particle.beziehung === type.key)
      for (let i = 0; i < addPerFrame && typeQueue.length > 0; i++) {
        let idx = particleQueue.findIndex(particle => particle.beziehung === type.key)
        if (idx !== -1) {
          let particleData = particleQueue.splice(idx, 1)[0]
          particles.push(new Particle(particleData.x, particleData.y, particleData.data, particleData.beziehung, p))
          visible[type.key]++
        }
      }
    })

    drawLabelsAndNumbers(p, dynamicTextSize)
    if (!fpsCheckDone) {
      fpsCheckFrame++
      if (fpsCheckFrame === 120) {
        if (p.frameRate() < 40) p.frameRate(30)
        fpsCheckDone = true
      }
    }
  }

  // Public API für reactive Updates / Resize
  p.updateData = (rows) => {
    selectedData = rows || []
    applyData()
  }
  p.resizeTo = (w, h) => p.resizeCanvas(w, h)

  function drawLabelsAndNumbers(p, textSize) {
    const borderText = 30

    if (props.isMobile) {
      // Mobile: 2 Spalten × 3 Zeilen
      beziehungsTypes.forEach((type, index) => {
        const col = index % 2
        const rowPos = Math.floor(index / 2)
        const cellH = p.height / 3
        const x = col * (p.width / 2) + borderText
        const y = rowPos * cellH + cellH * 0.75
        p.text(type.label, x, y)
        const count = particleQueue.length > 0 ? visible[type.key] : totals[type.key]
        p.text(formatNumber(count), x, y - textSize * 1.1)
      })
    } else {
      // Desktop: 3 Spalten × 2 Zeilen
      const positions = [
        { x: borderText, y: p.height * 0.35 },
        { x: p.width * (1/3) + borderText, y: p.height * 0.35 },
        { x: p.width * (2/3) + borderText, y: p.height * 0.35 },
        { x: borderText, y: p.height * 0.85 },
        { x: p.width * (1/3) + borderText, y: p.height * 0.85 },
        { x: p.width * (2/3) + borderText, y: p.height * 0.85 }
      ]
      beziehungsTypes.forEach((type, index) => {
        p.text(type.label, positions[index].x, positions[index].y)
        const count = particleQueue.length > 0 ? visible[type.key] : totals[type.key]
        p.text(formatNumber(count), positions[index].x, positions[index].y - 70)
      })
    }
  }

  // Ursprünglich: updateParticlesForCurrentSelection → umbenannt zu applyData für klareren Zweck
  function applyData() {
    // Zähler zurücksetzen
    Object.keys(totals).forEach(key => {
      totals[key] = 0
      visible[key] = 0
    })

    particleQueue = []
    particles = []

    let borderCross = 20

    selectedData.forEach(row => {
      beziehungsTypes.forEach((type, index) => {
        let count = row[type.field] || 0
        totals[type.key] += count

        let xStart, xEnd, yStart, yEnd

        if (props.isMobile) {
          // Mobile: 2 Spalten × 3 Zeilen
          const col = index % 2
          const row_pos = Math.floor(index / 2)
          xStart = col * (p.width / 2) + crossSize
          xEnd = (col + 1) * (p.width / 2) - crossSize
          yStart = row_pos * (p.height / 3) + crossSize
          yEnd = (row_pos + 1) * (p.height / 3) - crossSize
        } else {
          // Desktop: 3 Spalten × 2 Zeilen
          const col = index % 3
          const row_pos = Math.floor(index / 3)
          xStart = col === 0 ? crossSize : p.width * (col/3) + borderCross
          xEnd = col === 2 ? p.width - crossSize : p.width * ((col+1)/3) - borderCross
          yStart = row_pos === 0 ? crossSize : p.height * 0.5 + borderCross
          yEnd = row_pos === 0 ? p.height * 0.5 - borderCross : p.height - crossSize
        }

        for (let j = 0; j < count; j++) {
          let px = p.random(xStart, xEnd)
          let py = p.random(yStart, yEnd)
          particleQueue.push({ 
            x: px, 
            y: py, 
            data: row, 
            beziehung: type.key 
          })
        }
      })
    })
    
    p.redraw()
  }

  function formatNumber(num) {
    return (num || 0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, "'")
  }

  class Particle {
    constructor(x, y, data, beziehung, p) {
      this.pos = p.createVector(x, y)
      this.home = p.createVector(x, y)
      this.r = crossSize
      this.initialDelay = 50 + Math.floor(p.random(20))
      this.beziehung = beziehung
    }

    update(p, mouse) {
      if (this.initialDelay > 0) {
        this.initialDelay--
        return
      }

      let distToMouse = p5.Vector.dist(this.pos, mouse)
      let totalForce = p.createVector(0, 0)

      if (distToMouse < 150) {
        let attractionForce = p5.Vector.sub(mouse, this.pos)
        attractionForce.normalize()
        attractionForce.mult(attractPower)
        totalForce.add(attractionForce)
      } else {
        let homeForce = p5.Vector.sub(this.home, this.pos)
        homeForce.mult(homePower)
        totalForce.add(homeForce)
      }

      if (distToMouse < 150) {
        for (let other of particles) {
          if (other !== this) {
            let distance = p5.Vector.dist(this.pos, other.pos)
            if (distance < 80 && distance > 0) {
              let repelForce = p5.Vector.sub(this.pos, other.pos)
              repelForce.normalize()
              repelForce.mult(repelPower / distance)
              totalForce.add(repelForce)
            }
          }
        }
      }

      this.pos.add(totalForce)
      this.constrainPosition(p)
    }

    constrainPosition(p) {
      let typeIndex = beziehungsTypes.findIndex(t => t.key === this.beziehung)
      if (typeIndex === -1) return

      let xMin, xMax, yMin, yMax

      if (props.isMobile) {
        const col = typeIndex % 2
        const row_pos = Math.floor(typeIndex / 2)
        xMin = col * (p.width / 2) + this.r
        xMax = (col + 1) * (p.width / 2) - this.r
        yMin = row_pos * (p.height / 3) + this.r
        yMax = (row_pos + 1) * (p.height / 3) - this.r
      } else {
        const col = typeIndex % 3
        const row_pos = Math.floor(typeIndex / 3)
        xMin = col === 0 ? this.r : p.width * (col/3) + this.r
        xMax = col === 2 ? p.width - this.r : p.width * ((col+1)/3) - this.r
        yMin = row_pos === 0 ? this.r : p.height * 0.5 + this.r
        yMax = row_pos === 0 ? p.height * 0.5 - this.r : p.height - this.r
      }

      this.pos.x = p.constrain(this.pos.x, xMin, xMax)
      this.pos.y = p.constrain(this.pos.y, yMin, yMax)
    }

    display(p) {
      p.push()
      p.translate(this.pos.x, this.pos.y)
      p.rotate(p.PI / 4)
      p.stroke(0)
      p.strokeWeight(crossStrokeWeight)
      p.strokeCap(p.SQUARE)
      let size = 2.5 * this.r
      p.line(-size / 2, 0, size / 2, 0)
      p.line(0, -size / 2, 0, size / 2)
      p.pop()
    }
  }
}

onMounted(() => {
  if (mountRef.value) {
    while (mountRef.value.firstChild) {
      mountRef.value.removeChild(mountRef.value.firstChild)
    }
  }
  observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      if (!p5Instance && props.data && props.data.length > 0) {
        p5Instance = new p5(sketch, mountRef.value)
      } else {
        p5Instance?.loop()
      }
    } else {
      p5Instance?.noLoop()
    }
  }, { threshold: 0 })
  if (mountRef.value) observer.observe(mountRef.value)
})

onBeforeUnmount(() => {
  observer?.disconnect()
  observer = null
  if (p5Instance) {
    p5Instance.remove()
    p5Instance = null
  }
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
