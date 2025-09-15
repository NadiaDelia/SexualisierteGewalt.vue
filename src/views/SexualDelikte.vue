<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
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
  { key: 'vergewaltigung', label: 'Vergewaltigung' },
  { key: 'missbrauch', label: 'Sexueller Missbrauch' },
  { key: 'belaestigung', label: 'Sexuelle Belästigung' },
  { key: 'exhibitionismus', label: 'Exhibitionismus' },
]

// CSV- & Font-Dateien (liegen in src/assets/)
const csvUrl = new URL('../assets/data_sg.csv', import.meta.url).href
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

  // Intersection Observer für Auto-Reset
  setupIntersectionObservers()
})

// Intersection Observer Logik - Reset auf 'sexuelle_noetigung' wenn Sketch aus Viewport verschwindet
let intersectionObserver = null

const setupIntersectionObservers = () => {
  intersectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      // Wenn Element den Viewport verlässt (nicht mehr sichtbar)
      if (!entry.isIntersecting) {
        const id = entry.target.id
        resetSketchToDefault(id)
      }
    })
  }, {
    threshold: 0.05, // Element gilt als "nicht sichtbar" wenn weniger als 10% sichtbar sind
    rootMargin: '-50px' // Zusätzlicher Puffer
  })

  // Beobachte alle Sketch-Container
  // Diese IDs müssen im Template gesetzt werden
  const sketchIds = [
    'sketch-geschaedigte',
    'sketch-beschuldigte',
    'sketch-ort',
    'sketch-beziehung',
    'sketch-dunkelziffer'
  ]

  sketchIds.forEach(id => {
    const element = document.getElementById(id)
    if (element) {
      intersectionObserver.observe(element)
    }
  })
}

const resetSketchToDefault = (sketchId) => {
  console.log(`Resetting ${sketchId} to default`)

  switch (sketchId) {
    case 'sketch-geschaedigte':
      activeGeschaedigte.value = 'sexuelle_noetigung'
      break
    case 'sketch-beschuldigte':
      activeBeschuldigte.value = 'sexuelle_noetigung'
      break
    case 'sketch-ort':
      activeOrt.value = 'sexuelle_noetigung'
      genderOrt.value = 'frau' // Optional: auch Gender zurücksetzen
      break
    case 'sketch-beziehung':
      activeBeziehung.value = 'sexuelle_noetigung'
      break
    case 'sketch-dunkelziffer':
      activeDunkelziffer.value = 'sexuelle_noetigung'
      dunkelzifferMode.value = 'hell' // Optional: auch Modus zurücksetzen
      break
  }
}

onBeforeUnmount(() => {
  if (intersectionObserver) {
    intersectionObserver.disconnect()
  }
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

// Reset Dunkelziffer-Toggle auf "Angezeigt" wenn Straftat geändert wird
watch(activeDunkelziffer, (newVal) => {
  console.log('activeDunkelziffer changed:', newVal)
  dunkelzifferMode.value = 'hell'
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
        <h1>Muster<br />und blinde<br />Flecken</h1>
        <h2>Was die Polizeiliche Kriminalstatistik 2024<br />zu Sexualisierter Gewalt aufzeigt – und was nicht</h2>
        <div class="titelblatt-canvas-container">
          <P5CanvasTitelblatt :width="widthTitelblatt" :height="heightTitelblatt" :background="'transparent'"
            :font-family="'PxGroteskPan'" />
        </div>
      </div>
    </div>

    <!-- 1b. section PKS text: Erklärungstext als Overlay/Stacking -->
    <section class="text-overlay-section">
      <div class="text-overlay-content">
        <h2>Was ist die Polizeiliche Kriminalstatistik?</h2>
        <p>
          Die Polizei sammelt kontinuierlich Kennziffern zu registrierten Straftaten, auch zu Sexualisierter Gewalt. Sie
          werden jährlich in der Polizeilichen Kriminalstatistik der Schweiz veröffentlicht. Diese Zahlen sind wichtig:
          Sie zeigen Entwicklungen, Muster, Häufungen. Sie machen sichtbar, wer Gewalt ausübt, wer betroffen ist, wo
          Taten passieren und in welcher Beziehung Täter und Betroffene zueinander stehen. Gleichzeitig gilt: Zahlen
          zeichnen Muster – und lassen blinde Flecken.
        </p>
        <h2 class="h2-spaced">Wir schauen genauer hin</h2>
        <p>
          In fünf Visualisierungen betrachten wir zentrale Delikte Sexualisierter Gewalt. Dabei stützen wir uns auf die
          Daten der Kriminalstatistik, welche jeweils die angezeigten Fälle zählt. Zudem wichtig zu wissen: Die
          Statistik registriert nur zwei Geschlechter. Folgende Straftaten stehen im Zentrum: </p>
        <p>
        <div class="accordion-list">
          <div class="accordion-item">
            <div class="accordion-header" @click="toggleAccordion('sexuellerUebergriff')">
              <span class="accordion-icon" :class="{ 'open': openAccordions.sexuellerUebergriff }">+</span>
              <span>Sexueller Übergriff und sexuelle Nötigung</span>
            </div>
            <div class="accordion-content" :class="{ 'open': openAccordions.sexuellerUebergriff }">
              <p>Sexueller Übergriff: Sexuelle Handlung gegen den Willen oder Ausnutzen eines Schockzustands.<br />
                Sexuelle Nötigung: Zu sexueller Handlung zwingen (Drohung, Gewalt, psychischer Druck,
                Widerstandsunfähigkeit).</p>
            </div>
          </div>

          <div class="accordion-item">
            <div class="accordion-header" @click="toggleAccordion('vergewaltigung')">
              <span class="accordion-icon" :class="{ 'open': openAccordions.vergewaltigung }">+</span>
              <span>Vergewaltigung</span>
            </div>
            <div class="accordion-content" :class="{ 'open': openAccordions.vergewaltigung }">
              <p>Penetration gegen den Willen oder durch das Ausnutzen eines Schockzustands (geschlechtsneutral).</p>
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
      <div id="sketch-geschaedigte" class="split-left sticky-sketch">
        <h2>Wer ist von Sexualisierter Gewalt betroffen?</h2>
        <p class="annotation">Ein Kreuz entspricht einer geschädigten Person</p>
        <P5CanvasGeschaedigte :key="activeGeschaedigte + '-' + filteredGeschaedigte.length" :data="filteredGeschaedigte"
          :width="widthGeschaedigte" :height="heightGeschaedigte" :font-family="'PxGroteskPan'" :background="0" />
        <div class="btns">
          <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeGeschaedigte === s.key }"
            @click="activeGeschaedigte = s.key">{{ s.label }}</button>
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
            Frauen stellen bei allen Delikten die überwiegende Mehrheit der Betroffenen. Der Anteil liegt zwischen 84
            Prozent (sexuelle Nötigung) und 98 Prozent (Vergewaltigung).
          </p>
          <p>
            Dieses Struktur ist seit Jahren stabil: Frauen machen konstant die deutliche Mehrheit der Betroffenen aus.
            Einziger Ausreisser und hier nicht dargestellt: Sexuelle Handlungen mit Kindern. Hier liegt der Anteil
            Jungen bei rund einem Viertel der Betroffenen. </p>
        </div>
        <div style="height: 50vh;"></div>
      </div>
    </div>

    <!-- 3. Split Section: Sketch Beschuldigte sticky + Text (unverändert) -->
    <div class="split-section">
      <div class="split-left sticky-sketch" id="sketch-beschuldigte">
        <h2>Wer übt Sexualisierte Gewalt aus?</h2>
        <p class="annotation">Ein Kreuz entspricht einer beschuldigten Person</p>
        <P5CanvasBeschuldigte :key="activeBeschuldigte + '-' + filteredBeschuldigte.length" :data="filteredBeschuldigte"
          :width="widthBeschuldigte" :height="heightBeschuldigte" :background="0" :font-family="'PxGroteskPan'"
          :show-labels="true" left-field="beschuldigte_f" right-field="beschuldigte_m" left-label="Frauen"
          right-label="Männer" :mouse-radius="150" :repel-radius="80" :attract-power="1.5" />
        <div class="btns">
          <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeBeschuldigte === s.key }"
            @click="activeBeschuldigte = s.key">{{ s.label }}</button>
        </div>
      </div>
      <div class="split-right">
        <div style="height: 150vh;"></div>
        <div class="side-text scrollable-text">
          <h2>Nicht alle Männer aber fast immer ein Mann</h2>
          <p>
            Die Darstellung weist das Geschlecht der beschuldigten Personen für die einzelnen Straftaten aus. Das
            Verhältnis ist noch eindeutiger als bei den Betroffenen Sexualisierter Gewalt. Zwischen 96 Prozent (sexuelle
            Nötigung) und annähernd 100 Prozent (Vergewaltigung) der Beschuldigten sind Männer.
          </p>
          <p>
            Wichtig zu wissen: Vor der Sexualstrafrechtsreform kannte der Straftatbestand Vergewaltigung ausschliesslich
            weibliche Betroffene und männliche Täter. Seit 1. Juli 2024 ist das Gesetz geschlechtsneutral definiert.
            Vergewaltigung umfasst jegliche Penetration gegen den Willen der betroffenen Person oder durch das Ausnutzen
            eines Schockzustands.
          </p>
        </div>
        <div style="height: 50vh;"></div>
      </div>
    </div>

    <!-- 4. section ort: Sketch Ort sticky + Text -->
    <div class="split-section">
      <div class="split-left sticky-sketch" id="sketch-ort">
        <h2>Wo findet Sexualisierte Gewalt statt?</h2>
        <p class="annotation">Ein Kreuz entspricht einer Straftat</p>
        <P5CanvasOrt :key="activeOrt + '-' + genderOrt + '-' + filteredOrt.length" :data="filteredOrt" :width="widthOrt"
          :height="heightOrt" :background="0" :font-family="'PxGroteskPan'" :gender="genderOrt" />
        <div class="btns">
          <div class="filter-buttons">
            <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeOrt === s.key }"
              @click="activeOrt = s.key">{{ s.label }}</button>
          </div>
          <div class="gender-toggle-container">
            <button :class="['toggle-btn', { 'active-gender': genderOrt === 'frau' }]"
              @click="genderOrt = 'frau'">F</button>
            <button :class="['toggle-btn', { 'active-gender': genderOrt === 'mann' }]"
              @click="genderOrt = 'mann'">M</button>
          </div>
        </div>
      </div>
      <div class="split-right">
        <div style="height: 150vh;"></div>
        <div class="side-text scrollable-text">
          <h2>Das Zuhause ist kein sicherer Ort.</h2>
          <p>
            Die Taten Sexualisierter Gewalt finden überwiegend im privaten Umfeld statt. Ausgenommen sind sexuelle
            Belästigung und Exhibitionismus. Unter privatem Raum werden ausschliesslich die «eigenen vier Wände»
            verstanden. Ein Raum gilt als öffentlich, wenn er grundsätzlich für verschiedenste Personen zugänglich ist
            (beispielsweise auch das Treppenhaus oder die gemeinsame Waschküche eines Mehrfamilienhauses).
          </p>
          <p>
            Sexuelle Nötigung, Vergewaltigung und sexuelle Übergriffe finden überwiegend im privaten Umfeld statt. Das
            steht im Widerspruch zu verbreiteten Vergewaltigungsmythen, die den Täter als fremden Mann im Dunkeln
            zeichnen.
          </p>
        </div>
        <div style="height: 50vh;"></div>
      </div>
    </div>

    <!-- 5. section beziehung: Sketch Beziehung sticky + Text -->
    <div class="split-section">
      <div class="split-left sticky-sketch" id="sketch-beziehung">
        <h2>Welche Beziehung haben Beschuldigte und Geschädigte?</h2>
        <p class="annotation">Ein Kreuz entspricht einer geschädigten Person</p>
        <P5CanvasBeziehung :key="activeBeziehung + '-' + filteredBeziehung.length" :data="filteredBeziehung"
          :width="widthBeziehung" :height="heightBeziehung" :background="0" :font-family="'PxGroteskPan'"
          :mouse-radius="150" :repel-radius="80" :attract-power="1.5" />
        <div class="btns">
          <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeBeziehung === s.key }"
            @click="activeBeziehung = s.key">{{ s.label }}</button>
        </div>
      </div>
      <div class="split-right">
        <div style="height: 150vh;"></div>
        <div class="side-text scrollable-text">
          <h2>Nur selten fremd.</h2>
          <p>
            Die Visualisierung zeigt anhand der Anzahl Geschädigten die Beziehung zu den Beschuldigten auf. Die sechs
            Kategorien sind: Partner (Partner*innen und Ex-Partner*innen), verwandt, bekannt (Kollegen, Freunde
            Bekannte), Arbeit (Arbeit und Ausbildung), keine Beziehung und andere Beziehung (Amtsverhältnis, gesetzliche
            Vertretung, ärztlicher Kontext, ohne Angabe und unaufgeklärte Straftaten).
          </p>
          <p>
            Es bestätigt sich, was die Daten zur Örtlichkeit andeuten. Die Taten Sexualisierter Gewalt finden vor allem
            in einem vermeintlich vertrauten Umfeld statt. Einzig bei Exhibitionismus und sexueller Belästigung besteht
            meist keine Beziehung. Sexuelle Belästigung findet jedoch überall statt, gehäuft auch im Bekanntenkreis oder
            bei der Arbeit oder in der Ausbildungsstätte.
          </p>
        </div>
        <div style="height: 50vh;"></div>
      </div>
    </div>

    <!-- 6. section dunkelziffer: Sketch Dunkelziffer fullscreen -->
    <div class="fullscreen-section">
      <div class="fullscreen-sketch" id="sketch-dunkelziffer">
        <h2 class="dunkelziffer-title">Angezeigte vs. tatsächliche Sexualisierte Gewalt</h2>
        <p class="dunkelziffer-annotation">Ein Kreuz entspricht einer geschädigten Person</p>
        <div class="dunkelziffer-canvas-container">
          <P5CanvasDunkelziffer :key="activeDunkelziffer + '-' + dunkelzifferMode + '-' + filteredDunkelziffer.length"
            :data="filteredDunkelziffer" :width="widthDunkelziffer" :height="heightDunkelziffer"
            :background="'transparent'" :font-family="'PxGroteskPan'" :dunkelziffer="dunkelzifferMode"
            :mouse-radius="80" :repel-radius="100" :attract-power="10" />
        </div>
        <div class="btns fullscreen-buttons">
          <div class="filter-buttons">
            <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeDunkelziffer === s.key }"
              @click="activeDunkelziffer = s.key">{{ s.label }}</button>
          </div>
          <div class="dunkelziffer-toggle-container">
            <button :class="['toggle-btn', { 'active-dunkelziffer': dunkelzifferMode === 'hell' }]"
              @click="dunkelzifferMode = 'hell'">Angezeigt</button>
            <button :class="['toggle-btn', { 'active-dunkelziffer': dunkelzifferMode === 'dunkel' }]"
              @click="dunkelzifferMode = 'dunkel'">Tatsächlich</button>
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
          Die Polizeiliche Kriminalstatistik zählt ausschliesslich, was polizeilich erfasst wird. Was nicht angezeigt
          wird verbleibt im Dunkeln. Um neben dem Hellfeld auch das Dunkelfeld zu erfassen, werden in der Schweiz
          regelmässig Prävalenzstudien durchgeführt. Hier wird erfragt, ob die Betroffenen eine Straftat erlebt haben,
          unabhängig davon, ob sie diese auch zur Anzeige gebracht haben.
        </p>
        <p>
          Die Dunkelziffern für Sexualisierte Gewalt sind hierbei stets erschreckend hoch. Sie bewegen sich zwischen 88
          Prozent (Vergewaltigung und Sexuelle Nötigung) und 93 Prozent (sexuelle Belästigung). Das heisst nur rund eine
          von zehn Personen geht zur Polizei! Damit sind Straftaten im Bereich Sexualisierte Gewalt jene mit der
          geringsten Anzeigerate. Im Vergleich dazu: Autodiebstahl hat eine Dunkelziffer von 18 Prozent.
        </p>
        <h2 class="h2-spaced">Warum ist das so?</h2>
        <p>
          Viele Betroffene sehen aus Scham, Schuldgefühlen oder aus Angst, dass ihnen nicht geglaubt wird von einer
          Anzeige ab. Das hängt unter anderem damit zusammen, dass die meisten Tatpersonen aus dem nahen Umfeld der
          Geschädigten stammen. So sind sich Betroffene oft unsicher, ob sie überhaupt Anzeige erstatten können. Dass es
          sich bei Sexualisierter Gewalt um einen massiven, gewaltvollen Eingriff in die Intimsphäre eines Menschen
          handelt, trägt weiter zur geringen Anzeigerate bei. Vielen Betroffenen fällt es schwer, über das Erlebte zu
          sprechen. In der Gleichung zwischen Selbstschutz und Recht überwiegt die Angst vor einer Retraumatisierung.
        </p>
      </div>
    </section>

    <!-- 8. Finale Forderungen Section -->
    <section class="final-text-overlay-section">
      <div class="text-overlay-content">
        <h2 class="h2-spaced">Wir fordern</h2><br/>
        <ul class="bullet-list">
          <li><span class="bullet-cross">+</span>Präventionsarbeit: Beispielsweise in Form von nationalen
            Präventionskampagnen und Arbeit mit Tatpersonen</li>
          <li><span class="bullet-cross">+</span>Konsequenter Opferschutz: Beispielsweise durch Krisenzentren und
            24h-Beratungsstellen</li>
          <li><span class="bullet-cross">+</span>Bessere Strafverfolgung: durch eine konsequente und lückenlose
            Umsetzung des neuen Sexualstrafrechts</li>
          <li><span class="bullet-cross">+</span>Finanzielle Ressourcen: eine professionelle und nachhaltige Umsetzung
            von Massnahmen steht und fällt mit der Finanzierung</li>
        </ul>
        <h2 class="h2-spaced">Hilf mit!</h2>
          <p>
            Bestelle jetzt ein Postkarten-Set und schreibe Freund*innen, Politiker*innen und Behörden an.
            Fordere sie auf, Sexualisierte Gewalt konsequent zu bekämpfen. Oder unterstütze unsere Arbeit mit einer Spende.
          </p>
      </div>
    </section>
  </div>

</template>

<style scoped>
/* =========================
   SCROLL & LAYOUT SYSTEM
   ========================= */

/* Main Scroll Container */
.main-scroll {
  scroll-snap-type: y mandatory;
  overflow-y: auto;
  height: 100vh;
  background: #000;
}

/* Scroll Snap Behavior */
.main-scroll>section,
.split-section,
.fullscreen-section {
  scroll-snap-align: start;
  min-height: 150vh;
}

/* =========================
   FULLSCREEN SECTIONS
   ========================= */

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

/* =========================
   SPLIT SECTIONS LAYOUT
   ========================= */

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

.split-right {
  flex: 1 1 40%;
  display: flex;
  flex-direction: column;
  justify-content: left;
  background: #000;
  color: #fff;
  padding: 3em;
  position: relative;
}

.side-text {
  margin: auto 0;
  padding: 3em;
  color: #fff;
  max-width: 600px;
}

.scrollable-text {
  height: auto;
  min-height: 100vh;
  overflow-y: visible;
  position: sticky;
  top: 30px;
}

/* =========================
   FULLSCREEN SECTIONS
   ========================= */

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
  top: 30px;
  left: 50%;
  transform: translateX(-68%);
  z-index: 1;
  color: #fff;
  text-align: left;
  margin: 0;
  pointer-events: none;
}

.dunkelziffer-annotation {
  position: absolute;
  top: 75px;
  left: 18.4%;
  z-index: 1;
  color: #fff;
  text-align: left;
  margin: 0;
  pointer-events: none;
  font-family: PxGroteskPan, sans-serif;
  font-weight: 700;
  font-size: 1em;
  line-height: 1.3;
}

.dunkelziffer-canvas-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 15;
  /* Höher als Buttons, damit Kreuze über alles erscheinen */
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  /* Canvas selbst nicht klickbar, damit Buttons durchklickbar bleiben */
}

.fullscreen-buttons {
  position: absolute;
  bottom: -30px;
  /* Mehr Abstand vom unteren Rand */
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
  align-items: center;
  z-index: 10;
  pointer-events: auto;
  /* Explizit anklickbar machen */
}

/* Sicherstellen, dass alle Buttons in fullscreen-buttons anklickbar bleiben */
.fullscreen-buttons button {
  pointer-events: auto;
}

/* Button-Container in Split-Sections - mehr Abstand vom unteren Rand */
.btns {
  margin-bottom: 60px;
  /* Abstand vom unteren Rand der sticky-Elemente */
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

/* =========================
   TEXT OVERLAY SECTIONS
   ========================= */

/* Text Overlay Section - scrollt über Dunkelziffer mit sanftem Übergang */
.text-overlay-section {
  min-height: 200vh; /* Mehr Höhe für besseres Snap-Verhalten */
  background: linear-gradient(
    to bottom,
    transparent 0%,
    transparent 10%,
    rgba(0, 0, 0, 0.5) 30%,
    rgba(0, 0, 0, 1) 50%,
    #000 100%
  );
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  scroll-snap-align: start;
  margin: 0;
  position: relative;
  z-index: 3;
  margin-top: -100vh;
  padding-top: 100vh; /* Platz für Fade, dann zentrierter Text */
}

.text-overlay-content {
  max-width: 800px;
  padding: 60px;
  text-align: left;
}

/* H2 in Text-Overlay-Bereichen sollen auch engen Abstand haben */
.text-overlay-content h2 {
  margin-bottom: 3px;
}

/* Finale Forderungen Section - normale Sektion ohne Overlay */
.final-text-overlay-section {
  min-height: 100vh;
  background: #000;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  scroll-snap-align: start;
  margin: 0;
  position: relative;
  z-index: 4;
}
</style>