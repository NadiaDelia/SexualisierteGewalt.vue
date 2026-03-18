<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import p5 from 'p5'

// Props-Interface: Definiert welche Daten von der Parent-Komponente übergeben werden können

const props = defineProps({
  data: { type: Array, default: () => [] },
  width: { type: Number, default: 800 },
  height: { type: Number, default: 600 },
  background: { type: [Number, Array, String], default: 0 },
  fontFamily: { type: String, default: 'PxGroteskPan' },
  isMobile: { type: Boolean, default: false },
  isSmallDesktop: { type: Boolean, default: false }
})

// Vue Template Ref: Verbindung zum DOM-Element für p5.js Canvas-Mounting

let mountRef = ref(null)
let p5Instance = null
let observer = null

// Responsive width/height logic
const getResponsiveWidth = () => {
  if (props.isMobile) {
    // 20px Margin links und rechts, nie breiter als 100vw-40px
    return Math.max(0, window.innerWidth - 40)
  }
  return props.width
}
const getResponsiveHeight = () => {
  if (props.isMobile) {
    return Math.max(320, Math.min(window.innerHeight * 0.7, 700)) // Min 320px, max 70vh oder 700px
  }
  return props.height
}

const sketch = (p) => {
  let particles = [];
  let particleQueue = [];
  let selectedData;
  let geschaedigteFrauen = 0;
  let geschaedigteMaenner = 0;
  let visibleFrauen = 0;
  let visibleMaenner = 0;

  // Responsive cross size
  let crossSize = props.isMobile ? 10 : (props.isSmallDesktop ? 12 : 14);
  let crossStrokeWeight = props.isMobile ? 4 : (props.isSmallDesktop ? 5 : 6);
  let fpsCheckDone = false;
  let fpsCheckFrame = 0;


  p.setup = () => {
    p.createCanvas(getResponsiveWidth(), getResponsiveHeight())
    p.frameRate(props.isMobile ? 30 : 60)
    applyData(props.data)
  }

  p.windowResized = () => {
    p.resizeCanvas(getResponsiveWidth(), getResponsiveHeight())
    applyData(props.data)
  }

  p.touchMoved = () => false

  p.draw = () => {
    p.background(props.background)
    if (props.fontFamily) p.textFont(props.fontFamily)
    // Dynamische Schriftgröße: Desktop und Mobile unterschiedlich
    const dynamicTextSize = props.isMobile
      ? Math.max(20, Math.min(p.width * 0.14, 90))
      : props.isSmallDesktop
        ? Math.max(18, Math.min(window.innerHeight * 0.08, 60))
        : Math.max(18, Math.min(p.width * 0.13, 90))
    p.textSize(dynamicTextSize)
    p.textAlign(p.LEFT, p.BOTTOM)
    p.fill(0)

    if (props.isMobile) {
      p.textAlign(p.CENTER, p.CENTER);
      const cx = p.width / 2;
      const half = p.height / 2;
      const frauenYNum = half * 0.4;
      const frauenYLabel = half * 0.6;
      const maennerYNum = half + half * 0.4;
      const maennerYLabel = half + half * 0.6;
      const maennerYLabelClamped = Math.min(maennerYLabel, p.height - dynamicTextSize * 0.5);
      const frauenNum = particleQueue.length > 0 ? formatNumber(visibleFrauen) : formatNumber(geschaedigteFrauen);
      const maennerNum = particleQueue.length > 0 ? formatNumber(visibleMaenner) : formatNumber(geschaedigteMaenner);
      p.text(frauenNum, cx, frauenYNum);
      p.text('Frauen', cx, frauenYLabel);
      p.text(maennerNum, cx, maennerYNum);
      p.text('Männer', cx, maennerYLabelClamped);
    } else {
      // Desktop: Block in Mitte der jeweiligen Canvas-Hälfte zentriert
      const frauenZahl = particleQueue.length > 0 ? formatNumber(visibleFrauen) : formatNumber(geschaedigteFrauen)
      const maennerZahl = particleQueue.length > 0 ? formatNumber(visibleMaenner) : formatNumber(geschaedigteMaenner)
      p.textSize(dynamicTextSize)
      const frauenBlockW = Math.max(p.textWidth(frauenZahl), p.textWidth('Frauen'))
      const maennerBlockW = Math.max(p.textWidth(maennerZahl), p.textWidth('Männer'))
      const frauenX = p.width / 4 - frauenBlockW / 2
      const maennerX = p.width * 3 / 4 - maennerBlockW / 2
      const lineGap = dynamicTextSize * 0.15
      const blockH = dynamicTextSize * 2 + lineGap
      const numY = p.height / 2 - blockH / 2 + dynamicTextSize / 2
      const labelY = numY + dynamicTextSize + lineGap
      p.textAlign(p.LEFT, p.CENTER)
      p.text('Frauen', frauenX, labelY)
      p.text('Männer', maennerX, labelY)
      p.text(frauenZahl, frauenX, numY)
      p.text(maennerZahl, maennerX, numY)
    }

    // Partikel animieren
    const mouseVec = p.createVector(p.mouseX, p.mouseY)
    for (let i = 0; i < particles.length; i++) {
      particles[i].update(p, mouseVec)
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
    if (!fpsCheckDone) {
      fpsCheckFrame++;
      if (fpsCheckFrame === 120) {
        if (p.frameRate() < 40) p.frameRate(30);
        fpsCheckDone = true;
      }
    }
  }

  // Public API für reactive Updates / Resize
  p.updateData = (rows) => applyData(rows)
  p.resizeTo = (w, h) => p.resizeCanvas(w, h)

  // updateParticlesForCurrentSelection > Name vereinfacht
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
      geschaedigteMaenner += Number(selectedData[i].geschaedigte_m) || 0;
      for (let j = 0; j < (Number(selectedData[i].geschaedigte_f) || 0); j++) {
        let px, py;
        if (props.isMobile) {
          px = p.random(crossSize, p.width - crossSize);
          py = p.random(crossSize, p.height / 2 - crossSize);
        } else {
          px = p.random(crossSize, p.width * 0.5 - crossSize);
          py = p.random(crossSize, p.height - crossSize);
        }
        particleQueue.push({ x: px, y: py, data: selectedData[i], gender: 'frau' });
      }
      for (let j = 0; j < (Number(selectedData[i].geschaedigte_m) || 0); j++) {
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
  }

  //1000er-Trennzeichen
  function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "’");
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
    update(p, mouse) {
      if (this.growing) {
        if (this.initialDelay > 0) {
          this.initialDelay--;
          return;
        }
      }
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
}




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
    :style="
      props.isMobile
        ? `display:block; width:calc(100vw - 40px); height:${getResponsiveHeight()}px; max-width:100vw; margin:0 auto;`
        : `display:block; width:${getResponsiveWidth()}px; height:${getResponsiveHeight()}px; max-width:100%; margin:0 auto;`
    "
  ></div>
</template>
