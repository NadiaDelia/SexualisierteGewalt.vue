
<template>
  <div class="canvas-wrap" ref="container"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import p5 from 'p5'
import * as d3 from 'd3'

const container = ref(null)
let sketch = null

// ---- p5 Instance Sketch: Partikel-Test ----
const createSketch = (p) => {
  let csvData = []
  let dataLoaded = false
  let particles = []

  p.setup = () => {
    p.createCanvas(800, 600)
    p.background(0)
    // CSV laden
    d3.csv('/data_sg.csv', d3.autoType).then((data) => {
      csvData = data
      dataLoaded = true
      // Erzeuge für jede Zeile so viele Partikel wie geschaedigte_f und geschaedigte_m
      particles = []
      csvData.forEach(row => {
        // Frauen links
        for (let i = 0; i < (row.geschaedigte_f || 0); i++) {
          particles.push({
            x: p.random(30, p.width * 0.48),
            y: p.random(30, p.height - 30),
            alpha: 0,
            visible: false
          })
        }
        // Männer rechts
        for (let i = 0; i < (row.geschaedigte_m || 0); i++) {
          particles.push({
            x: p.random(p.width * 0.52, p.width - 30),
            y: p.random(30, p.height - 30),
            alpha: 0,
            visible: false
          })
        }
      })
      p.loop()
    })
    p.noLoop()
  }

  p.draw = () => {
    p.background(0)
    if (dataLoaded) {
      // Animation: Pro Frame erscheinen ein paar Kreuze mehr
      let newlyVisible = 0
      for (let i = 0; i < particles.length; i++) {
        let pt = particles[i]
        if (!pt.visible && newlyVisible < 10) {
          pt.visible = true
          newlyVisible++
        }
        if (pt.visible && pt.alpha < 255) {
          pt.alpha += 20
          if (pt.alpha > 255) pt.alpha = 255
        }
        if (pt.visible) {
          p.push()
          p.translate(pt.x, pt.y)
          p.rotate(p.PI / 4)
          p.stroke(255, pt.alpha)
          p.strokeWeight(4)
          p.strokeCap(p.SQUARE)
          let size = 18
          p.line(-size/2, 0, size/2, 0)
          p.line(0, -size/2, 0, size/2)
          p.pop()
        }
      }
      // Stoppe Animation, wenn alle sichtbar und voll eingeblendet
      if (particles.every(pt => pt.visible && pt.alpha >= 255)) {
        p.noLoop()
      }
      p.fill(255)
      p.textAlign(p.LEFT, p.TOP)
      p.textSize(18)
      p.text('Kreuze: ' + particles.length, 10, 10)
    } else {
      p.fill(255)
      p.textAlign(p.CENTER, p.CENTER)
      p.textSize(32)
      p.text('Lade Daten...', p.width/2, p.height/2)
    }
  }
}


onMounted(() => {
  // Container leeren, falls noch alte Canvas vorhanden
  if (container.value) {
    while (container.value.firstChild) {
      container.value.removeChild(container.value.firstChild)
    }
  }
  sketch = new p5(createSketch, container.value)
})


onBeforeUnmount(() => {
  if (sketch) {
    sketch.remove()
    sketch = null
  }
  // Container leeren
  if (container.value) {
    while (container.value.firstChild) {
      container.value.removeChild(container.value.firstChild)
    }
  }
})
</script>

<style scoped>
.viz {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
}

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.ctl {
  appearance: none;
  border: 1px solid #444;
  background: #121212;
  color: #eaeaea;
  padding: 8px 12px;
  border-radius: 10px;
  cursor: pointer;
  transition: transform .05s ease, background .2s ease, border-color .2s ease;
}
.ctl:hover { background: #1a1a1a; }
.ctl.active {
  background: #2a2a2a;
  border-color: #888;
}

.canvas-wrap {
  width: 100%;
  min-height: 300px; /* tatsächliche Höhe setzt p5 per JS */
  position: relative;
}

canvas {
  display: block;
  width: 100%;
  height: auto;
}


</style>
