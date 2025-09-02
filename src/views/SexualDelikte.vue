<script setup>
import { ref, computed, onMounted } from 'vue'
import * as d3 from 'd3'
import P5CanvasGeschaedigte from '../components/P5CanvasGeschaedigte.vue'
import P5CanvasBeschuldigte from '../components/P5CanvasBeschuldigte.vue'


// Mapping wie in deinem alten Sketch
const STRAFTATEN = [
  { key: 'sexuelle_noetigung', label: 'Sexuelle Nötigung' },
  { key: 'vergewaltigung',     label: 'Vergewaltigung' },
  { key: 'missbrauch',         label: 'Sexueller Missbrauch' },
  { key: 'belaestigung',       label: 'Sexuelle Belästigung' },
  { key: 'exhibitionismus',    label: 'Exhibitionismus' },
]

// CSV- & Font-Dateien (liegen in src/assets/)
const csvUrl  = new URL('../assets/data_sg.csv', import.meta.url).href
// Direkt-URL aus dem public-Ordner:
const fontUrl = '/Px-Grotesk-Pan-Bold.otf'

// const fontUrl = null // keine Schrift importieren

/** Sketch 1 Geschaedigte **/
const raw = ref([])
const active = ref('sexuelle_noetigung')
const width = ref(Math.round(window.innerWidth * 0.6))
const height = ref(Math.round(window.innerHeight * 0.8))

window.addEventListener('resize', () => {
  width.value = Math.round(window.innerWidth * 0.6)
  height.value = Math.round(window.innerHeight * 0.8)
})

/** Sketch 2 Beschuldigte**/
const active2 = ref('sexuelle_noetigung')
const width2 = ref(Math.round(window.innerWidth * 0.6))
const height2 = ref(Math.round(window.innerHeight * 0.8))

window.addEventListener('resize', () => {
  width2.value = Math.round(window.innerWidth * 0.6)
  height2.value = Math.round(window.innerHeight * 0.8)
})

// CSV laden
onMounted(async () => {
  const csv = await d3.csv(csvUrl, d3.autoType)
  raw.value = csv
})

// Filterdaten berechnen
const filtered = computed(() =>
  active.value ? raw.value.filter(d => d.straftat === active.value) : raw.value
)

const filtered2 = computed(() =>
  active2.value ? raw.value.filter(d => d.straftat === active2.value) : raw.value
)


// Filter setzen
function setFilter(key) {
  active.value = key
}

// Text erscheint erst, wenn Sketch nicht mehr sichtbar ist
import { onUnmounted, nextTick } from 'vue'
const showText = ref(false)
let observer = null
onMounted(async () => {
  await nextTick()
  const sketchEl = document.getElementById('sketch-section')
  if (sketchEl) {
    observer = new window.IntersectionObserver((entries) => {
      if (!entries[0].isIntersecting) {
        showText.value = true
      } else {
        showText.value = false
      }
    }, { threshold: 0 })
    observer.observe(sketchEl)
  }
})
onUnmounted(() => {
  if (observer) observer.disconnect()
})
</script>

<template>
<div class="main-scroll">
  <!-- 1. Titelbild -->
  <section>
    <h1>Wer verübt<br/>sexualisierte<br/>Gewalt und<br/>wer ist betroffen?</h1>
  </section>

  <!-- 2. Split-Section: Sketch links sticky, rechts scrollt Text hoch -->
  <div class="split-section">
    <div class="split-left sticky-sketch">
      <h2>Geschädigte Sexualisierter Gewalt 2024</h2>
      <P5CanvasGeschaedigte
        :key="active + '-' + filtered.length"
        :data="filtered"
        :width="width"
        :height="height"
        :font-url="fontUrl"
        :background="0"
      />
      <div class="btns">
        <button
          v-for="s in STRAFTATEN"
          :key="s.key"
          :class="{active: active === s.key}"
          @click="active = s.key"
        >{{ s.label }}</button>
      </div>
    </div>
    <div class="split-right">
  <div style="height: 150vh;"></div>
  <div class="side-text scrollable-text">
        <h3>Wer sind die Betroffenen?</h3>
        <p>
          Sexualisierte Gewalt betrifft Menschen unterschiedlichster Herkunft, Altersgruppen und Geschlechter. Die Zahlen zeigen, dass ...
        </p>
        <p>
          Weitere Informationen, Statistiken und persönliche Geschichten können hier platziert werden.
        </p>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, urna eu tincidunt consectetur, nisi nisl aliquam nunc, eget aliquam nisl nunc euismod nunc. Duis euismod, nisl eu aliquam tincidunt, nunc nisl aliquam nunc, eget aliquam nisl nunc euismod nunc.
        </p>
        <p>
          Noch mehr Beispieltext, damit gescrollt werden kann. Füge hier beliebig viel Content ein.
        </p>
      </div>
      <div style="height: 50vh;"></div>
    </div>
  </div>

  <!-- Split: Sketch Beschuldigte sticky + Text (unverändert) -->
  <div class="split-section">
    <div class="split-left sticky-sketch">
      <h2>Beschuldigte Sexualisierter Gewalt 2024</h2>
      <P5CanvasBeschuldigte
        :key="active2 + '-' + filtered2.length"
        :data="filtered2"
        :width="width2"
        :height="height2"
        :background="0"
        :show-labels="true"
        left-field="beschuldigte_f"
        right-field="beschuldigte_m"
        left-label="Frauen"
        right-label="Männer"
        :mouse-radius="150"
        :repel-radius="80"
        :attract-power="1.5"
      />
      <div class="btns">
        <button
          v-for="s in STRAFTATEN"
          :key="s.key"
          :class="{active2: active2 === s.key}"
          @click="active2 = s.key"
        >{{ s.label }}</button>
      </div>
    </div>
    <div class="split-right">
      <div class="side-text scrollable-text">
        <h3>Wer sind die Beschuldigten?</h3>
        <p>
          Die Beschuldigten sexualisierter Gewalt sind überwiegend männlich, aber auch Frauen sind betroffen. Die Statistiken zeigen ...
        </p>
        <p>
          Weitere Analysen und Hintergrundinformationen können hier ergänzt werden.
        </p>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, urna eu tincidunt consectetur, nisi nisl aliquam nunc, eget aliquam nisl nunc euismod nunc. Duis euismod, nisl eu aliquam tincidunt, nunc nisl aliquam nunc, eget aliquam nisl nunc euismod nunc.
        </p>
        <p>
          Noch mehr Beispieltext, damit gescrollt werden kann. Füge hier beliebig viel Content ein.
        </p>
      </div>
    </div>
  </div>
</div>
</template>

<style scoped>
/* Scrollbarer Text rechts neben sticky Sketch */
.scrollable-text {
  height: auto;
  min-height: 100vh;
  overflow-y: visible;
  position: sticky;
  top: 30px;
}
button {
  transition: 0.2s;
}
button:hover {
  transform: translateY(0px);
}
/* Sticky Header */
/* Snap Scrolling */
.main-scroll {
  scroll-snap-type: y mandatory;
  overflow-y: auto;
  height: 100vh;
  background: #000;
}
.main-scroll > section,
.split-section {
  scroll-snap-align: start;
  min-height: 150vh;
}
section {
  display: flex;
  flex-direction: column;
  justify-content: left;
  align-items: left;
  margin: 0 0 0 60px;
  background: #000;
}
.btns {
  margin-top: 24px;
  display: flex; 
  flex-wrap: wrap;
  gap: 8px;
}
.btns button {
  border: 2px solid #000;
  background: #000;
  color: #fff;
  padding: 8px 16px;
  cursor: pointer;
  transition: background .2s, border-color .2s;
}
.btns button.active {
  border: 2px solid #fff;
  background: #000;
  color: #fff;
}
.btns button:hover {
  background: #000;
  border: 2px solid #fff;
}
.overlay-text {
  position: absolute;
  top: 30px;
  left: 30px;
  right: 30px;
  background: #000;
  color: #fff;
  padding: 24px;
  opacity: 0.95;
  z-index: 2;
  font-size: 1.2em;
  border: 2px solid #fff;
  pointer-events: none;
}
.split-section {
  min-height: 100vh;
  display: flex;
  flex-direction: row;
  align-items: stretch;
  scroll-snap-align: start;
  background: #000;
}
.split-left {
  flex: 1 1 60%;
  display: flex;
  flex-direction: column;
  align-items: left;
  justify-content: left;
  background: #000;
  margin-left: 60px;
}

.sticky-sketch {
  position: sticky;
  top: 0;
  height: 100vh;
  z-index: 1;
  background: #000;
  display: flex;
  flex-direction: column;
  align-items: left;
  justify-content: left;
  margin-left: 60px;
}

.side-text {
  margin: auto 0;
  padding: 3em;
  color: #fff;
  max-width: 600px;
}
.split-right {
  flex: 1 1 40%;
  display: flex;
  flex-direction: column;
  justify-content: left;
  background: #000;
  color: #fff;
  padding: 3em;
  /* Keine Linie mehr */
  position: relative;
}

/* Fade-In Transition */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.8s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
