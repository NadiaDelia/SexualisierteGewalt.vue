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
})// Eindeutige Canvas-ID generieren
const canvasId = ref(`p5-canvas-falling-crosses-${Math.random().toString(36).substr(2, 9)}`)

let p5Instance = null

// Globale Variable für den Fall-Trigger
let globalFallCrosses = false

// p5.js Sketch definieren
const sketch = (p) => {
    let particles = []
    let crossSize = 20
    let crossStrokeWeight = 10
    let anzahlKreuze = 50
    let customFont

    // Particle Klasse innerhalb des Sketches definieren
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
            // Für das physikalische Fallen
            this.falling = false
            this.fallDelay = 0
            this.fallSpeed = 0
            this.gravity = 0.7 + p.random(0.2, 1.2) // individuelle Schwerkraft
            this.vy = 0 // vertikale Geschwindigkeit
            this.vx = p.random(-1, 1) // leichte horizontale Bewegung
            this.hasFallen = false // Flag für gefallene Particles
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

            // Wenn Maus in der Nähe: Partikel kurz wegstossen
            if (distToMouse < 80 && !this.perturbed) {
                let dir = p5.Vector.sub(this.pos, mouse)
                dir.normalize()
                dir.mult(10 + p.random(5))
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

        display() {
            // Kreuz
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

    p.setup = () => {
        p.createCanvas(props.width, props.height)

        // Partikel/Kreuze zufällig auf dem Canvas verteilen
        particles = []
        for (let i = 0; i < anzahlKreuze; i++) {
            let px = p.random(crossSize, props.width - crossSize)
            let py = p.random(crossSize, props.height - crossSize)
            particles.push(new Particle(px, py))
        }
        
        // Global verfügbar machen für Reset-Funktion
        window.globalParticles = particles
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
                    // Initialisiere Fallverhalten beim ersten Mal
                    particle.fallDelay = p.int(p.random(0, 40)) // bis zu 1 Sekunde Verzögerung
                    particle.falling = true
                }
                if (particle.fallDelay > 0) {
                    particle.fallDelay--
                } else {
                    particle.vy += particle.gravity // Beschleunigung
                    particle.pos.y += particle.vy
                    particle.pos.x += particle.vx // leichte horizontale Bewegung
                }
                if (particle.pos.y - particle.r > props.height) {
                    // Particle nicht entfernen, sondern als "gefallen" markieren
                    particle.hasFallen = true
                    particle.pos.y = props.height + 100 // Weit außerhalb des sichtbaren Bereichs
                    continue
                }
            } else {
                particle.update()
            }
            
            // Nur anzeigen wenn das Particle nicht gefallen ist
            if (!particle.hasFallen) {
                particle.display()
            }
        }
    }

    p.windowResized = () => {
        p.resizeCanvas(props.width, props.height)
    }
}

// Component lifecycle
onMounted(() => {
    console.log('🔥 P5CanvasForderungen MOUNTED!')
    console.log('Canvas ID:', canvasId.value)
    console.log('Props:', props)

    // Kleine Verzögerung um sicherzustellen, dass der DOM bereit ist
    setTimeout(() => {
        const container = document.getElementById(canvasId.value)
        console.log('Container found:', container)
        if (container) {
            try {
                // Instance Mode explizit verwenden
                p5Instance = new p5(sketch, container)
                console.log('p5 Instance created:', p5Instance)
            } catch (error) {
                console.error('Error creating p5 instance:', error)
            }
        } else {
            console.error('Container not found!')
        }
    }, 100)
})

onBeforeUnmount(() => {
    console.log('🔥 P5CanvasForderungen UNMOUNTING!')
    if (p5Instance) {
        try {
            p5Instance.remove()
            p5Instance = null
            console.log('p5 Instance cleaned up')
        } catch (error) {
            console.error('Error cleaning up p5 instance:', error)
        }
    }
})

// Watch für Props-Änderungen
watch([() => props.width, () => props.height], () => {
    if (p5Instance) {
        p5Instance.resizeCanvas(props.width, props.height)
    }
})

// Watch für Fall-Trigger
watch(() => props.triggerFall, (newVal) => {
    console.log('🔥 Trigger Fall received:', newVal)
    if (newVal && p5Instance) {
        globalFallCrosses = true
        window.globalFallCrosses = true
        console.log('🔥 Global fall crosses set to true!')
    } else if (!newVal) {
        // Beim expliziten Zurücksetzen auch stoppen
        globalFallCrosses = false
        window.globalFallCrosses = false
        console.log('🛑 Fall crosses stopped via prop')
    }
})

// Watch für Reset-Counter
watch(() => props.resetCounter, (newVal, oldVal) => {
    if (newVal > oldVal && p5Instance) {
        console.log('🔄 Reset triggered via prop, counter:', newVal)
        
        // Direkt im p5 Sketch resetten
        globalFallCrosses = false
        window.globalFallCrosses = false
        
        // Falls keine Particles da sind, neue erstellen
        if (window.globalParticles && window.globalParticles.length === 0) {
            console.log('🔄 Creating new particles for reset')
            for (let i = 0; i < 50; i++) {
                let px = p5Instance.random(20, props.width - 20)
                let py = p5Instance.random(20, props.height - 20)
                let newParticle = {
                    pos: p5Instance.createVector(px, py),
                    home: p5Instance.createVector(px, py),
                    falling: false,
                    hasFallen: false,
                    vy: 0,
                    vx: 0
                }
                window.globalParticles.push(newParticle)
            }
        } else if (window.globalParticles) {
            // Bestehende Particles zurücksetzen
            for (let particle of window.globalParticles) {
                particle.pos.x = particle.home.x
                particle.pos.y = particle.home.y
                particle.falling = false
                particle.hasFallen = false
                particle.vy = 0
                particle.vx = 0
            }
        }
        
        console.log('✅ Reset complete via prop')
    }
})

// Component lifecycle
onMounted(() => {
    console.log('🔥 P5CanvasForderungen MOUNTED!')
    console.log('Canvas ID:', canvasId.value)
    console.log('Props:', props)

    // Kleine Verzögerung um sicherzustellen, dass der DOM bereit ist
    setTimeout(() => {
        const container = document.getElementById(canvasId.value)
        console.log('Container found:', container)
        if (container) {
            try {
                p5Instance = new p5(sketch, container)
                console.log('p5 Instance created:', p5Instance)
            } catch (error) {
                console.error('Error creating p5 instance:', error)
            }
        } else {
            console.error('Container not found!')
        }
    }, 100)
})

// Cleanup beim Unmount
onBeforeUnmount(() => {
    if (p5Instance) {
        p5Instance.remove()
    }
    if (window.globalParticles) {
        delete window.globalParticles
    }
})
</script>

<style scoped>
.p5-canvas-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
}
</style>