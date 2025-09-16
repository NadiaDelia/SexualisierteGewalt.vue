<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import p5 from 'p5'

const props = defineProps({
  data: { type: Array, default: () => [] },
  width: { type: Number, default: 800 },
  height: { type: Number, default: 600 },
  background: { type: [Number, Array, String], default: 255 },
  fontFamily: { type: String, default: 'PxGroteskPan' },
})

let mountRef = ref(null)
let p5Instance = null

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

  let crossSize = 14
  let crossStrokeWeight = 6

  p.setup = () => {
    p.createCanvas(props.width, props.height)
    p.frameRate(60)
    selectedData = props.data || []
    applyData()
  }

  p.draw = () => {
    p.background(props.background)
    p.textFont('PxGroteskPan')
    p.textSize(60)
    p.textAlign(p.LEFT, p.BOTTOM)
    p.fill(255)

    // Partikel zeichnen
    for (let i = 0; i < particles.length; i++) {
      particles[i].update(p)
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

    drawLabelsAndNumbers(p)
  }

  // Public API für reactive Updates / Resize
  p.updateData = (rows) => {
    selectedData = rows || []
    applyData()
  }
  p.resizeTo = (w, h) => p.resizeCanvas(w, h)

  function drawLabelsAndNumbers(p) {
    let borderText = 30
    
    // Positionen für 3x2 Grid
    const positions = [
      { x: borderText, y: props.height * 0.35 }, // Partner (oben links)
      { x: props.width * (1/3) + borderText, y: props.height * 0.35 }, // verwandt (oben mitte)
      { x: props.width * (2/3) + borderText, y: props.height * 0.35 }, // bekannt (oben rechts)
      { x: borderText, y: props.height * 0.85 }, // Arbeit (unten links)
      { x: props.width * (1/3) + borderText, y: props.height * 0.85 }, // keine (unten mitte)
      { x: props.width * (2/3) + borderText, y: props.height * 0.85 }  // andere (unten rechts)
    ]

    // Labels zeichnen
    beziehungsTypes.forEach((type, index) => {
      p.text(type.label, positions[index].x, positions[index].y)
      
      // Zahlen zeichnen
      let count = particleQueue.length > 0 ? visible[type.key] : totals[type.key]
      p.text(formatNumber(count), positions[index].x, positions[index].y - 70)
    })
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

        // Positionen für 3x2 Grid berechnen
        let col = index % 3
        let row_pos = Math.floor(index / 3)
        
        let xStart = col === 0 ? crossSize : props.width * (col/3) + borderCross
        let xEnd = col === 2 ? props.width - crossSize : props.width * ((col+1)/3) - borderCross
        let yStart = row_pos === 0 ? crossSize : props.height * 0.5 + borderCross
        let yEnd = row_pos === 0 ? props.height * 0.5 - borderCross : props.height - crossSize

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

    update(p) {
      if (this.initialDelay > 0) {
        this.initialDelay--
        return
      }

      let mouse = p.createVector(p.mouseX, p.mouseY)
      let distToMouse = p5.Vector.dist(this.pos, mouse)
      let totalForce = p.createVector(0, 0)

      if (distToMouse < 150) {
        let attractionForce = p5.Vector.sub(mouse, this.pos)
        attractionForce.normalize()
        attractionForce.mult(1.5)
        totalForce.add(attractionForce)
      } else {
        let homeForce = p5.Vector.sub(this.home, this.pos)
        homeForce.mult(0.04)
        totalForce.add(homeForce)
      }

      if (distToMouse < 150) {
        for (let other of particles) {
          if (other !== this) {
            let distance = p5.Vector.dist(this.pos, other.pos)
            if (distance < 80 && distance > 0) {
              let repelForce = p5.Vector.sub(this.pos, other.pos)
              repelForce.normalize()
              repelForce.mult(3.0 / distance)
              totalForce.add(repelForce)
            }
          }
        }
      }

      this.pos.add(totalForce)
      this.constrainPosition(p)
    }

    constrainPosition(p) {
      // Finde Index der Beziehung
      let typeIndex = beziehungsTypes.findIndex(t => t.key === this.beziehung)
      if (typeIndex === -1) return

      let col = typeIndex % 3
      let row_pos = Math.floor(typeIndex / 3)
      
      let xMin = col === 0 ? this.r : props.width * (col/3) + this.r
      let xMax = col === 2 ? props.width - this.r : props.width * ((col+1)/3) - this.r
      let yMin = row_pos === 0 ? this.r : props.height * 0.5 + this.r
      let yMax = row_pos === 0 ? props.height * 0.5 - this.r : props.height - this.r

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
