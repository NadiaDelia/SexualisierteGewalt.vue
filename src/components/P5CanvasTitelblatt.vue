<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'
import p5 from 'p5'

const props = defineProps({
  width: { type: Number, default: window.innerWidth },
  height: { type: Number, default: window.innerHeight },
  background: { type: [Number, String], default: 0 },
  fontFamily: { type: String, default: 'PxGroteskPan' },
  isMobile: { type: Boolean, default: false }
})

const mountRef = ref(null)
let p5Instance = null
let observer = null

const sketch = (p) => {
  let particles = []
  let crossSize = props.isMobile ? 16 : 20
  let crossStrokeWeight = props.isMobile ? 8 : 10
  let anzahlKreuze = props.isMobile ? 150 : 500

  p.setup = () => {
    // Responsive: Portrait für Mobile, Landscape für Desktop
    let w = props.width
    let h = props.height
    if (props.isMobile) {
      w = window.innerWidth
      h = window.innerHeight
    }
    p.createCanvas(w, h)

    // Menü-Bereich definieren (vertikal mittig, rechts)
    const menuTop = h * 0.35
    const menuBottom = h * 0.65
    const menuRight = w - 80

    // Partikel/Kreuze zufällig auf dem Canvas verteilen
    for (let i = 0; i < anzahlKreuze; i++) {
      let px, py
      let attempts = 0

      if (props.isMobile) {
        // Auf Mobile: keine Menü-Ausschluss-Logik
        px = p.random(0, w)
        py = p.random(0, h)
      } else {
        // Desktop: Menü-Bereich ausschließen
        do {
          px = p.random(0, w)
          py = p.random(0, h)
          attempts++
        } while (py > menuTop && py < menuBottom && px > menuRight && attempts < 50)
      }

      particles.push(new Particle(px, py, p))
    }
  }

  p.draw = () => {
    if (props.background === 'transparent') {
      p.clear()
    } else {
      p.background(props.background)
    }
    
    for (let i = 0; i < particles.length; i++) {
      particles[i].update(p)
      particles[i].display(p)
    }
  }

  p.windowResized = () => {
    let w = props.width
    let h = props.height
    if (props.isMobile) {
      w = window.innerWidth
      h = window.innerHeight
    }
    p.resizeCanvas(w, h)
  }

  class Particle {
    constructor(x, y, p) {
      this.pos = p.createVector(x, y)
      this.home = p.createVector(x, y)
      this.r = crossSize
      this.growing = true
      this.initialDelay = 50 + p.int(p.random(20))
      this.vel = p.createVector(0, 0)
      this.perturbed = false
      this.perturbTimer = 0
    }
    
    update(p) {
      if (this.growing) {
        if (this.initialDelay > 0) {
          this.initialDelay--
          return
        }
      }

      let mouse = p.createVector(p.mouseX, p.mouseY)
      let distToMouse = p5.Vector.dist(this.pos, mouse)

      // Wenn Maus in der Nähe: Partikel kurz wegstossen
      if (distToMouse < 80 && !this.perturbed) {
        let dir = p5.Vector.sub(this.pos, mouse)
        dir.normalize()
        dir.mult(10 + p.random(3))
        this.vel = dir
        this.perturbed = true
        this.perturbTimer = 10 + p.int(p.random(10))
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
        homeDir.mult(0.04)
        this.pos.add(homeDir)
      }

      // Begrenzung: Partikel bleiben auf dem Canvas
      // Menü-Bereich ausschließen (vertikal mittig, rechts) – nur Desktop
      const menuTop = props.height * 0.25
      const menuBottom = props.height * 0.75
      const menuRight = props.width - 80

      this.pos.x = p.constrain(this.pos.x, this.r, props.width - this.r)
      this.pos.y = p.constrain(this.pos.y, this.r, props.height - this.r)

      if (!props.isMobile) {
        // Wenn im Menü-Bereich (vertikal), nicht zu weit rechts (nur Desktop)
        if (this.pos.y > menuTop && this.pos.y < menuBottom && this.pos.x > menuRight) {
          this.pos.x = menuRight
        }
      }
    }

    display(p) {
      // Kreuz
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
  observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      if (!p5Instance && mountRef.value) p5Instance = new p5(sketch, mountRef.value)
      else p5Instance?.loop()
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
})
</script>

<template>
  <div ref="mountRef" class="p5-canvas-titlepage"></div>
</template>
