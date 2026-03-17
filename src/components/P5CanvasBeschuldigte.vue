<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import p5 from 'p5'

const props = defineProps({
  data: { type: Array, default: () => [] },
  width: { type: Number, default: 800 },
  height: { type: Number, default: 600 },
  background: { type: [Number, Array, String], default: 0 },
  fontFamily: { type: String, default: 'PxGroteskPan' },
  isMobile: { type: Boolean, default: false }
})

const mountRef = ref(null)
let p5Instance = null
let observer = null

// Responsive width/height logic
const getResponsiveWidth = () => {
  if (props.isMobile) {
    return Math.max(0, window.innerWidth - 40)
  }
  return props.width
}
const getResponsiveHeight = () => {
  if (props.isMobile) {
    return Math.max(320, Math.min(window.innerHeight * 0.7, 700))
  }
  return props.height
}

const sketch = (p) => {
  // --- Variablen aus deinem Sketch ---
  let particles = [];
  let particleQueue = [];
  let selectedData = [];
  let beschuldigteFrauen = 0;
  let beschuldigteMaenner = 0;
  let visibleFrauen = 0;
  let visibleMaenner = 0;
  let crossSize = props.isMobile ? 10 : 14;
  let crossStrokeWeight = props.isMobile ? 4 : 6;
  const attractPower = props.isMobile ? 2.0 : 1.5; // Die Kreuze werden stärker von der Maus angezogen bei höherem Wert
  const homePower    = props.isMobile ? 0.04 : 0.04; // Die Kreuze kehren stärker zu ihrem Ursprungsort zurück bei höherem Wert
  const repelPower   = props.isMobile ? 2.0 : 2.0; // Die Kreuze stossen sich stärker gegenseitig ab bei höherem Wert

  p.setup = () => {
    p.createCanvas(getResponsiveWidth(), getResponsiveHeight());
    p.frameRate(props.isMobile ? 30 : 60);
    applyData(props.data);
  };

  p.windowResized = () => {
    p.resizeCanvas(getResponsiveWidth(), getResponsiveHeight())
    applyData(props.data)
  }

  p.touchMoved = () => false // Verhindert Scrollen auf Mobile, wenn man über das Canvas wischt

  // --- Draw ---
  p.draw = () => {
    p.background(props.background);
    if (props.fontFamily) p.textFont(props.fontFamily);
    const dynamicTextSize = props.isMobile
      ? Math.max(20, Math.min(p.width * 0.14, 90))
      : Math.max(18, Math.min(p.width * 0.13, 90))
    p.textSize(dynamicTextSize);
    p.textAlign(p.LEFT, p.BOTTOM);
    p.fill(255);

    // Partikel zeichnen
    const mouseVec = p.createVector(p.mouseX, p.mouseY);
    for (let i = 0; i < particles.length; i++) {
      particles[i].update(p, mouseVec);
      particles[i].display(p);
    }

    // Kreuze für Frauen und Männer gleichzeitig erscheinen lassen
    let addPerFrame = 5;
    for (let i = 0; i < addPerFrame; i++) {
      let frauIdx = particleQueue.findIndex(pt => pt.gender === 'frau');
      if (frauIdx !== -1) {
        let pt = particleQueue.splice(frauIdx, 1)[0];
        particles.push(new Particle(pt.x, pt.y, pt.data, pt.gender, p));
        visibleFrauen++;
      }
      let mannIdx = particleQueue.findIndex(pt => pt.gender === 'mann');
      if (mannIdx !== -1) {
        let pt = particleQueue.splice(mannIdx, 1)[0];
        particles.push(new Particle(pt.x, pt.y, pt.data, pt.gender, p));
        visibleMaenner++;
      }
    }

    // Text über Kreuzen zeichnen
    if (props.isMobile) {
      p.textAlign(p.CENTER, p.CENTER);
      const cx = p.width / 2;
      const half = p.height / 2;
      const frauenYNum = half * 0.4;
      const frauenYLabel = half * 0.6;
      const maennerYNum = half + half * 0.4;
      const maennerYLabel = half + half * 0.6;
      const maennerYLabelClamped = Math.min(maennerYLabel, p.height - dynamicTextSize * 0.5);
      const frauenNum = particleQueue.length > 0 ? formatNumber(visibleFrauen) : formatNumber(beschuldigteFrauen);
      const maennerNum = particleQueue.length > 0 ? formatNumber(visibleMaenner) : formatNumber(beschuldigteMaenner);
      p.text(frauenNum, cx, frauenYNum);
      p.text('Frauen', cx, frauenYLabel);
      p.text(maennerNum, cx, maennerYNum);
      p.text('Männer', cx, maennerYLabelClamped);
    } else {
      p.textAlign(p.LEFT, p.CENTER);
      p.text("Frauen", p.width * 0.04, p.height * 0.65);
      p.text("Männer", p.width * 0.54, p.height * 0.65);
      if (particleQueue.length > 0) {
        p.text(formatNumber(visibleFrauen), p.width * 0.04, p.height * 0.54);
        p.text(formatNumber(visibleMaenner), p.width * 0.54, p.height * 0.54);
      } else {
        p.text(formatNumber(beschuldigteFrauen), p.width * 0.04, p.height * 0.54);
        p.text(formatNumber(beschuldigteMaenner), p.width * 0.54, p.height * 0.54);
      }
    }
  };

  // Public API
  p.updateData = (rows) => applyData(rows);
  p.resizeTo = (w, h) => p.resizeCanvas(w, h);

  // --- Partikel-Update ---
  function applyData(rows) {
    beschuldigteFrauen = 0;
    beschuldigteMaenner = 0;
    visibleFrauen = 0;
    visibleMaenner = 0;
    particleQueue = [];
    particles = [];
    selectedData = rows || [];
    for (let i = 0; i < selectedData.length; i++) {
      beschuldigteFrauen += Number(selectedData[i].beschuldigte_f) || 0;
      for (let j = 0; j < (Number(selectedData[i].beschuldigte_f) || 0); j++) {
        let px, py;
        if (props.isMobile) {
          px = p.random(crossSize, p.width - crossSize);
          py = p.random(crossSize, p.height / 2 - crossSize);
        } else {
          px = p.random(crossSize, p.width * 0.50 - crossSize);
          py = p.random(crossSize, p.height - crossSize);
        }
        particleQueue.push({ x: px, y: py, data: selectedData[i], gender: 'frau' });
      }
      beschuldigteMaenner += Number(selectedData[i].beschuldigte_m) || 0;
      for (let j = 0; j < (Number(selectedData[i].beschuldigte_m) || 0); j++) {
        let px, py;
        if (props.isMobile) {
          px = p.random(crossSize, p.width - crossSize);
          py = p.random(p.height / 2 + crossSize, p.height - crossSize);
        } else {
          px = p.random(p.width * 0.50 + crossSize, p.width - crossSize);
          py = p.random(crossSize, p.height - crossSize);
        }
        particleQueue.push({ x: px, y: py, data: selectedData[i], gender: 'mann' });
      }
    }
    p.redraw();
  }

  // --- Zahl formatieren ---
  function formatNumber(num) {
    return (num || 0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, "’");
  }

  // --- Particle-Klasse ---
  class Particle {
    constructor(x, y, data, gender, p) {
      this.pos = p.createVector(x, y);
      this.home = p.createVector(x, y);
      this.r = crossSize;
      this.growing = true;
      this.initialDelay = 50 + Math.floor(p.random(20));
      this.gender = gender;
    }
    update(p, mouse) {
      if (this.growing) {
        if (this.initialDelay > 0) {
          this.initialDelay--;
          return;
        }
      }
      let distToMouse = p5.Vector.dist(this.pos, mouse);
      let totalForce = p.createVector(0, 0);
      if (distToMouse < 150) {
        let attractionForce = p5.Vector.sub(mouse, this.pos);
        attractionForce.normalize();
        attractionForce.mult(attractPower);
        totalForce.add(attractionForce);
      } else {
        let homeForce = p5.Vector.sub(this.home, this.pos);
        homeForce.mult(homePower);
        totalForce.add(homeForce);
      }
      if (distToMouse < 150) {
        for (let other of particles) {
          if (other !== this) {
            let distance = p5.Vector.dist(this.pos, other.pos);
            if (distance < 80 && distance > 0) {
              let repelForce = p5.Vector.sub(this.pos, other.pos);
              repelForce.normalize();
              repelForce.mult(repelPower / distance);
              totalForce.add(repelForce);
            }
          }
        }
      }
      this.pos.add(totalForce);
      // Grenzlogik
      if (props.isMobile) {
        if (this.gender === 'frau') {
          this.pos.x = p.constrain(this.pos.x, this.r, p.width - this.r);
          this.pos.y = p.constrain(this.pos.y, this.r, p.height / 2 - this.r);
        } else if (this.gender === 'mann') {
          this.pos.x = p.constrain(this.pos.x, this.r, p.width - this.r);
          this.pos.y = p.constrain(this.pos.y, p.height / 2 + this.r, p.height - this.r);
        }
      } else {
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
};



onMounted(() => {
  observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      if (!p5Instance) p5Instance = new p5(sketch, mountRef.value)
      else p5Instance.loop()
    } else {
      p5Instance?.noLoop()
    }
  }, { threshold: 0 })
  if (mountRef.value) observer.observe(mountRef.value)
})

onBeforeUnmount(() => {
  observer?.disconnect()
  observer = null
  p5Instance?.remove()
  p5Instance = null
})

watch(() => props.data, (rows) => {
  if (p5Instance && typeof p5Instance.updateData === 'function') {
    p5Instance.updateData(rows)
  }
}, { deep: true })
</script>

<template>
  <div ref="mountRef"
    :style="
      props.isMobile
        ? `display:block; width:calc(100vw - 40px); height:${getResponsiveHeight()}px; max-width:100vw; margin:0 auto;`
        : `display:block; width:${getResponsiveWidth()}px; height:${getResponsiveHeight()}px; max-width:100%; margin:0 auto;`
    "
  ></div>
</template>