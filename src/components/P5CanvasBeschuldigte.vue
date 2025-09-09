<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import p5 from 'p5'

const props = defineProps({
  // CSV-Zeilen (gefiltert)
  data: { type: Array, default: () => [] },
  width: { type: Number, default: 800 },
  height: { type: Number, default: 600 },
  background: { type: [Number, Array, String], default: 0 },
  showLabels: { type: Boolean, default: true },

  // Spaltennamen – hier standardmäßig auf "beschuldigte_*"
  leftField:  { type: String, default: 'beschuldigte_f' },
  rightField: { type: String, default: 'beschuldigte_m' },

  // Labels
  leftLabel:  { type: String, default: 'Frauen' },
  rightLabel: { type: String, default: 'Männer' },

  // Physik-Parameter
  mouseRadius:   { type: Number, default: 150 },
  repelRadius:   { type: Number, default: 80 },
  attractPower:  { type: Number, default: 1.5 },
  fadeDelayMin:  { type: Number, default: 50 },
  fadeDelayJitter:{ type: Number, default: 20 },
})

const mountRef = ref(null)
let p5Instance = null

const sketch = (p) => {
  // --- Variablen aus deinem Sketch ---
  let particles = [];
  let particleQueue = [];
  let selectedData = [];
  let currentStraftat = null;
  let beschuldigteFrauen = 0;
  let beschuldigteMaenner = 0;
  let visibleFrauen = 0;
  let visibleMaenner = 0;
  const crossSize = 14;
  const crossStrokeWeight = 6;
  // Button-Referenzen
  let buttonRefs = {};

  // --- Setup ---
  p.setup = () => {
    p.createCanvas(props.width, props.height);
    p.frameRate(60);
    selectedData = props.data || [];
    createFilterButtons();
    updateParticlesForCurrentSelection();
  };

  // --- Draw ---
  p.draw = () => {
    p.background(props.background);
    p.textFont('PxGroteskPan');
    p.textSize(90);
    p.textAlign(p.LEFT, p.BOTTOM);
    p.fill(0);

    // Partikel zeichnen
    for (let i = 0; i < particles.length; i++) {
      particles[i].update(p);
      particles[i].display(p);
    }

    // Kreuze für Frauen und Männer gleichzeitig erscheinen lassen
    let frauenQueue = particleQueue.filter(pt => pt.gender === 'frau');
    let maennerQueue = particleQueue.filter(pt => pt.gender === 'mann');
    let addPerFrame = 5;
    for (let i = 0; i < addPerFrame; i++) {
      if (frauenQueue.length > 0) {
        let idx = particleQueue.findIndex(pt => pt.gender === 'frau');
        if (idx !== -1) {
          let pt = particleQueue.splice(idx, 1)[0];
          particles.push(new Particle(pt.x, pt.y, pt.data, pt.gender, p));
          visibleFrauen++;
        }
      }
      if (maennerQueue.length > 0) {
        let idx = particleQueue.findIndex(pt => pt.gender === 'mann');
        if (idx !== -1) {
          let pt = particleQueue.splice(idx, 1)[0];
          particles.push(new Particle(pt.x, pt.y, pt.data, pt.gender, p));
          visibleMaenner++;
        }
      }
    }

    // Labels
    p.text("Frauen", p.width * 0.04, p.height * 0.65);
    p.text("Männer", p.width * 0.54, p.height * 0.65);

    // Zahlen, wenn Animation fertig
    if (particleQueue.length > 0) {
      p.text(formatNumber(visibleFrauen), p.width * 0.04, p.height * 0.54);
      p.text(formatNumber(visibleMaenner), p.width * 0.54, p.height * 0.54);
    } else {
      p.text(formatNumber(beschuldigteFrauen), p.width * 0.04, p.height * 0.54);
      p.text(formatNumber(beschuldigteMaenner), p.width * 0.54, p.height * 0.54);
    }
  };

  // --- Filterbuttons erstellen ---
  function createFilterButtons() {
    // Buttons im DOM erzeugen, falls noch nicht vorhanden
    const buttonData = [
      { key: "sexuelle_noetigung", label: "Sexuelle Nötigung" },
      { key: "vergewaltigung", label: "Vergewaltigung" },
      { key: "missbrauch", label: "Sexueller Missbrauch" },
      { key: "belaestigung", label: "Sexuelle Belästigung" },
      { key: "exhibitionismus", label: "Exhibitionismus" }
    ];}
  //   // Buttons unterhalb des Canvas erzeugen
  //   const parent = p._userNode || p.canvas.parentNode;
  //   let btnContainer = parent.querySelector('.button-container');
  //   if (!btnContainer) {
  //     btnContainer = document.createElement('div');
  //     btnContainer.className = 'button-container';
  //     btnContainer.style.marginTop = '20px';
  //     btnContainer.style.display = 'flex';
  //     btnContainer.style.gap = '12px';
  //     parent.appendChild(btnContainer);
  //   }
  //   // Buttons erzeugen
  //   buttonRefs = {};
  //   btnContainer.innerHTML = '';
  //   buttonData.forEach((btn, i) => {
  //     const b = document.createElement('button');
  //     b.textContent = btn.label;
  // b.className = 'filter-btn'; // Styling jetzt über CSS
  //     b.onclick = () => {
  //       currentStraftat = btn.key;
  //       selectedData = (props.data || []).filter(d => d.straftat === btn.key);
  //       updateParticlesForCurrentSelection();
  //       updateButtonStyles();
  //     };
  //     btnContainer.appendChild(b);
  //     buttonRefs[btn.key] = b;
  //   });
  //   updateButtonStyles();
  // }

  // --- Partikel-Update ---
  function updateParticlesForCurrentSelection() {
    beschuldigteFrauen = 0;
    beschuldigteMaenner = 0;
    visibleFrauen = 0;
    visibleMaenner = 0;
    particleQueue = [];
    particles = [];
    for (let i = 0; i < selectedData.length; i++) {
      // Frauen links
      beschuldigteFrauen += selectedData[i].beschuldigte_f || 0;
      for (let j = 0; j < (selectedData[i].beschuldigte_f || 0); j++) {
        let px = p.random(crossSize, p.width * 0.50 - crossSize);
        let py = p.random(crossSize, p.height - crossSize);
        particleQueue.push({ x: px, y: py, data: selectedData[i], gender: 'frau' });
      }
      // Männer rechts
      beschuldigteMaenner += selectedData[i].beschuldigte_m || 0;
      for (let j = 0; j < (selectedData[i].beschuldigte_m || 0); j++) {
        let px = p.random(p.width * 0.50 + crossSize, p.width - crossSize);
        let py = p.random(crossSize, p.height - crossSize);
        particleQueue.push({ x: px, y: py, data: selectedData[i], gender: 'mann' });
      }
    }
    p.redraw();
  }

  // --- Button-Stile aktualisieren ---
  function updateButtonStyles() {
    Object.keys(buttonRefs).forEach(key => {
      buttonRefs[key].classList.remove('active');
      buttonRefs[key].style.background = '#fff';
      buttonRefs[key].style.color = '#222';
    });
    if (currentStraftat && buttonRefs[currentStraftat]) {
      buttonRefs[currentStraftat].classList.add('active');
      buttonRefs[currentStraftat].style.background = '#222';
      buttonRefs[currentStraftat].style.color = '#fff';
    }
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
    update(p) {
      if (this.growing) {
        if (this.initialDelay > 0) {
          this.initialDelay--;
          return;
        }
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
      // Grenzlogik für Frauen (linke Seite)
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

  // --- API für Vue ---
  p.updateData = (rows) => {
    selectedData = rows || [];
    updateParticlesForCurrentSelection();
  };
  p.resizeTo = (w, h) => p.resizeCanvas(w, h);
};



onMounted(() => {
  // Container leeren, falls noch alte Canvas vorhanden
  if (mountRef.value) {
    while (mountRef.value.firstChild) {
      mountRef.value.removeChild(mountRef.value.firstChild)
    }
  }
  // Nur erzeugen, wenn Daten vorhanden sind
  if (props.data && props.data.length > 0) {
    p5Instance = new p5(sketch, mountRef.value)
  }
})


onBeforeUnmount(() => {
  if (p5Instance) {
    p5Instance.remove()
    p5Instance = null
  }
  // Container leeren
  if (mountRef.value) {
    while (mountRef.value.firstChild) {
      mountRef.value.removeChild(mountRef.value.firstChild)
    }
  }
})



watch(() => props.data, (rows) => {
  // p5-Instanz nur erzeugen, wenn Daten vorhanden sind
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
