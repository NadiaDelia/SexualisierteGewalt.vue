<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import p5 from 'p5'

const props = defineProps({
  data: { type: Array, default: () => [] },
  width: { type: Number, default: 1000 },
  height: { type: Number, default: 800 },
  background: { type: [Number, Array, String], default: 0 },
  fontFamily: { type: String, default: 'PxGroteskPan' },
  dunkelziffer: { type: String, default: 'hell' }, // 'hell' oder 'dunkel'
})

const mountRef = ref(null)
let p5Instance = null

const sketch = (p) => {
  let particles = []
  let particleQueue = []
  let selectedData = []
  let totalParticleCount = 0
  let visibleFrau = 0
  let visibleMann = 0

  const crossSize = 14
  const crossStrokeWeight = 6

  p.setup = () => {
    p.createCanvas(props.width, props.height)
    p.frameRate(60)
    selectedData = props.data || []
    applyData()
  }

  p.draw = () => {
    // Transparenter Hintergrund wenn background === 'transparent'
    if (props.background === 'transparent') {
      p.clear()
    } else {
      p.background(props.background)
    }
    if (props.fontFamily) p.textFont(props.fontFamily)
    p.fill(255)

    totalParticleCount = particles.length

    // Partikel zeichnen
    for (let i = 0; i < particles.length; i++) {
      particles[i].update(p)
      particles[i].display(p)
    }

    // Progressive Beschleunigung für Partikel-Animation
    let queueSize = particleQueue.length
    let totalParticles = particles.length + queueSize
    let progress = particles.length / Math.max(totalParticles, 1)

    let addPerFrame
    if (totalParticles <= 50) {
      addPerFrame = 5
    } else if (totalParticles <= 500) {
      let minSpeed = 8
      let maxSpeed = 20
      addPerFrame = Math.floor(minSpeed + (maxSpeed - minSpeed) * progress * progress)
    } else if (totalParticles <= 2000) {
      let minSpeed = 15
      let maxSpeed = 60
      addPerFrame = Math.floor(minSpeed + (maxSpeed - minSpeed) * progress * progress)
    } else if (totalParticles <= 9000) {
      let minSpeed = 25
      let maxSpeed = 200
      addPerFrame = Math.floor(minSpeed + (maxSpeed - minSpeed) * progress * progress)
    } else {
      let minSpeed = 200
      let maxSpeed = 2000
      addPerFrame = Math.floor(minSpeed + (maxSpeed - minSpeed) * progress * progress)
    }

    addPerFrame = Math.max(5, addPerFrame)

    // Ausgewogene Verteilung zwischen Frauen und Männern
    let addedFrau = 0
    let addedMann = 0
    let maxPerGender = Math.ceil(addPerFrame / 2)

    for (let i = particleQueue.length - 1; i >= 0 && (addedFrau + addedMann) < addPerFrame; i--) {
      let particle = particleQueue[i]
      if (particle.dunkelziffer === props.dunkelziffer) {
        if (particle.gender === 'frau' && addedFrau < maxPerGender) {
          particleQueue.splice(i, 1)
          
          let newX = particle.x
          let newY = particle.y

          if (props.dunkelziffer === 'dunkel') {
            // Progressive Expansion für "tatsächlich"
            let totalCurrentVisible = particles.filter(p => p.dunkelziffer === 'dunkel').length
            let totalQueueRemaining = particleQueue.filter(q => q.dunkelziffer === 'dunkel').length
            let totalTarget = totalCurrentVisible + totalQueueRemaining

            let globalProgress = totalCurrentVisible / Math.max(totalTarget, 1)
            let expansionFactor = 0.1 + globalProgress * 0.9

            let centerX = props.width / 2
            let centerY = props.height / 2
            let areaWidth = 1000
            let areaHeight = 800

            let baseMinX = centerX - areaWidth / 2
            let baseMaxX = centerX
            let baseMinY = centerY - areaHeight / 2
            let baseMaxY = centerY + areaHeight / 2

            let expandedMinX = baseMinX - (baseMinX - 0) * expansionFactor
            let expandedMaxX = baseMaxX
            let expandedMinY = baseMinY - (baseMinY - 0) * expansionFactor
            let expandedMaxY = baseMaxY + (props.height - baseMaxY) * expansionFactor

            newX = p.random(expandedMinX, expandedMaxX)
            newY = p.random(expandedMinY, expandedMaxY)
          }

          particles.push(new Particle(newX, newY, particle.data, particle.dunkelziffer, particle.gender, p))
          addedFrau++
        } else if (particle.gender === 'mann' && addedMann < maxPerGender) {
          particleQueue.splice(i, 1)
          
          let newX = particle.x
          let newY = particle.y

          if (props.dunkelziffer === 'dunkel') {
            // Progressive Expansion für "tatsächlich"
            let totalCurrentVisible = particles.filter(p => p.dunkelziffer === 'dunkel').length
            let totalQueueRemaining = particleQueue.filter(q => q.dunkelziffer === 'dunkel').length
            let totalTarget = totalCurrentVisible + totalQueueRemaining

            let globalProgress = totalCurrentVisible / Math.max(totalTarget, 1)
            let expansionFactor = 0.1 + globalProgress * 0.9

            let centerX = props.width / 2
            let centerY = props.height / 2
            let areaWidth = 1000
            let areaHeight = 800

            let baseMinX = centerX
            let baseMaxX = centerX + areaWidth / 2
            let baseMinY = centerY - areaHeight / 2
            let baseMaxY = centerY + areaHeight / 2

            let expandedMinX = baseMinX
            let expandedMaxX = baseMaxX + (props.width - baseMaxX) * expansionFactor
            let expandedMinY = baseMinY - (baseMinY - 0) * expansionFactor
            let expandedMaxY = baseMaxY + (props.height - baseMaxY) * expansionFactor

            newX = p.random(expandedMinX, expandedMaxX)
            newY = p.random(expandedMinY, expandedMaxY)
          }

          particles.push(new Particle(newX, newY, particle.data, particle.dunkelziffer, particle.gender, p))
          addedMann++
        }
      }
    }

    // Aktuell sichtbare Partikel zählen
    visibleFrau = particles.filter(particle => particle.gender === 'frau').length
    visibleMann = particles.filter(particle => particle.gender === 'mann').length

    // Responsive, vertikal zentrierte Zahlen und Labels
    let zahlSize = 90
    let abstand = 40
    let frauenText = "Frauen"
    let maennerText = "Männer"
    let frauenBreite = p.textWidth(frauenText)
    let blockHeight = zahlSize + 10 + zahlSize
    let blockCenterY = props.height / 2 - blockHeight / 2

    let frauenX = props.width / 2 - abstand - frauenBreite
    let maennerX = props.width / 2 + abstand

    p.textSize(zahlSize)
    p.textAlign(p.LEFT, p.TOP)
    p.text(formatNumber(visibleFrau), frauenX, blockCenterY)
    p.text(formatNumber(visibleMann), maennerX, blockCenterY)
    p.text(frauenText, frauenX, blockCenterY + zahlSize + 10)
    p.text(maennerText, maennerX, blockCenterY + zahlSize + 10)
  }

  // Public API für reactive Updates / Resize
  p.updateData = (rows) => {
    selectedData = rows || []
    applyData()
  }
  p.updateDunkelziffer = (dunkelziffer) => {
    updateDunkelzifferTransition()
  }
  p.resizeTo = (w, h) => {
    p.resizeCanvas(w, h)
    applyData()
  }

  // Ursprünglich: updateParticlesForCurrentSelection → umbenannt zu applyData für klareren Zweck
  function applyData() {
    particleQueue = []
    particles = []
    visibleFrau = 0
    visibleMann = 0

    for (let i = 0; i < selectedData.length; i++) {
      if (props.dunkelziffer === 'hell') {
        // Bei "registriert" - getrennte Geschlechterverteilung in 1000x800px Bereich
        let centerX = props.width / 2
        let centerY = props.height / 2
        let areaWidth = 1000
        let areaHeight = 800

        // Frauen Hellfeld - linke Hälfte des zentrierten Bereichs
        for (let j = 0; j < (selectedData[i].geschaedigte_f || 0); j++) {
          let px = p.random(centerX - areaWidth / 2, centerX)
          let py = p.random(centerY - areaHeight / 2, centerY + areaHeight / 2)
          particleQueue.push({ x: px, y: py, data: selectedData[i], gender: 'frau', dunkelziffer: 'hell' })
        }
        // Männer Hellfeld - rechte Hälfte des zentrierten Bereichs
        for (let j = 0; j < (selectedData[i].geschaedigte_m || 0); j++) {
          let px = p.random(centerX, centerX + areaWidth / 2)
          let py = p.random(centerY - areaHeight / 2, centerY + areaHeight / 2)
          particleQueue.push({ x: px, y: py, data: selectedData[i], gender: 'mann', dunkelziffer: 'hell' })
        }
      } else {
        // Bei "tatsächlich" - expandierende Verteilung über den ganzen Bildschirm
        let centerX = props.width / 2

        // Frauen Dunkelfeld - linke Bildschirmhälfte
        for (let j = 0; j < (selectedData[i].geschaedigte_f_dz || 0); j++) {
          let px = p.random(0, centerX)
          let py = p.random(0, props.height)
          particleQueue.push({ x: px, y: py, data: selectedData[i], gender: 'frau', dunkelziffer: 'dunkel' })
        }
        // Männer Dunkelfeld - rechte Bildschirmhälfte
        for (let j = 0; j < (selectedData[i].geschaedigte_m_dz || 0); j++) {
          let px = p.random(centerX, props.width)
          let py = p.random(0, props.height)
          particleQueue.push({ x: px, y: py, data: selectedData[i], gender: 'mann', dunkelziffer: 'dunkel' })
        }
      }
    }
    p.redraw()
  }

  function updateDunkelzifferTransition() {
    // Berechne Zielwerte für aktuelle Auswahl
    let targetFrau = 0
    let targetMann = 0

    for (let i = 0; i < selectedData.length; i++) {
      if (props.dunkelziffer === 'hell') {
        targetFrau += selectedData[i].geschaedigte_f || 0
        targetMann += selectedData[i].geschaedigte_m || 0
      } else {
        targetFrau += selectedData[i].geschaedigte_f_dz || 0
        targetMann += selectedData[i].geschaedigte_m_dz || 0
      }
    }

    // Aktuelle Anzahl der sichtbaren Partikel
    let currentFrau = particles.filter(particle => particle.gender === 'frau').length
    let currentMann = particles.filter(particle => particle.gender === 'mann').length

    // Wenn wir mehr Partikel brauchen (von hell zu dunkel) - zur Queue hinzufügen
    if (targetFrau > currentFrau) {
      let needed = targetFrau - currentFrau
      let centerX = props.width / 2
      let centerY = props.height / 2
      let areaWidth = 1000
      let areaHeight = 800

      for (let i = 0; i < needed; i++) {
        let px, py
        if (props.dunkelziffer === 'hell') {
          px = p.random(centerX - areaWidth / 2, centerX)
          py = p.random(centerY - areaHeight / 2, centerY + areaHeight / 2)
        } else {
          let totalFrauenPartikel = targetFrau
          let currentParticleIndex = currentFrau + i
          let progress = currentParticleIndex / Math.max(totalFrauenPartikel - 1, 1)
          let expansionFactor = 0.1 + progress * 0.9

          let baseMinX = centerX - areaWidth / 2
          let baseMaxX = centerX
          let baseMinY = centerY - areaHeight / 2
          let baseMaxY = centerY + areaHeight / 2

          let expandedMinX = baseMinX - (baseMinX - 0) * expansionFactor
          let expandedMaxX = baseMaxX
          let expandedMinY = baseMinY - (baseMinY - 0) * expansionFactor
          let expandedMaxY = baseMaxY + (props.height - baseMaxY) * expansionFactor

          px = p.random(expandedMinX, expandedMaxX)
          py = p.random(expandedMinY, expandedMaxY)
        }
        particleQueue.push({ x: px, y: py, data: selectedData[0], gender: 'frau', dunkelziffer: props.dunkelziffer })
      }
    } else if (targetFrau < currentFrau) {
      let toRemove = currentFrau - targetFrau
      for (let i = particles.length - 1; i >= 0 && toRemove > 0; i--) {
        if (particles[i].gender === 'frau') {
          particles.splice(i, 1)
          toRemove--
        }
      }
    }

    // Das gleiche für Männer
    if (targetMann > currentMann) {
      let needed = targetMann - currentMann
      let centerX = props.width / 2
      let centerY = props.height / 2
      let areaWidth = 1000
      let areaHeight = 800

      for (let i = 0; i < needed; i++) {
        let px, py
        if (props.dunkelziffer === 'hell') {
          px = p.random(centerX, centerX + areaWidth / 2)
          py = p.random(centerY - areaHeight / 2, centerY + areaHeight / 2)
        } else {
          let totalMännerPartikel = targetMann
          let currentParticleIndex = currentMann + i
          let progress = currentParticleIndex / Math.max(totalMännerPartikel - 1, 1)
          let expansionFactor = 0.1 + progress * 0.9

          let baseMinX = centerX
          let baseMaxX = centerX + areaWidth / 2
          let baseMinY = centerY - areaHeight / 2
          let baseMaxY = centerY + areaHeight / 2

          let expandedMinX = baseMinX
          let expandedMaxX = baseMaxX + (props.width - baseMaxX) * expansionFactor
          let expandedMinY = baseMinY - (baseMinY - 0) * expansionFactor
          let expandedMaxY = baseMaxY + (props.height - baseMaxY) * expansionFactor

          px = p.random(expandedMinX, expandedMaxX)
          py = p.random(expandedMinY, expandedMaxY)
        }
        particleQueue.push({ x: px, y: py, data: selectedData[0], gender: 'mann', dunkelziffer: props.dunkelziffer })
      }
    } else if (targetMann < currentMann) {
      let toRemove = currentMann - targetMann
      for (let i = particles.length - 1; i >= 0 && toRemove > 0; i--) {
        if (particles[i].gender === 'mann') {
          particles.splice(i, 1)
          toRemove--
        }
      }
    }
  }

  function formatNumber(num) {
    return (num || 0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, "’")
  }

  class Particle {
    constructor(x, y, data, dunkelziffer, gender, p) {
      this.pos = p.createVector(x, y)
      this.home = p.createVector(x, y)
      this.r = crossSize
      this.growing = true
      this.initialDelay = 50 + Math.floor(p.random(20))
      this.vel = p.createVector(0, 0)
      this.perturbed = false
      this.perturbTimer = 0
      this.dunkelziffer = dunkelziffer
      this.gender = gender
    }

    update(p) {
      if (this.growing && this.initialDelay > 0) {
        this.initialDelay--
      }

      // Mouse-Interaction
      if (totalParticleCount > 15000) {
        // Optimierte Berechnung für viele Partikel
        let dx = this.pos.x - p.mouseX
        let dy = this.pos.y - p.mouseY
        let roughDist = Math.abs(dx) + Math.abs(dy)

        if (roughDist < 200) {
          let distSquared = dx * dx + dy * dy

          if (distSquared < 10000) {
            let force = Math.max(15, 25 - Math.sqrt(distSquared) / 4)
            let magnitude = Math.sqrt(distSquared)
            if (magnitude > 0) {
              this.vel.x = (dx / magnitude) * (force + p.random(5))
              this.vel.y = (dy / magnitude) * (force + p.random(5))
              this.perturbed = true
              this.perturbTimer = 2 + Math.floor(p.random(2))
            }
          }
        }
      } else {
        // Normale Berechnung für weniger Partikel
        let mouse = p.createVector(p.mouseX, p.mouseY)
        let distToMouse = p5.Vector.dist(this.pos, mouse)

        if (distToMouse < 80 && !this.perturbed) {
          let dir = p5.Vector.sub(this.pos, mouse)
          dir.normalize()
          dir.mult(10 + p.random(3))
          this.vel = dir
          this.perturbed = true
          this.perturbTimer = 2 + Math.floor(p.random(2))
        }
      }

      // Wenn gestört, Bewegung auslaufen lassen
      if (this.perturbed) {
        this.pos.add(this.vel)
        this.vel.mult(0.7)
        this.perturbTimer--
        if (this.perturbTimer <= 0) {
          this.perturbed = false
        }
      } else {
        // Sanft zur Ausgangsposition zurück
        let homeDir = p5.Vector.sub(this.home, this.pos)
        homeDir.mult(0.08)
        this.pos.add(homeDir)
      }

      // Grenzlogik basierend auf dem Dunkelziffer-Modus
      let centerX = props.width / 2
      let centerY = props.height / 2
      let areaWidth = 1000
      let areaHeight = 800

      if (this.dunkelziffer === 'hell') {
        // Bei "registriert" - getrennte Geschlechterverteilung im zentrierten Bereich
        if (this.gender === 'frau') {
          this.pos.x = p.constrain(this.pos.x, centerX - areaWidth / 2 + this.r, centerX - this.r)
          this.pos.y = p.constrain(this.pos.y, centerY - areaHeight / 2 + this.r, centerY + areaHeight / 2 - this.r)
        } else if (this.gender === 'mann') {
          this.pos.x = p.constrain(this.pos.x, centerX + this.r, centerX + areaWidth / 2 - this.r)
          this.pos.y = p.constrain(this.pos.y, centerY - areaHeight / 2 + this.r, centerY + areaHeight / 2 - this.r)
        }
      } else {
        // Bei "tatsächlich" - expandierende Verteilung über den ganzen Bildschirm
        if (this.gender === 'frau') {
          this.pos.x = p.constrain(this.pos.x, this.r, centerX - this.r)
          this.pos.y = p.constrain(this.pos.y, this.r, props.height - this.r)
        } else if (this.gender === 'mann') {
          this.pos.x = p.constrain(this.pos.x, centerX + this.r, props.width - this.r)
          this.pos.y = p.constrain(this.pos.y, this.r, props.height - this.r)
        }
      }
    }

    display(p) {
      p.push()
      p.translate(this.pos.x, this.pos.y)
      p.rotate(p.PI / 4)
      p.stroke(255)
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
  if (props.data && props.data.length > 0) {
    p5Instance = new p5(sketch, mountRef.value)
  }
})

onBeforeUnmount(() => {
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

watch(() => props.dunkelziffer, () => {
  if (p5Instance && p5Instance.updateDunkelziffer) {
    p5Instance.updateDunkelziffer(props.dunkelziffer)
  }
})

watch([() => props.width, () => props.height], ([w, h]) => {
  p5Instance?.resizeTo?.(w, h)
})
</script>

<template>
  <div ref="mountRef" style="display:block; width:100%; height:100%"></div>
</template>
