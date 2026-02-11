<template>
  <div :id="canvasId" class="p5-canvas-container"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import p5 from 'p5'

// Props definieren
const props = defineProps({
  width: {
    type: Number,
    default: 800
  },
  height: {
    type: Number,
    default: 600
  },
  background: {
    type: [Number, String],
    default: 0
  },
  fontFamily: {
    type: String,
    default: 'PxGroteskPan'
  },
  triggerFall: {
    type: Boolean,
    default: false
  },
  resetCounter: {
    type: Number,
    default: 0
  }
})

// Eindeutige Canvas-ID generieren
const canvasId = ref(`p5-canvas-falling-crosses-${Math.random().toString(36).substr(2, 9)}`)

let p5Instance = null
let globalFallCrosses = false

// p5.js Sketch definieren
const sketch = (p) => {
  let particles = []
  let crossSize = 20
  let crossStrokeWeight = 10
  let anzahlKreuze = 50

  // Particle Klasse
  class Particle {
    constructor(x, y) {
      this.pos = p.createVector(x, y)
      this.home = p.createVector(x, y)
      this.r = crossSize
      this.growing = true
      this.initialDelay = 50 + p.int(p.random(20))
      this.vel = p.createVector(0, 0)
      this.perturbed = false
      this.perturbTimer = 0
      this.falling = false
      this.fallDelay = 0
      this.gravity = 0.7 + p.random(0.2, 1.2)
      this.vy = 0
      this.vx = p.random(-1, 1)
      this.hasFallen = false
    }

    update() {
      if (this.growing) {
        if (this.initialDelay > 0) {
          this.initialDelay--
          return
        }
      }

      let mouse = p.createVector(p.mouseX, p.mouseY)
      let distToMouse = p5.Vector.dist(this.pos, mouse)

      if (distToMouse < 80 && !this.perturbed) {
        let dir = p5.Vector.sub(this.pos, mouse)
        dir.normalize()
        dir.mult(10 + p.random(5))
        this.vel = dir
        this.perturbed = true
        this.perturbTimer = 10 + p.int(p.random(10))
      }

      if (this.perturbed) {
        this.pos.add(this.vel)
        this.vel.mult(0.7)
        this.perturbTimer--
        if (this.perturbTimer <= 0) {
          this.perturbed = false
        }
      } else {
        let homeDir = p5.Vector.sub(this.home, this.pos)
        homeDir.mult(0.04)
        this.pos.add(homeDir)
      }

      // Begrenzung: Partikel bleiben auf dem Canvas
      // Menü-Bereich ausschließen (vertikal mittig, rechts)
      const menuTop = p.height * 0.25
      const menuBottom = p.height * 0.75
      const menuRight = p.width - 80
      
      this.pos.x = p.constrain(this.pos.x, this.r, p.width - this.r)
      this.pos.y = p.constrain(this.pos.y, this.r, p.height - this.r)
      
      // Wenn im Menü-Bereich (vertikal), nicht zu weit rechts
      if (this.pos.y > menuTop && this.pos.y < menuBottom && this.pos.x > menuRight) {
        this.pos.x = menuRight
      }
    }

    display() {
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

  p.setup = () => {
    p.createCanvas(props.width, props.height)

    // Menü-Bereich definieren (vertikal mittig, rechts)
    const menuTop = p.height * 0.35
    const menuBottom = p.height * 0.65
    const menuRight = p.width - 80

    particles = []
    for (let i = 0; i < anzahlKreuze; i++) {
      let px, py
      let attempts = 0
      
      // Platzierung mit Menü-Ausschluss
      do {
        px = p.random(crossSize, p.width - crossSize)
        py = p.random(crossSize, p.height - crossSize)
        attempts++
      } while (py > menuTop && py < menuBottom && px > menuRight && attempts < 50)
      
      particles.push(new Particle(px, py))
    }
    
    window.globalParticles = particles
    
    window.globalResetParticles = () => {
      
      particles = []
      for (let i = 0; i < anzahlKreuze; i++) {
        let px, py
        let attempts = 0
        
        do {
          px = p.random(crossSize, p.width - crossSize)
          py = p.random(crossSize, p.height - crossSize)
          attempts++
        } while (py > menuTop && py < menuBottom && px > menuRight && attempts < 50)
        
        particles.push(new Particle(px, py))
        
        if (i < 5) {
        }
      }
      
      window.globalParticles = particles
    }
  }

  p.draw = () => {
    if (props.background === 'transparent') {
      p.clear()
    } else {
      p.background(props.background)
    }

    for (let i = particles.length - 1; i >= 0; i--) {
      let particle = particles[i]
      
      if (globalFallCrosses) {
        if (!particle.falling) {
          particle.fallDelay = p.int(p.random(0, 40))
          particle.falling = true
        }
        if (particle.fallDelay > 0) {
          particle.fallDelay--
        } else {
          particle.vy += particle.gravity
          particle.pos.y += particle.vy
          particle.pos.x += particle.vx
        }
        if (particle.pos.y - particle.r > p.height) {
          particle.hasFallen = true
          particle.pos.y = p.height + 100
          continue
        }
      } else {
        particle.update()
      }
      
      if (!particle.hasFallen) {
        particle.display()
      }
    }
  }

  p.windowResized = () => {
    p.resizeCanvas(props.width, props.height)
  }
}

onMounted(() => {
  
  setTimeout(() => {
    const container = document.getElementById(canvasId.value)
    if (container) {
      try {
        p5Instance = new p5(sketch, container)
      } catch (error) {
        console.error('Error creating p5 instance:', error)
      }
    }
  }, 100)
})

onBeforeUnmount(() => {
  if (p5Instance) {
    try {
      p5Instance.remove()
      p5Instance = null
    } catch (error) {
      console.error('Error cleaning up p5 instance:', error)
    }
  }
  if (window.globalParticles) {
    delete window.globalParticles
  }
  if (window.globalResetParticles) {
    delete window.globalResetParticles
  }
})

watch([() => props.width, () => props.height], () => {
  if (p5Instance) {
    p5Instance.resizeCanvas(props.width, props.height)
  }
})

watch(() => props.triggerFall, (newVal) => {
  if (newVal && p5Instance) {
    globalFallCrosses = true
    window.globalFallCrosses = true
  } else if (!newVal) {
    globalFallCrosses = false
    window.globalFallCrosses = false
  }
})

watch(() => props.resetCounter, (newVal, oldVal) => {
  if (newVal > oldVal && p5Instance) {
    
    globalFallCrosses = false
    window.globalFallCrosses = false
    
    if (window.globalResetParticles) {
      window.globalResetParticles()
    }
    
  }
})
</script>
