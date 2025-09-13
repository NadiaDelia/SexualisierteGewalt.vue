
      
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import * as d3 from 'd3'
import P5CanvasGeschaedigte from '../components/P5CanvasGeschaedigte.vue'
import P5CanvasBeschuldigte from '../components/P5CanvasBeschuldigte.vue'
import P5CanvasOrt from '../components/P5CanvasOrt.vue'
import P5CanvasBeziehung from '../components/P5CanvasBeziehung.vue'
import P5CanvasDunkelziffer from '../components/P5CanvasDunkelziffer.vue'
import P5CanvasTitelblatt from '../components/P5CanvasTitelblatt.vue'




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
const activeGeschaedigte = ref('sexuelle_noetigung')
const widthGeschaedigte = ref(Math.round(window.innerWidth * 0.6))
const heightGeschaedigte = ref(Math.round(window.innerHeight * 0.8))

window.addEventListener('resize', () => {
  widthGeschaedigte.value = Math.round(window.innerWidth * 0.6)
  heightGeschaedigte.value = Math.round(window.innerHeight * 0.8)
})

/** Sketch 2 Beschuldigte**/
const activeBeschuldigte = ref('sexuelle_noetigung')
const widthBeschuldigte = ref(Math.round(window.innerWidth * 0.6))
const heightBeschuldigte = ref(Math.round(window.innerHeight * 0.8))

window.addEventListener('resize', () => {
  widthBeschuldigte.value = Math.round(window.innerWidth * 0.6)
  heightBeschuldigte.value = Math.round(window.innerHeight * 0.8)
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

//** Für Titelblatt-Sketch**/
const widthTitelblatt = ref(window.innerWidth)
const heightTitelblatt = ref(window.innerHeight)

window.addEventListener('resize', () => {
  widthTitelblatt.value = window.innerWidth
  heightTitelblatt.value = window.innerHeight
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

//** Für Accordion-Liste **/
const openAccordions = ref({
  sexuellerUebergriff: false,
  vergewaltigung: false,
  missbrauch: false,
  sexuelleBelästigung: false,
  exhibitionismus: false
})

const toggleAccordion = (key) => {
  openAccordions.value[key] = !openAccordions.value[key]
}



// CSV laden
onMounted(async () => {
  const csv = await d3.csv(csvUrl, d3.autoType)
  raw.value = csv
})

// Filterdaten berechnen
//Geschaedigte
const filteredGeschaedigte = computed(() =>
  activeGeschaedigte.value ? raw.value.filter(d => d.straftat === activeGeschaedigte.value) : raw.value
)

//Beschuldigte
const filteredBeschuldigte = computed(() =>
  activeBeschuldigte.value ? raw.value.filter(d => d.straftat === activeBeschuldigte.value) : raw.value
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
  activeGeschaedigte.value = key
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
      <h1>Muster<br/>und blinde<br/>Flecken</h1>
      <h2>Was die Polizeiliche Kriminalstatistik 2024<br/>zu Sexualisierter Gewalt aufzeigt – und was nicht</h2>
      <div class="titelblatt-canvas-container">
        <P5CanvasTitelblatt
          :width="widthTitelblatt"
          :height="heightTitelblatt"
          :background="'transparent'"
          :font-family="'PxGroteskPan'"
        />
      </div>
    </div>
  </div>

  <!-- 1b. section PKS text: Erklärungstext als Overlay/Stacking -->
  <section class="text-overlay-section">
    <div class="text-overlay-content">
      <h2>Was ist die Polizeiliche Kriminalstatistik?</h2>
      <p>
    Die Polizei sammelt kontinuierlich Kennziffern zu registrierten Straftaten, auch zu Sexualisierter Gewalt. Sie werden jährlich in der Polizeilichen Kriminalstatistik der Schweiz veröffentlicht. Diese Zahlen sind wichtig: Sie zeigen Entwicklungen, Muster, Häufungen. Sie machen sichtbar, wer Gewalt ausübt, wer betroffen ist, wo Taten passieren und in welcher Beziehung Täter und Betroffene zueinander stehen. Gleichzeitig gilt: Zahlen zeichnen Muster – und lassen blinde Flecken.      
  </p>
  <h2 class="h2-spaced">Wir schauen genauer hin</h2>
      <p>
In fünf Visualisierungen betrachten wir zentrale Delikte Sexualisierter Gewalt. Dabei stützen wir uns auf die Daten der Kriminalstatistik, welche jeweils die angezeigten Fälle zählt. Zudem wichtig zu wissen: Die Statistik registriert nur zwei Geschlechter. Folgende Straftaten stehen im Zentrum: </p>
<p>
      <div class="accordion-list">
        <div class="accordion-item">
          <div class="accordion-header" @click="toggleAccordion('sexuellerUebergriff')">
            <span class="accordion-icon" :class="{ 'open': openAccordions.sexuellerUebergriff }">+</span>
            <span>Sexueller Übergriff und sexuelle Nötigung</span>
          </div>
          <div class="accordion-content" :class="{ 'open': openAccordions.sexuellerUebergriff }">
            <p>Sexueller Übergriff: Sexuelle Handlung gegen den Willen oder Ausnutzen eines Schockzustands.<br/>
                Sexuelle Nötigung: Zu sexueller Handlung zwingen (Drohung, Gewalt, psychischer Druck, Widerstandsunfähigkeit).</p>
          </div>
        </div>
        
        <div class="accordion-item">
          <div class="accordion-header" @click="toggleAccordion('vergewaltigung')">
            <span class="accordion-icon" :class="{ 'open': openAccordions.vergewaltigung }">+</span>
            <span>Vergewaltigung</span>
          </div>
          <div class="accordion-content" :class="{ 'open': openAccordions.vergewaltigung }">
            <p>Penetration gegen den Willen oder Ausnutzen eines Schockzustands (geschlechtsneutral).</p>
          </div>
        </div>
        
        <div class="accordion-item">
          <div class="accordion-header" @click="toggleAccordion('missbrauch')">
            <span class="accordion-icon" :class="{ 'open': openAccordions.missbrauch }">+</span>
            <span>Missbrauch einer urteilsunfähigen oder zum Widerstand unfähigen Person</span>
          </div>
          <div class="accordion-content" :class="{ 'open': openAccordions.missbrauch }">
            <p>Zustand der Unfähigkeit ausnutzen für sexuelle Handlungen (früher «Schändung»).</p>
          </div>
        </div>
        
        <div class="accordion-item">
          <div class="accordion-header" @click="toggleAccordion('sexuelleBelästigung')">
            <span class="accordion-icon" :class="{ 'open': openAccordions.sexuelleBelästigung }">+</span>
            <span>Sexuelle Belästigung</span>
          </div>
          <div class="accordion-content" :class="{ 'open': openAccordions.sexuelleBelästigung }">
            <p>Unerwartete sexuelle Handlung/Belästigung (tätlich, verbal, schriftlich, bildlich), auf Antrag.</p>
          </div>
        </div>
        
        <div class="accordion-item">
          <div class="accordion-header" @click="toggleAccordion('exhibitionismus')">
            <span class="accordion-icon" :class="{ 'open': openAccordions.exhibitionismus }">+</span>
            <span>Exhibitionismus</span>
          </div>
          <div class="accordion-content" :class="{ 'open': openAccordions.exhibitionismus }">
            <p>Exhibitionistische Handlung vor anderen, in der Regel auf Antrag.</p>
          </div>
        </div>
      </div>
      </p>
    </div>
  </section>

  <!-- 2. Split-Section: Sketch links sticky, rechts scrollt Text hoch -->
  <div class="split-section">
    <div class="split-left sticky-sketch">
      <h2>Wer ist von Sexualisierter Gewalt betroffen?</h2>
      <P5CanvasGeschaedigte
        :key="activeGeschaedigte + '-' + filteredGeschaedigte.length"
        :data="filteredGeschaedigte"
        :width="widthGeschaedigte"
        :height="heightGeschaedigte"
        :font-family="'PxGroteskPan'"
        :background="0"
      />
      <div class="btns">
        <button
          v-for="s in STRAFTATEN"
          :key="s.key"
          :class="{active: activeGeschaedigte === s.key}"
          @click="activeGeschaedigte = s.key"
        >{{ s.label }}</button>
      </div>
    </div>
    <div class="split-right">
  <div style="height: 150vh;"></div>
  <div class="side-text scrollable-text">
        <h2>Es trifft vor allem Frauen</h2>
        <p>
Die Visualisierung zeigt, wieviele Personen 2024 für die jeweiligen Straftaten Anzeige erstattet haben.
</p>
<p>
  Das Bild ist eindeutig: Frauen stellen bei allen Delikten die überwiegende Mehrheit der Betroffenen. Der Anteil liegt zwischen 84 Prozent (sexuelle Nötigung) und 98 Prozent (Vergewaltigung).       
 </p>
 <p>
Dieses Struktur ist seit Jahren stabil: Frauen machen konstant die deutliche Mehrheit der registrierten Betroffenen aus. Einziger Ausreisser und hier nicht dargestellt: Sexuelle Handlungen mit Kindern. Hier liegt der Anteil Jungen bei rund einem Viertel der Betroffenen. </p>  
      </div>
      <div style="height: 50vh;"></div>
    </div>
  </div>

  <!-- 3. Split Section: Sketch Beschuldigte sticky + Text (unverändert) -->
  <div class="split-section">
    <div class="split-left sticky-sketch">
      <h2>Wer übt Sexualisierte Gewalt aus?</h2>
      <P5CanvasBeschuldigte
        :key="activeBeschuldigte + '-' + filteredBeschuldigte.length"
        :data="filteredBeschuldigte"
        :width="widthBeschuldigte"
        :height="heightBeschuldigte"
        :background="0"
        :font-family="'PxGroteskPan'"
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
          :class="{active: activeBeschuldigte === s.key}"
          @click="activeBeschuldigte = s.key"
        >{{ s.label }}</button>
      </div>
    </div>
    <div class="split-right">
        <div style="height: 150vh;"></div>
      <div class="side-text scrollable-text">
        <h2>Nicht alle Männer aber fast immer ein Mann</h2>
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
          <h2>Wo findet Sexualisierte Gewalt statt?</h2>
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
          <div style="height: 150vh;"></div>
          <div class="side-text scrollable-text">
            <h2>Das Zuhause ist kein sicherer Ort.</h2>
            <p>
              
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

      <!-- 5. section beziehung: Sketch Beziehung sticky + Text -->
      <div class="split-section">
        <div class="split-left sticky-sketch">
          <h2>Wie ist die Beziehung zwischen Täter:in und Geschädigter?</h2>
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
          <div style="height: 150vh;"></div>
          <div class="side-text scrollable-text">
            <h2>Nur selten fremd.</h2>
            <p>
            
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

      <!-- 6. section dunkelziffer: Sketch Dunkelziffer fullscreen -->
      <div class="fullscreen-section">
        <div class="fullscreen-sketch">
          <h2 class="dunkelziffer-title">Angezeigte vs. tatsächliche Sexualisierte Gewalt</h2>
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
          <div style="height: 50vh;"></div>
        </div>
      </div>

      <!-- 7. section dunkelziffer text: Erklärungstext als Overlay/Stacking -->
      <section class="text-overlay-section">
        <div class="text-overlay-content">
          <h2>Der Grossteil bleibt unsichtbar.</h2>
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
  padding-top: 40px;
}

.fullscreen-section:first-of-type .fullscreen-sketch h1 {
  margin-bottom: 20px;
}

.fullscreen-section:first-of-type .fullscreen-sketch h2 {
  margin-top: 0;
}

.titelblatt-canvas-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -1;
  display: flex;
  align-items: center;
  justify-content: center;
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