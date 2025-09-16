<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import p5 from 'p5'

const props = defineProps({
  data: { type: Array, default: () => [] },
  width: { type: Number, default: 1000 },
  height: { type: Number, default: 800 },
  background: { type: [Number, Array, String], default: 0 },
  fontFamily: { type: String, default: 'PxGroteskPan' },
  gender: { type: String, default: 'frau' },
})

const mountRef = ref(null)
let p5Instance = null

const sketch = (p) => {
  let particles = [];
  let particleQueue = [];
  let selectedData = [];
  let visiblePrivat = 0;
  let visibleOeffentlich = 0;
  let crossSize = 14;
  let crossStrokeWeight = 6;

  p.setup = () => {
    p.createCanvas(props.width, props.height);
    p.frameRate(60);
    selectedData = props.data || [];
    applyData();
  }

  p.draw = () => {
    p.background(props.background);
    if (props.fontFamily) p.textFont(props.fontFamily);
    p.textSize(90);
    p.textAlign(p.LEFT, p.BOTTOM);
    p.fill(255);

    // Partikel animieren
    for (let i = 0; i < particles.length; i++) {
      particles[i].update(p);
      particles[i].display(p);
    }

    // Kreuze für das aktuell gewählte Geschlecht und Ort
    let privatQueue = particleQueue.filter(pt => pt.gender === props.gender && pt.ort === 'privat');
    let oeffentlichQueue = particleQueue.filter(pt => pt.gender === props.gender && pt.ort === 'oeffentlich');
    let addPerFrame = 5;
    for (let i = 0; i < addPerFrame; i++) {
      if (privatQueue.length > 0) {
        let idx = particleQueue.findIndex(pt => pt.gender === props.gender && pt.ort === 'privat');
        if (idx !== -1) {
          let pt = particleQueue.splice(idx, 1)[0];
          particles.push(new Particle(pt.x, pt.y, pt.data, pt.gender, pt.ort, p));
          visiblePrivat++;
        }
      }
      if (oeffentlichQueue.length > 0) {
        let idx = particleQueue.findIndex(pt => pt.gender === props.gender && pt.ort === 'oeffentlich');
        if (idx !== -1) {
          let pt = particleQueue.splice(idx, 1)[0];
          particles.push(new Particle(pt.x, pt.y, pt.data, pt.gender, pt.ort, p));
          visibleOeffentlich++;
        }
      }
    }

    // Labels
    p.text('Privat', p.width * 0.04, p.height * 0.65);
    p.text('Öffentlich', p.width * 0.54, p.height * 0.65);

    // Zahlen
    p.text(formatNumber(visiblePrivat), p.width * 0.04, p.height * 0.54);
    p.text(formatNumber(visibleOeffentlich), p.width * 0.54, p.height * 0.54);
  };

  // Public API für reactive Updates / Resize
  p.updateData = (rows) => {
    selectedData = rows || [];
    applyData();
  };
  p.resizeTo = (w, h) => p.resizeCanvas(w, h);

  // Ursprünglich: updateParticlesForCurrentSelection → umbenannt zu applyData für klareren Zweck
  function applyData() {
    visiblePrivat = 0;
    visibleOeffentlich = 0;
    particleQueue = [];
    particles = [];
    for (let i = 0; i < selectedData.length; i++) {
      if (props.gender === 'frau') {
        for (let j = 0; j < (selectedData[i].ort_privat_f || 0); j++) {
          let px = p.random(crossSize, p.width * 0.50 - crossSize);
          let py = p.random(crossSize, p.height - crossSize);
          particleQueue.push({ x: px, y: py, data: selectedData[i], ort: 'privat', gender: 'frau' });
        }
        for (let j = 0; j < (selectedData[i].ort_oeffentlich_f || 0); j++) {
          let px = p.random(p.width * 0.50 + crossSize, p.width - crossSize);
          let py = p.random(crossSize, p.height - crossSize);
          particleQueue.push({ x: px, y: py, data: selectedData[i], ort: 'oeffentlich', gender: 'frau' });
        }
      } else {
        for (let j = 0; j < (selectedData[i].ort_privat_m || 0); j++) {
          let px = p.random(crossSize, p.width * 0.50 - crossSize);
          let py = p.random(crossSize, p.height - crossSize);
          particleQueue.push({ x: px, y: py, data: selectedData[i], ort: 'privat', gender: 'mann' });
        }
        for (let j = 0; j < (selectedData[i].ort_oeffentlich_m || 0); j++) {
          let px = p.random(p.width * 0.50 + crossSize, p.width - crossSize);
          let py = p.random(crossSize, p.height - crossSize);
          particleQueue.push({ x: px, y: py, data: selectedData[i], ort: 'oeffentlich', gender: 'mann' });
        }
      }
    }
    p.redraw();
  }

  class Particle {
    constructor(x, y, data, gender, ort, p) {
      this.pos = p.createVector(x, y);
      this.home = p.createVector(x, y);
      this.r = crossSize;
      this.growing = true;
      this.initialDelay = 50 + Math.floor(p.random(20));
      this.gender = gender;
      this.data = data;
      this.ort = ort;
    }
    update(p) {
      if (this.growing) {
        if (this.initialDelay > 0) {
          this.initialDelay--;
          return;
        }
        this.growing = false;
      }
      let mouse = p.createVector(p.mouseX, p.mouseY);
      let distToMouse = p5.Vector.dist(this.pos, mouse);
      let totalForce = p.createVector(0, 0);
      if (distToMouse < 150) {
        let attractionForce = p5.Vector.sub(mouse, this.pos);
        attractionForce.normalize();
        attractionForce.mult(1.5);
        totalForce.add(attractionForce);
      } else {
        let homeForce = p5.Vector.sub(this.home, this.pos);
        homeForce.mult(0.04);
        totalForce.add(homeForce);
      }
      if (distToMouse < 150) {
        for (let other of particles) {
          if (other !== this) {
            let distance = p5.Vector.dist(this.pos, other.pos);
            if (distance < 80 && distance > 0) {
              let repelForce = p5.Vector.sub(this.pos, other.pos);
              repelForce.normalize();
              repelForce.mult(3.0 / distance);
              totalForce.add(repelForce);
            }
          }
        }
      }
      this.pos.add(totalForce);
      if (this.ort === 'privat') {
        this.pos.x = p.constrain(this.pos.x, this.r, p.width * 0.5 - this.r);
      } else if (this.ort === 'oeffentlich') {
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
      p.stroke(0);
      p.strokeWeight(crossStrokeWeight);
      p.strokeCap(p.SQUARE);
      let size = 2.5 * this.r;
      p.line(-size / 2, 0, size / 2, 0);
      p.line(0, -size / 2, 0, size / 2);
      p.pop();
    }
  }

  //1000er-Trennzeichen
  function formatNumber(num) {
    return (num || 0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, "’");
  }
};

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

watch([() => props.width, () => props.height], ([w, h]) => {
  p5Instance?.resizeTo?.(w, h)
})
</script>

<template>
  <div ref="mountRef" style="display:block; width:100%; height:100%"></div>
</template>

<!-- Kein scoped CSS, Styling kommt aus style.css -->