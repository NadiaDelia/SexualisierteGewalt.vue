<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'
import p5 from 'p5'

const props = defineProps({
  width: { type: Number, default: window.innerWidth },
  height: { type: Number, default: window.innerHeight },
  background: { type: [Number, String], default: 0 },
  fontFamily: { type: String, default: 'PxGroteskPan' }
})

const mountRef = ref(null)
let p5Instance = null

const sketch = (p) => {
  let particles = []
  let crossSize = 20
  let crossStrokeWeight = 10
  let anzahlKreuze = 500

  p.setup = () => {
    p.createCanvas(props.width, props.height)
    
    // Partikel/Kreuze zufällig auf dem Canvas verteilen
    for (let i = 0; i < anzahlKreuze; i++) {
      let px = p.random(crossSize, props.width - crossSize)
      let py = p.random(crossSize, props.height - crossSize)
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
    p.resizeCanvas(props.width, props.height)
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
      this.pos.x = p.constrain(this.pos.x, this.r, props.width - this.r)
      this.pos.y = p.constrain(this.pos.y, this.r, props.height - this.r)
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
  if (mountRef.value) {
    p5Instance = new p5(sketch, mountRef.value)
  }
})

onBeforeUnmount(() => {
  if (p5Instance) {
    p5Instance.remove()
    p5Instance = null
  }
})
</script>

<template>
  <div ref="mountRef"></div>
</template>

<style scoped>
div {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
