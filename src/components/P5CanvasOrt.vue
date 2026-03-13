<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import p5 from 'p5'

const props = defineProps({
  data: { type: Array, default: () => [] },
  width: { type: Number, default: 1000 },
  height: { type: Number, default: 800 },
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
  let particles = [];
  let particleQueue = [];
  let selectedData = [];
  let visiblePrivat = 0;
  let visibleOeffentlich = 0;
  let crossSize = props.isMobile ? 10 : 14;
  let crossStrokeWeight = props.isMobile ? 4 : 6;
  const attractPower = props.isMobile ? 1.5 : 1.5;
  const homePower    = props.isMobile ? 0.07 : 0.04;
  const repelPower   = props.isMobile ? 1.0 : 2.0;
  let fpsCheckDone = false;
  let fpsCheckFrame = 0;

  p.setup = () => {
    p.createCanvas(getResponsiveWidth(), getResponsiveHeight());
    p.frameRate(props.isMobile ? 30 : 60);
    applyData(props.data);
  }

  p.windowResized = () => {
    p.resizeCanvas(getResponsiveWidth(), getResponsiveHeight())
    applyData(props.data)
  }

  p.draw = () => {
    p.background(props.background);
    if (props.fontFamily) p.textFont(props.fontFamily);
    const dynamicTextSize = props.isMobile
      ? Math.max(20, Math.min(p.width * 0.14, 90))
      : Math.max(18, Math.min(p.width * 0.13, 90))
    p.textSize(dynamicTextSize);
    p.textAlign(p.LEFT, p.BOTTOM);
    p.fill(255);

    // Partikel animieren
    const mouseVec = p.createVector(p.mouseX, p.mouseY);
    for (let i = 0; i < particles.length; i++) {
      particles[i].update(p, mouseVec);
      particles[i].display(p);
    }

    // Neue Kreuze hinzufügen
    let addPerFrame = 5;
    for (let i = 0; i < addPerFrame; i++) {
      let privatIdx = particleQueue.findIndex(pt => pt.ort === 'privat');
      if (privatIdx !== -1) {
        let pt = particleQueue.splice(privatIdx, 1)[0];
        particles.push(new Particle(pt.x, pt.y, pt.data, pt.ort, p));
        visiblePrivat++;
      }
      let oeffentlichIdx = particleQueue.findIndex(pt => pt.ort === 'oeffentlich');
      if (oeffentlichIdx !== -1) {
        let pt = particleQueue.splice(oeffentlichIdx, 1)[0];
        particles.push(new Particle(pt.x, pt.y, pt.data, pt.ort, p));
        visibleOeffentlich++;
      }
    }

    // Text über Kreuzen zeichnen
    if (props.isMobile) {
      p.textAlign(p.LEFT, p.CENTER);
      const half = p.height / 2;
      const privatYNum = half * 0.4;
      const privatYLabel = half * 0.6;
      const oeffentlichYNum = half + half * 0.4;
      const oeffentlichYLabel = half + half * 0.6;
      const oeffentlichYLabelClamped = Math.min(oeffentlichYLabel, p.height - dynamicTextSize * 0.5);
      const privatLabel = 'privat';
      const oeffentlichLabel = 'öffentlich';
      const privatNum = formatNumber(visiblePrivat);
      const oeffentlichNum = formatNumber(visibleOeffentlich);
      const privatBlockWidth = Math.max(p.textWidth(privatLabel), p.textWidth(privatNum));
      const oeffentlichBlockWidth = Math.max(p.textWidth(oeffentlichLabel), p.textWidth(oeffentlichNum));
      const privatX = p.width / 2 - privatBlockWidth / 2;
      const oeffentlichX = p.width / 2 - oeffentlichBlockWidth / 2;
      p.text(privatNum, privatX, privatYNum);
      p.text(privatLabel, privatX, privatYLabel);
      p.text(oeffentlichNum, oeffentlichX, oeffentlichYNum);
      p.text(oeffentlichLabel, oeffentlichX, oeffentlichYLabelClamped);
    } else {
      p.textAlign(p.LEFT, p.CENTER);
      p.text('privat', p.width * 0.04, p.height * 0.65);
      p.text('öffentlich', p.width * 0.54, p.height * 0.65);
      p.text(formatNumber(visiblePrivat), p.width * 0.04, p.height * 0.54);
      p.text(formatNumber(visibleOeffentlich), p.width * 0.54, p.height * 0.54);
    }
    if (!fpsCheckDone) {
      fpsCheckFrame++;
      if (fpsCheckFrame === 120) {
        if (p.frameRate() < 40) p.frameRate(30);
        fpsCheckDone = true;
      }
    }
  };

  // Public API
  p.updateData = (rows) => applyData(rows);
  p.resizeTo = (w, h) => p.resizeCanvas(w, h);

  function applyData(rows) {
    selectedData = rows || [];
    visiblePrivat = 0;
    visibleOeffentlich = 0;
    particleQueue = [];
    particles = [];
    for (let i = 0; i < selectedData.length; i++) {
      for (let j = 0; j < (selectedData[i].ort_privat_total || 0); j++) {
        let px, py;
        if (props.isMobile) {
          px = p.random(crossSize, p.width - crossSize);
          py = p.random(crossSize, p.height / 2 - crossSize);
        } else {
          px = p.random(crossSize, p.width * 0.50 - crossSize);
          py = p.random(crossSize, p.height - crossSize);
        }
        particleQueue.push({ x: px, y: py, data: selectedData[i], ort: 'privat' });
      }
      for (let j = 0; j < (selectedData[i].ort_oeffentlich_total || 0); j++) {
        let px, py;
        if (props.isMobile) {
          px = p.random(crossSize, p.width - crossSize);
          py = p.random(p.height / 2 + crossSize, p.height - crossSize);
        } else {
          px = p.random(p.width * 0.50 + crossSize, p.width - crossSize);
          py = p.random(crossSize, p.height - crossSize);
        }
        particleQueue.push({ x: px, y: py, data: selectedData[i], ort: 'oeffentlich' });
      }
    }
    p.redraw();
  }

  class Particle {
    constructor(x, y, data, ort, p) {
      this.pos = p.createVector(x, y);
      this.home = p.createVector(x, y);
      this.r = crossSize;
      this.growing = true;
      this.initialDelay = 50 + Math.floor(p.random(20));
      this.data = data;
      this.ort = ort;
    }
    update(p, mouse) {
      if (this.growing) {
        if (this.initialDelay > 0) {
          this.initialDelay--;
          return;
        }
        this.growing = false;
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
      if (distToMouse < 150 && !props.isMobile) {
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
      if (props.isMobile) {
        if (this.ort === 'privat') {
          this.pos.x = p.constrain(this.pos.x, this.r, p.width - this.r);
          this.pos.y = p.constrain(this.pos.y, this.r, p.height / 2 - this.r);
        } else if (this.ort === 'oeffentlich') {
          this.pos.x = p.constrain(this.pos.x, this.r, p.width - this.r);
          this.pos.y = p.constrain(this.pos.y, p.height / 2 + this.r, p.height - this.r);
        }
      } else {
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

<!-- Kein scoped CSS, Styling kommt aus style.css -->