
      
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import * as d3 from 'd3'
import P5CanvasGeschaedigte from '../components/P5CanvasGeschaedigte.vue'
import P5CanvasBeschuldigte from '../components/P5CanvasBeschuldigte.vue'
import P5CanvasOrt from '../components/P5CanvasOrt.vue'
import P5CanvasBeziehung from '../components/P5CanvasBeziehung.vue'
import P5CanvasDunkelziffer from '../components/P5CanvasDunkelziffer.vue'




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


//** Für Ort-Sketch**/
const activeOrt = ref('sexuelle_noetigung')
const genderOrt = ref('frau')
const widthOrt = ref(Math.round(window.innerWidth * 0.6))
const heightOrt = ref(Math.round(window.innerHeight * 0.8))

window.addEventListener('resize', () => {
  widthOrt.value = Math.round(window.innerWidth * 0.6)
  heightOrt.value = Math.round(window.innerHeight * 0.8)
})

//** Für Beziehung-Sketch**/
const activeBeziehung = ref('sexuelle_noetigung')
const widthBeziehung = ref(Math.round(window.innerWidth * 0.6))
const heightBeziehung = ref(Math.round(window.innerHeight * 0.8))

window.addEventListener('resize', () => {
  widthBeziehung.value = Math.round(window.innerWidth * 0.6)
  heightBeziehung.value = Math.round(window.innerHeight * 0.8)
})

//** Für Dunkelziffer-Sketch**/
const activeDunkelziffer = ref('sexuelle_noetigung')
const dunkelzifferMode = ref('hell') // 'hell' oder 'dunkel'
const widthDunkelziffer = ref(window.innerWidth)
const heightDunkelziffer = ref(window.innerHeight)

window.addEventListener('resize', () => {
  widthDunkelziffer.value = window.innerWidth
  heightDunkelziffer.value = window.innerHeight
})



// CSV laden
onMounted(async () => {
  const csv = await d3.csv(csvUrl, d3.autoType)
  raw.value = csv
})

// Filterdaten berechnen
//Geschaedigte
const filtered = computed(() =>
  active.value ? raw.value.filter(d => d.straftat === active.value) : raw.value
)

//Beschuldigte
const filtered2 = computed(() =>
  active2.value ? raw.value.filter(d => d.straftat === active2.value) : raw.value
)

//Ort
const filteredOrt = computed(() =>
  activeOrt.value ? raw.value.filter(d => d.straftat === activeOrt.value) : raw.value
)

//Beziehung
const filteredBeziehung = computed(() =>
  activeBeziehung.value ? raw.value.filter(d => d.straftat === activeBeziehung.value) : raw.value
)

//Dunkelziffer
const filteredDunkelziffer = computed(() =>
  activeDunkelziffer.value ? raw.value.filter(d => d.straftat === activeDunkelziffer.value) : raw.value
)

// Debug: Überwache Änderungen
watch(activeOrt, (newVal) => {
  console.log('activeOrt changed:', newVal)
})
watch(genderOrt, (newVal) => {
  console.log('genderOrt changed:', newVal)
})

console.log('filteredOrt', filteredOrt.value)
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
  <!-- 1a. Titelbild -->
  <div class="fullscreen-section">
    <div class="fullscreen-sketch">
      <h1>Wer verübt<br/>sexualisierte<br/>Gewalt und<br/>wer ist betroffen?</h1>
    </div>
  </div>

  <!-- 1b. section PKS text: Erklärungstext als Overlay/Stacking -->
  <section class="text-overlay-section">
    <div class="text-overlay-content">
      <h3>Was ist die Polizeiliche Kriminalstatistik?</h3>
      <p>
        Die Polizeiliche Kriminalstatistik (PKS) ist eine jährliche Erhebung der Polizei, die Informationen über Straftaten und deren Aufklärung liefert. Sie bildet die Grundlage für die Analyse von Kriminalität in Deutschland.
      </p>
      <p>
        Die PKS erfasst jedoch nur die Fälle, die der Polizei bekannt werden. Die Dunkelziffer, also die nicht erfassten Fälle, bleibt unberücksichtigt.
      </p>
      <p>
        Studien zeigen, dass nur ein Bruchteil der tatsächlichen Fälle sexualisierter Gewalt offiziell erfasst wird. Dies macht die Bekämpfung dieser Verbrechen besonders schwierig.
      </p>
      <p>
        Weitere Analysen und Hintergrundinformationen können hier ergänzt werden.
      </p>
    </div>
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

  <!-- 3. Split Section: Sketch Beschuldigte sticky + Text (unverändert) -->
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
          :class="{active: active2 === s.key}"
          @click="active2 = s.key"
        >{{ s.label }}</button>
      </div>
    </div>
    <div class="split-right">
        <div style="height: 150vh;"></div>
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
      <div style="height: 50vh;"></div>
    </div>
  </div>

      <!-- 4. section ort: Sketch Ort sticky + Text -->
      <div class="split-section">
        <div class="split-left sticky-sketch">
          <h2>Ort der Tat 2024</h2>
          <P5CanvasOrt
            :key="activeOrt + '-' + genderOrt + '-' + filteredOrt.length"
            :data="filteredOrt"
            :width="widthOrt"
            :height="heightOrt"
            :background="0"
            :font-family="'PxGroteskPan'"
            :gender="genderOrt"
          />
          <div class="btns">
            <div class="filter-buttons">
              <button
                v-for="s in STRAFTATEN"
                :key="s.key"
                :class="{active: activeOrt === s.key}"
                @click="activeOrt = s.key"
              >{{ s.label }}</button>
            </div>
            <div class="gender-toggle-container">
              <button
                :class="['toggle-btn', { 'active-gender': genderOrt === 'frau' }]"
                @click="genderOrt = 'frau'"
              >F</button>
              <button
                :class="['toggle-btn', { 'active-gender': genderOrt === 'mann' }]"
                @click="genderOrt = 'mann'"
              >M</button>
            </div>
          </div>
        </div>
        <div class="split-right">
          <div class="side-text scrollable-text">
            <h3>Wo finden die Taten statt?</h3>
            <p>
              Die Orte der Taten sind unterschiedlich verteilt. Privat und öffentlich werden hier gegenübergestellt.
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

      <!-- 5. section beziehung: Sketch Beziehung sticky + Text -->
      <div class="split-section">
        <div class="split-left sticky-sketch">
          <h2>Beziehung zwischen Täter:in und Geschädigter 2024</h2>
          <P5CanvasBeziehung
            :key="activeBeziehung + '-' + filteredBeziehung.length"
            :data="filteredBeziehung"
            :width="widthBeziehung"
            :height="heightBeziehung"
            :background="0"
            :font-family="'PxGroteskPan'"
            :mouse-radius="150"
            :repel-radius="80"
            :attract-power="1.5"
          />
          <div class="btns">
            <button
              v-for="s in STRAFTATEN"
              :key="s.key"
              :class="{active: activeBeziehung === s.key}"
              @click="activeBeziehung = s.key"
            >{{ s.label }}</button>
          </div>
        </div>
        <div class="split-right">
          <div class="side-text scrollable-text">
            <h3>Wie ist die Beziehung zwischen Täter:in und Geschädigter?</h3>
            <p>
              Die Beziehung zwischen Täter:in und geschädigter Person variiert stark je nach Art der Straftat. Partner, verwandte Personen, Bekannte, Arbeitskolleg:innen oder völlig fremde Personen können Täter:innen sein.
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

      <!-- 6. section dunkelziffer: Sketch Dunkelziffer fullscreen -->
      <div class="fullscreen-section">
        <div class="fullscreen-sketch">
          <h2 class="dunkelziffer-title">Dunkelziffer - Angezeigt vs. Tatsächlich 2024</h2>
          <div class="dunkelziffer-canvas-container">
            <P5CanvasDunkelziffer
              :key="activeDunkelziffer + '-' + dunkelzifferMode + '-' + filteredDunkelziffer.length"
              :data="filteredDunkelziffer"
              :width="widthDunkelziffer"
              :height="heightDunkelziffer"
              :background="'transparent'"
              :font-family="'PxGroteskPan'"
              :dunkelziffer="dunkelzifferMode"
              :mouse-radius="80"
              :repel-radius="100"
              :attract-power="10"
            />
          </div>
          <div class="btns fullscreen-buttons">
            <div class="filter-buttons">
              <button
                v-for="s in STRAFTATEN"
                :key="s.key"
                :class="{active: activeDunkelziffer === s.key}"
                @click="activeDunkelziffer = s.key"
              >{{ s.label }}</button>
            </div>
            <div class="dunkelziffer-toggle-container">
              <button
                :class="['toggle-btn', { 'active-dunkelziffer': dunkelzifferMode === 'hell' }]"
                @click="dunkelzifferMode = 'hell'"
              >Angezeigt</button>
              <button
                :class="['toggle-btn', { 'active-dunkelziffer': dunkelzifferMode === 'dunkel' }]"
                @click="dunkelzifferMode = 'dunkel'"
              >Tatsächlich</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 7. section dunkelziffer text: Erklärungstext als Overlay/Stacking -->
      <section class="text-overlay-section">
        <div class="text-overlay-content">
          <h3>Was ist die Dunkelziffer?</h3>
          <p>
            Die Dunkelziffer zeigt den Unterschied zwischen angezeigten und tatsächlichen Fällen sexualisierter Gewalt. Viele Fälle werden nie bei der Polizei gemeldet.
          </p>
          <p>
            Die Gründe dafür sind vielfältig: Scham, Angst vor den Folgen, mangelndes Vertrauen in das Justizsystem oder die Nähe zum Täter.
          </p>
          <p>
            Studien zeigen, dass nur ein Bruchteil der tatsächlichen Fälle sexualisierter Gewalt offiziell erfasst wird. Dies macht die Bekämpfung dieser Verbrechen besonders schwierig.
          </p>
          <p>
            Weitere Analysen und Hintergrundinformationen können hier ergänzt werden.
          </p>
        </div>
      </section>
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

/* Sticky Header */
/* Snap Scrolling */
.main-scroll {
  scroll-snap-type: y mandatory;
  overflow-y: auto;
  height: 100vh;
  background: #000;
}
.main-scroll > section,
.split-section,
.fullscreen-section {
  scroll-snap-align: start;
  min-height: 150vh;
}

/* Erste Section - gleiche Struktur wie Dunkelziffer */
.fullscreen-section:first-of-type {
  min-height: 200vh !important;
}

.fullscreen-section:first-of-type .fullscreen-sketch {
  justify-content: flex-start;
  align-items: flex-start;
  padding-left: 60px;
  padding-top: 100px;
}

section {
  display: flex;
  flex-direction: column;
  justify-content: left;
  align-items: left;
  margin: 0;
  background: #000;
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

/* Fullscreen Dunkelziffer Section */
.fullscreen-section {
  min-height: 200vh !important;
  position: relative;
  scroll-snap-align: start;
  z-index: 1;
}

.fullscreen-sketch {
  width: 100vw !important;
  height: 100vh !important;
  margin: 0 !important;
  padding: 0;
  box-sizing: border-box;
  position: sticky;
  top: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.dunkelziffer-title {
  position: absolute;
  top: 40px;
  left: 50%;
  transform: translateX(-68%);
  z-index: 1;
  color: #fff;
  text-align: left;
  margin: 0;
  pointer-events: none;
}

.dunkelziffer-canvas-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
}

.fullscreen-buttons {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
  align-items: center;
  z-index: 10;
}

.dunkelziffer-toggle-container {
  display: flex;
  gap: 5px;
  margin-left: 20px;
}

.active-dunkelziffer {
  background-color: #fff !important;
  color: #000 !important;
}

/* Text Overlay Section - scrollt über Dunkelziffer */
.text-overlay-section {
  min-height: 100vh;
  background: #000;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  scroll-snap-align: start;
  margin: 0;
  position: relative;
  z-index: 3;
  margin-top: -100vh;
}

.text-overlay-content {
  max-width: 800px;
  padding: 60px;
  text-align: left;
}
</style>