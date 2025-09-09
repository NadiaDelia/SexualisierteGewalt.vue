<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import p5 from 'p5'

const props = defineProps({
  data: { type: Array, default: () => [] },
  background: { type: [Number, Array, String], default: 0 },
  showLabels: { type: Boolean, default: true },
  fontFamily: { type: String, default: 'PxGroteskPan' },
})

const mountRef = ref(null)
let p5Instance = null
const canvasWidth = ref(1000)
const canvasHeight = ref(800)

const sketch = (p) => {
  let particles = [];
  let particleQueue = [];
  let selectedData;
  let geschaedigteFrauen = 0;
  let geschaedigteMaenner = 0;
  let visibleFrauen = 0;
  let visibleMaenner = 0;
  let crossSize = 14;
  let crossStrokeWeight = 6;

  let customFont = null;

  p.setup = () => {
    p.createCanvas(canvasWidth.value, canvasHeight.value)
    p.frameRate(60)
    applyData(props.data)
  }

  p.draw = () => {
  p.background(props.background)
  if (props.fontFamily) p.textFont(props.fontFamily)
  p.textSize(90)
  p.textAlign(p.LEFT, p.BOTTOM)
  p.fill(255)

    // Labels
    p.text('Frauen', p.width * 0.04, p.height * 0.65)
    p.text('Männer', p.width * 0.54, p.height * 0.65)

    // Zahlen während Animation (hochzählen)
    if (particleQueue.length > 0) {
      p.text(formatNumber(visibleFrauen), p.width * 0.04, p.height * 0.54)
      p.text(formatNumber(visibleMaenner), p.width * 0.54, p.height * 0.54)
    } else {
      p.text(formatNumber(geschaedigteFrauen), p.width * 0.04, p.height * 0.54)
      p.text(formatNumber(geschaedigteMaenner), p.width * 0.54, p.height * 0.54)
    }

    // Partikel animieren
    for (let i = 0; i < particles.length; i++) {
      particles[i].update(p)
      particles[i].display(p)
    }

    // Kreuze für Frauen und Männer gleichzeitig erscheinen lassen
    let addPerFrame = 5;
    for (let i = 0; i < addPerFrame; i++) {
      // Frauen hinzufügen
      let frauIdx = particleQueue.findIndex(pt => pt.gender === 'frau');
      if (frauIdx !== -1) {
        let pt = particleQueue.splice(frauIdx, 1)[0];
        particles.push(new Particle(pt.x, pt.y, pt.data, pt.gender, p));
        visibleFrauen++;
      }
      // Männer hinzufügen
      let mannIdx = particleQueue.findIndex(pt => pt.gender === 'mann');
      if (mannIdx !== -1) {
        let pt = particleQueue.splice(mannIdx, 1)[0];
        particles.push(new Particle(pt.x, pt.y, pt.data, pt.gender, p));
        visibleMaenner++;
      }
    }
  }

  // Public API für reactive Updates / Resize
  p.updateData = (rows) => applyData(rows)
  p.resizeTo = (w, h) => p.resizeCanvas(w, h)

  function applyData(rows) {
    selectedData = rows || [];
    geschaedigteFrauen = 0;
    geschaedigteMaenner = 0;
    visibleFrauen = 0;
    visibleMaenner = 0;
    particleQueue = [];
    particles = [];
    for (let i = 0; i < selectedData.length; i++) {
      geschaedigteFrauen += Number(selectedData[i].geschaedigte_f) || 0;
      for (let j = 0; j < (Number(selectedData[i].geschaedigte_f) || 0); j++) {
        let px = p.random(crossSize, p.width * 0.5 - crossSize);
        let py = p.random(crossSize, p.height - crossSize);
        particleQueue.push({ x: px, y: py, data: selectedData[i], gender: 'frau' });
      }
      geschaedigteMaenner += Number(selectedData[i].geschaedigte_m) || 0;
      for (let j = 0; j < (Number(selectedData[i].geschaedigte_m) || 0); j++) {
        let px = p.random(p.width * 0.50 + crossSize, p.width - crossSize);
        let py = p.random(crossSize, p.height - crossSize);
        particleQueue.push({ x: px, y: py, data: selectedData[i], gender: 'mann' });
      }
    }
  }

  class Particle {
    constructor(x, y, data, gender, p) {
      this.pos = p.createVector(x, y);
      this.home = p.createVector(x, y);
      this.r = crossSize;
      this.growing = true;
      this.initialDelay = 50 + Math.floor(p.random(20));
      this.vel = p.createVector(0, 0);
      this.perturbed = false;
      this.perturbTimer = 0;
      this.data = data;
      this.gender = gender;
    }
    update(p) {
      if (this.growing) {
        if (this.initialDelay > 0) {
          this.initialDelay--;
          return;
        }
      }
      let mouse = p.createVector(p.mouseX, p.mouseY);
      let distToMouse = p5.Vector.dist(this.pos, mouse);
      if (distToMouse < 80 && !this.perturbed) {
        let dir = p5.Vector.sub(this.pos, mouse);
        dir.normalize();
        dir.mult(10 + p.random(3));
        this.vel = dir;
        this.perturbed = true;
        this.perturbTimer = 10 + Math.floor(p.random(10));
      }
      if (this.perturbed) {
        this.pos.add(this.vel);
        this.vel.mult(0.7);
        this.perturbTimer--;
        if (this.perturbTimer <= 0) {
          this.perturbed = false;
        }
      } else {
        let homeDir = p5.Vector.sub(this.home, this.pos);
        homeDir.mult(0.04);
        this.pos.add(homeDir);
      }
      if (this.gender === 'frau') {
        this.pos.x = p.constrain(this.pos.x, this.r, p.width * 0.5 - this.r);
      } else if (this.gender === 'mann') {
        this.pos.x = p.constrain(this.pos.x, p.width * 0.5 + this.r, p.width - this.r);
      }
      if (this.pos.y < this.r) {
        this.pos.y = this.r;
      } else if (this.pos.y > p.height - this.r) {
        this.pos.y = p.height - this.r;
      }
    }
    display(p) {
      p.push();
      p.translate(this.pos.x, this.pos.y);
      p.rotate(p.PI / 4);
      p.stroke(255);
      p.strokeWeight(crossStrokeWeight);
      p.strokeCap(p.SQUARE);
      let size = 2.5 * this.r;
      p.line(-size / 2, 0, size / 2, 0);
      p.line(0, -size / 2, 0, size / 2);
      p.pop();
    }
  }

  function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "’");
  }
}

function handleResize() {
  canvasWidth.value = 1000;
  canvasHeight.value = 800;
  if (p5Instance && typeof p5Instance.resizeTo === 'function') {
    p5Instance.resizeTo(canvasWidth.value, canvasHeight.value)
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

watch(() => props.data, (rows) => {
  if (
    p5Instance &&
    typeof p5Instance.updateData === 'function'
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
