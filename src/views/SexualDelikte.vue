<script setup>

// Hamburger-Menü State (nur Mobile)
import { ref as vueRef, computed as vueComputed, onMounted as vueOnMounted, onUnmounted as vueOnUnmounted } from 'vue'
const menuOpen = vueRef(false)
const showHamburger = vueRef(false)


function updateShowHamburger() {
  showHamburger.value = typeof window !== 'undefined' ? window.innerWidth <= 768 : false
}

vueOnMounted(() => {
  updateShowHamburger()
  window.addEventListener('resize', updateShowHamburger)
})
vueOnUnmounted(() => {
  window.removeEventListener('resize', updateShowHamburger)
})

function handleHamburgerNav(sectionId) {
  menuOpen.value = false
  scrollToSection(sectionId)
}


// Footer Sichtbarkeit (main-scroll scroll)
const showFooter = ref(false)
function checkFooterVisibility() {
  const mainScroll = document.querySelector('.main-scroll')
  if (!mainScroll) return
  const atBottom = mainScroll.scrollTop + mainScroll.clientHeight >= mainScroll.scrollHeight - 2
  showFooter.value = atBottom
}
onMounted(() => {
  const mainScroll = document.querySelector('.main-scroll')
  if (!mainScroll) return
  mainScroll.addEventListener('scroll', checkFooterVisibility)
  checkFooterVisibility()
})
onUnmounted(() => {
  const mainScroll = document.querySelector('.main-scroll')
  if (!mainScroll) return
  mainScroll.removeEventListener('scroll', checkFooterVisibility)
})

// Dynamische body-Klasse für schwarzen Bereich unter Footer
watch(showFooter, (visible) => {
  if (visible) {
    document.body.classList.add('footer-visible')
  } else {
    document.body.classList.remove('footer-visible')
  }
})

/* ------------------------------------------------------------------
   IMPORTS
------------------------------------------------------------------ */
import {
  ref,
  computed,
  watch,
  onMounted,
  onBeforeUnmount,
  onUnmounted,
  nextTick
} from 'vue'

import * as d3 from 'd3'
import { useSketchDimensions } from '../composables/useSketchDimensions.js'

import P5CanvasGeschaedigte from '../components/P5CanvasGeschaedigte.vue'
import P5CanvasBeschuldigte from '../components/P5CanvasBeschuldigte.vue'
import P5CanvasOrt from '../components/P5CanvasOrt.vue'
import P5CanvasBeziehung from '../components/P5CanvasBeziehung.vue'
import P5CanvasDunkelziffer from '../components/P5CanvasDunkelziffer.vue'
import P5CanvasTitelblatt from '../components/P5CanvasTitelblatt.vue'
import P5CanvasForderungen from '../components/P5CanvasForderungen.vue'

import FooterBrava from '../components/FooterBrava.vue'
import FilterBottomSheet from '../components/FilterBottomSheet.vue'

// Formular State
const form = ref({
  vorname: '',
  name: '',
  email: '',
  adresse: '',
  plz: '',
  ort: '',
  kommentar: '',
  newsletter: true
})
const errors = ref({});
const formStatus = ref('');
const submitted = ref(false);

function validateForm() {
  errors.value = {};
  // Pflichtfelder
  if (!form.value.vorname) errors.value.vorname = '*** Bitte Vorname eingeben.';
  if (!form.value.name) errors.value.name = '*** Bitte Name eingeben.';
  if (!form.value.email) {
    errors.value.email = '*** Bitte E-Mail eingeben.';
  } else if (!/^\S+@\S+\.\S+$/.test(form.value.email)) {
    errors.value.email = '*** Bitte gültige E-Mail eingeben.';
  }
  if (!form.value.adresse) errors.value.adresse = '*** Bitte Adresse eingeben.';
  if (!form.value.plz) {
    errors.value.plz = '*** Bitte Postleitzahl eingeben.';
  } else if (!/^\d{4}$/.test(form.value.plz)) {
    errors.value.plz = '*** Bitte gültige Postleitzahl eingeben (4 Ziffern).';
  }
  if (!form.value.ort) errors.value.ort = '*** Bitte Ort eingeben.';
  return Object.keys(errors.value).length === 0;
}

async function handleFormSubmit() {
  if (!validateForm()) return;
  formStatus.value = '';
  const payload = new URLSearchParams();
  payload.append('vorname', form.value.vorname);
  payload.append('name', form.value.name);
  payload.append('email', form.value.email);
  payload.append('adresse', form.value.adresse);
  payload.append('plz', form.value.plz);
  payload.append('ort', form.value.ort);
  payload.append('kommentar', form.value.kommentar);
  payload.append('newsletter', form.value.newsletter ? 'Ja' : 'Nein');
  try {
    const res = await fetch('/save_form.php', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: payload.toString()
    });
    if (res.ok) {
      triggerCrossesFall();
      form.value = { vorname: '', name: '', email: '', adresse: '', plz: '', ort: '', kommentar: '', newsletter: false };
      setTimeout(() => {
        submitted.value = true;
        formStatus.value = 'Danke für deine Bestellung!';
      }, 500); //
    } else {
      formStatus.value = 'Fehler beim Speichern.';
    }
  } catch (e) {
    formStatus.value = 'Verbindungsfehler.';
  }
}

/* ------------------------------------------------------------------
   STICKY NAVIGATION
------------------------------------------------------------------ */
const activeSection = ref('')
const showNav = ref(true) // Immer sichtbar

const navItems = [
  { id: 'intro', label: 'Home' },
  { id: 'geschaedigte', label: 'Betroffene' },
  { id: 'beschuldigte', label: 'Beschuldigte' },
  { id: 'ort', label: 'Ort' },
  { id: 'dunkelziffer', label: 'Dunkelziffer' },
  { id: 'forderungen', label: 'Forderungen' },
  { id: 'pks', label: 'Über die Visualisierungen' },
  { id: 'bestellen', label: 'Postkarten bestellen' }
]

const scrollToSection = (sectionId) => {
  const mainScroll = document.querySelector('.main-scroll')
  const section = document.getElementById(`section-${sectionId}`)

  if (section && mainScroll) {
    const rect = section.getBoundingClientRect()
    const scrollTop = mainScroll.scrollTop
    const offset = rect.top

    mainScroll.scrollTo({
      top: scrollTop + offset,
      behavior: 'smooth'
    })
  }
}

onMounted(() => {
  const mainScroll = document.querySelector('.main-scroll')
  if (!mainScroll) return

  // Scroll Event für active section tracking
  mainScroll.addEventListener('scroll', () => {
    const sections = mainScroll.querySelectorAll('[id^="section-"]')
    const viewportHeight = mainScroll.clientHeight

    sections.forEach(section => {
      const rect = section.getBoundingClientRect()
      if (rect.top < viewportHeight / 2 && rect.bottom > viewportHeight / 2) {
        activeSection.value = section.id.replace('section-', '')
      }
    })
  })

  // Click außerhalb Pop-up zum Schließen
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.info-popup') && !e.target.closest('.info-btn')) {
      showInfoGeschaedigte.value = false
      showInfoBeschuldigte.value = false
      showInfoOrt.value = false
      showInfoBeziehung.value = false
      showInfoDunkelziffer.value = false
    }
  })
})

/* ------------------------------------------------------------------
   SKETCH DIMENSIONS & STATES
------------------------------------------------------------------ */
const { width: widthForderungen, height: heightForderungen } =
  useSketchDimensions({ useFullscreen: true })

const triggerFallForderungen = ref(false)
const resetForderungen = ref(0)

/* ------------------------------------------------------------------
   FORDERUNGEN ACTION
------------------------------------------------------------------ */
const triggerCrossesFall = () => {
  triggerFallForderungen.value = true
}

/* ------------------------------------------------------------------
   CONSTANTS & DATA
------------------------------------------------------------------ */
const STRAFTATEN = [
  { key: 'sexuelle_noetigung', label: 'Sexuelle Nötigung' },
  { key: 'vergewaltigung', label: 'Vergewaltigung' },
  { key: 'missbrauch', label: 'Sexueller Missbrauch' },
  { key: 'belaestigung', label: 'Sexuelle Belästigung' },
  { key: 'exhibitionismus', label: 'Exhibitionismus' }
]

const csvUrl = new URL('../assets/data_sg.csv', import.meta.url).href
const fontUrl = '/Px-Grotesk-Pan-Bold.otf'

/* ------------------------------------------------------------------
   REFS & FILTER STATES
------------------------------------------------------------------ */
const raw = ref([])

const activeGeschaedigte = ref('sexuelle_noetigung')
const activeBeschuldigte = ref('sexuelle_noetigung')
const activeOrt = ref('sexuelle_noetigung')
const activeBeziehung = ref('sexuelle_noetigung')
const activeDunkelziffer = ref('sexuelle_noetigung')
const dunkelzifferMode = ref('hell')


/* ------------------------------------------------------------------
  FILTER BOTTOM SHEET (Mobile)
------------------------------------------------------------------ */
const showFilterSheet = ref(false)
const isSketchVisible = ref(false)

// Info-Overlay für Mobile
const showMobileInfo = ref(false)

let sketchObserver = null

onMounted(() => {
  const mainScroll = document.querySelector('.main-scroll')
  if (!mainScroll) return

  // IDs der Sketch-Container
  const sketchIds = [
    'sketch-geschaedigte',
    'sketch-beschuldigte',
    'sketch-ort',
    'sketch-beziehung',
    'sketch-dunkelziffer'
  ]

  const targets = sketchIds
    .map(id => document.getElementById(id))
    .filter(Boolean)

  sketchObserver = new IntersectionObserver(
    (entries) => {
      // Mindestens ein Sketch sichtbar?
      isSketchVisible.value = entries.some(entry => entry.isIntersecting)
    },
    {
      root: mainScroll,
      threshold: 0.3 // Passe an, wie viel sichtbar sein muss (z.B. 0.3 = 30%)
    }
  )

  targets.forEach(target => sketchObserver.observe(target))
})

onUnmounted(() => {
  if (sketchObserver) {
    sketchObserver.disconnect()
    sketchObserver = null
  }
})

/* ------------------------------------------------------------------
   INFO POPUP STATE
------------------------------------------------------------------ */
const showInfoGeschaedigte = ref(false)
const showInfoBeschuldigte = ref(false)
const showInfoOrt = ref(false)
const showInfoBeziehung = ref(false)
const showInfoDunkelziffer = ref(false)

/* ------------------------------------------------------------------
   ACCORDION STATE
------------------------------------------------------------------ */
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


/* ------------------------------------------------------------------
   SKETCH DIMENSIONS
------------------------------------------------------------------ */
const { width: widthGeschaedigte, height: heightGeschaedigte } = useSketchDimensions()
const { width: widthBeschuldigte, height: heightBeschuldigte } = useSketchDimensions()
const { width: widthOrt, height: heightOrt } = useSketchDimensions()
const { width: widthBeziehung, height: heightBeziehung } = useSketchDimensions()
import { ref as vueRef2, computed as vueComputed2 } from 'vue'
const isMobile = vueRef2(typeof window !== 'undefined' ? window.innerWidth <= 768 : false)
if (typeof window !== 'undefined') {
  window.addEventListener('resize', () => {
    isMobile.value = window.innerWidth <= 768
  })
}
const { width: widthTitelblatt, height: heightTitelblatt } =
  useSketchDimensions({ useFullscreen: true })
const { width: widthDunkelziffer, height: heightDunkelziffer } =
  useSketchDimensions({ useFullscreen: true })

/* ------------------------------------------------------------------
   CSV LOAD + INTERSECTION OBSERVER (RESET LOGIC)
------------------------------------------------------------------ */
let intersectionObserver = null

onMounted(async () => {
  raw.value = await d3.csv(csvUrl, d3.autoType)
  setupIntersectionObservers()
})

const setupIntersectionObservers = () => {
  intersectionObserver = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) {
          const id = entry.target.id

          if (id === 'sketch-forderungen') {
            if (triggerFallForderungen.value) {
              resetSketchToDefault(id)
            }
          } else {
            resetSketchToDefault(id)
          }
        }
      })
    },
    {
      threshold: 0.1,
      rootMargin: '-100px'
    }
  )

  const sketchIds = [
    'sketch-geschaedigte',
    'sketch-beschuldigte',
    'sketch-ort',
    'sketch-beziehung',
    'sketch-dunkelziffer',
    'sketch-forderungen'
  ]

  sketchIds.forEach(id => {
    const el = document.getElementById(id)
    if (el) intersectionObserver.observe(el)
  })
}

const resetSketchToDefault = (id) => {
  switch (id) {
    case 'sketch-geschaedigte':
      activeGeschaedigte.value = 'sexuelle_noetigung'
      break
    case 'sketch-beschuldigte':
      activeBeschuldigte.value = 'sexuelle_noetigung'
      break
    case 'sketch-ort':
      activeOrt.value = 'sexuelle_noetigung'
      break
    case 'sketch-beziehung':
      activeBeziehung.value = 'sexuelle_noetigung'
      break
    case 'sketch-dunkelziffer':
      activeDunkelziffer.value = 'sexuelle_noetigung'
      dunkelzifferMode.value = 'hell'
      break
    case 'sketch-forderungen':
      triggerFallForderungen.value = false
      resetForderungen.value++
      break
  }
}

/* ------------------------------------------------------------------
   TEXT ERSCHEINT ERST NACH VERLASSEN DER VISUALISIERUNG
------------------------------------------------------------------ */
const showText = ref(false)
let textObserver = null

onMounted(async () => {
  await nextTick()

  const el = document.getElementById('sketch-section')
  if (!el) return

  textObserver = new IntersectionObserver(
    entries => {
      showText.value = !entries[0].isIntersecting
    },
    { threshold: 0 }
  )

  textObserver.observe(el)
})

/* ------------------------------------------------------------------
   CLEANUP
------------------------------------------------------------------ */
onUnmounted(() => {
  if (textObserver) textObserver.disconnect()
})

onBeforeUnmount(() => {
  if (intersectionObserver) intersectionObserver.disconnect()
})

/* ------------------------------------------------------------------
   COMPUTED FILTERS
------------------------------------------------------------------ */
const filteredGeschaedigte = computed(() =>
  raw.value.filter(d => d.straftat === activeGeschaedigte.value)
)

const filteredBeschuldigte = computed(() =>
  raw.value.filter(d => d.straftat === activeBeschuldigte.value)
)

const filteredOrt = computed(() =>
  raw.value.filter(d => d.straftat === activeOrt.value)
)

const filteredBeziehung = computed(() =>
  raw.value.filter(d => d.straftat === activeBeziehung.value)
)

const filteredDunkelziffer = computed(() =>
  raw.value.filter(d => d.straftat === activeDunkelziffer.value)
)

/* ------------------------------------------------------------------
   WATCHERS
------------------------------------------------------------------ */
watch(activeDunkelziffer, () => {
  dunkelzifferMode.value = 'hell'
})

/* ------------------------------------------------------------------
   HELPERS
------------------------------------------------------------------ */
function setFilter(key) {
  activeGeschaedigte.value = key
}
</script>


<template>

  <!-- Dot Navigation (nur Desktop/Tablet) -->
  <nav class="dot-nav" :class="{ 'nav-hidden': !showNav }">
    <button v-for="item in navItems" :key="item.id" class="dot-item"
      :class="{ 'dot-active': activeSection === item.id }" @click="scrollToSection(item.id)" :title="item.label">
      <span class="dot"></span>
      <span class="dot-label">{{ item.label }}</span>
    </button>
  </nav>

  <!-- Hamburger-Menü (nur Mobile) -->
  <div class="hamburger-menu" v-if="showHamburger">
    <button class="hamburger-btn" :class="{ open: menuOpen }" @click="menuOpen = !menuOpen" :aria-expanded="menuOpen">
      <span class="hamburger-icon"></span>
    </button>
    <div class="hamburger-overlay" v-if="menuOpen">
      <nav class="hamburger-nav">
        <button v-for="item in navItems" :key="item.id" class="hamburger-link" @click="handleHamburgerNav(item.id)">
          {{ item.label }}
        </button>
      </nav>
    </div>
  </div>

  <!-- Filter-Button (nur Mobile & wenn P5 sichtbar) -->
  <button v-if="showHamburger && isSketchVisible && !menuOpen" class="filter-btn-mobile" @click="showFilterSheet = true"
    aria-label="Filter öffnen">
    {{STRAFTATEN.find(s => s.key === (activeSection === 'beschuldigte' ? activeBeschuldigte : activeSection === 'ort' ? activeOrt : activeSection === 'beziehung' ? activeBeziehung : activeSection === 'dunkelziffer' ? activeDunkelziffer : activeGeschaedigte))?.label || 'Straftat auswählen'}}
    <svg width="24" height="24" viewBox="0 0 24 24"
      style="margin-left:0.4em; vertical-align:middle; display:inline-block;">
      <polyline points="5,8 12,16 19,8" fill="none" stroke="#fff" stroke-width="3" />
    </svg>
  </button>


  <div class="main-scroll">
    <!-- 1a. Titelbild -->
    <div class="fullscreen-section" id="section-intro">
      <div class="fullscreen-sketch">
        <div class="titelblatt-text">
          <h1>Muster<br />und blinde<br />Flecken</h1>
          <h2 class="titelblatt-headline">Was die Polizeiliche Kriminalstatistik 2025 zu<br />Sexualisierter Gewalt <br
              class="mobile-only" />aufzeigt
            – und was nicht</h2>
        </div>
        <div class="titelblatt-canvas-container">
          <P5CanvasTitelblatt :width="widthTitelblatt" :height="heightTitelblatt" :background="'transparent'"
            :isMobile="isMobile" :font-family="'PxGroteskPan'" />
        </div>
      </div>
    </div>

    <!-- 1b. section PKS text: Erklärungstext als Overlay/Stacking -->
    <section class="text-overlay-section">
      <div class="text-overlay-content">
        <h2>Sexualisierte Gewalt – wir schauen hin</h2>
        <p>
          Die Polizei sammelt kontinuierlich Kennziffern zu angezeigten Straftaten, auch zu Sexualisierter Gewalt. Sie
          werden jährlich in der Polizeilichen Kriminalstatistik der Schweiz veröffentlicht.
        </p>
        <p>Diese Zahlen sind wichtig: Sie zeigen Entwicklungen, Muster, Häufungen. Sie machen sichtbar, wer Gewalt
          ausübt, wer betroffen ist und wo Taten passieren. Und sie lassen erkennen, wieviel Gewalt unentdeckt bleibt.
        </p>
        <p>
          Auf dieser Scrollseite zeigen wir in vier Visualisierungen grundlegende Strukturen von Delikten im Bereich
          Sexualisierte Gewalt.
        </p>
        <ul class="cross-list">
          <li><a href="#section-geschaedigte">Wer ist von Sexualisierter Gewalt betroffen?</a></li>
          <li><a href="#section-beschuldigte">Wer übt Sexualisierte Gewalt aus?</a></li>
          <li><a href="#section-ort">Wo findet Sexualisierte Gewalt statt?</a></li>
          <!-- <li><a href="#section-beziehung">Welche Beziehung haben Tatpersonen und Betroffene?</a></li> -->
          <li><a href="#section-dunkelziffer">Wie hoch ist die Dunkelziffer?</a></li>
          <li><a href="#section-pks">Über die Visualisierungen</a></li>
        </ul>
      </div>
    </section>

    <!-- 2. Split-Section: Sketch links sticky, rechts scrollt Text hoch -->
    <div class="split-section" id="section-geschaedigte">
      <div id="sketch-geschaedigte" class="split-left sticky-sketch">
        <h2>Wer ist von Sexualisierter Gewalt betroffen?</h2>
        <P5CanvasGeschaedigte :key="activeGeschaedigte + '-' + filteredGeschaedigte.length" :data="filteredGeschaedigte"
          :width="widthGeschaedigte" :height="heightGeschaedigte" :font-family="'PxGroteskPan'" :background="255"
          :isMobile="isMobile" />
        <div class="btns" v-if="!showHamburger">
          <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeGeschaedigte === s.key }"
            @click="activeGeschaedigte = s.key">{{ s.label }}</button>
          <button class="info-btn" @click="showInfoGeschaedigte = !showInfoGeschaedigte">i</button>
        </div>

        <!-- Info Pop-up -->
        <div v-if="showInfoGeschaedigte" class="info-popup">
          <button class="popup-close" @click="showInfoGeschaedigte = false">×</button>
          <h3>Anmerkungen</h3>
          <p>Darstellung: Ein Kreuz entspricht einer geschädigten bzw. betroffenen Person. </p>
          <p>Definitionen: Weitere Infos zu den einzelnen Straftaten findest du im Abschnitt <a
              href="#section-pks">«Über die Visualisierungen»</a>.</p>
          <p>Quelle: Polizeiliche Kriminalstatistik 2025, Bundesamt für Statistik.</p>
        </div>
      </div>

      <div class="split-right">
        <div v-if="!isMobile" style="height: 150vh;"></div>
        <div class="side-text scrollable-text">
          <h2>Nicht alle Männer aber fast immer ein Mann</h2>
          <p>
            Die Darstellung weist das Geschlecht der Beschuldigten für die einzelnen Straftaten aus. Das Verhältnis ist
            noch eindeutiger als bei den Betroffenen Sexualisierter Gewalt. Zwischen 96 Prozent (sexuelle Nötigung) und
            annähernd 100 Prozent (Vergewaltigung) der Beschuldigten sind Männer.
          </p>
          <p>
            Wichtig zu wissen: Vor der Sexualstrafrechtsreform kannte der Straftatbestand Vergewaltigung ausschliesslich
            weibliche Betroffene und männliche Täter. Seit 1. Juli 2024 ist das Gesetz geschlechtsneutral definiert.
            Vergewaltigung umfasst jegliche Penetration gegen den Willen der betroffenen Person. Ausserdem ist es neu
            auch eine Vergewaltigung, wenn Täter_innen einen Schockzustand ausnutzen.
          </p>
        </div>
        <div v-if="!isMobile" style="height: 50vh;"></div>
      </div>
    </div>

    <!-- 3. Split Section: Sketch Beschuldigte sticky + Text (unverändert) -->
    <div class="split-section" id="section-beschuldigte">
      <div class="split-left sticky-sketch" id="sketch-beschuldigte">
        <h2>Wer übt Sexualisierte Gewalt aus?</h2>
        <P5CanvasBeschuldigte :key="activeBeschuldigte + '-' + filteredBeschuldigte.length" :data="filteredBeschuldigte"
          :width="widthBeschuldigte" :height="heightBeschuldigte" :background="255" :font-family="'PxGroteskPan'"
          :isMobile="isMobile"
          :show-labels="true" left-field="beschuldigte_f" right-field="beschuldigte_m" left-label="Frauen"
          right-label="Männer" :mouse-radius="150" :repel-radius="80" :attract-power="1.5" />
        <div class="btns" v-if="!showHamburger">
          <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeBeschuldigte === s.key }"
            @click="activeBeschuldigte = s.key">{{ s.label }}</button>
          <button class="info-btn" @click="showInfoBeschuldigte = !showInfoBeschuldigte">i</button>
        </div>

        <!-- Info Pop-up -->
        <div v-if="showInfoBeschuldigte" class="info-popup">
          <button class="popup-close" @click="showInfoBeschuldigte = false">×</button>
          <h3>Anmerkungen</h3>
          <p>Darstellung: Ein Kreuz entspricht einer beschuldigten Person.</p>
          <p>Definitionen: Weitere Infos zu den einzelnen Straftaten findest du im Abschnitt <a
              href="#section-pks">«Über
              die Visualisierungen»</a>.</p>
          <p>Quelle: Polizeiliche Kriminalstatistik 2025, Bundesamt für Statistik.</p>
        </div>
      </div>

      <div class="split-right">
        <div v-if="!isMobile" style="height: 150vh;"></div>
        <div class="side-text scrollable-text">
          <h2>Nicht alle Männer aber fast immer ein Mann</h2>
          <p>
            Die Darstellung weist das Geschlecht der Beschuldigten für die einzelnen Straftaten aus. Das Verhältnis ist
            noch eindeutiger als bei den Betroffenen Sexualisierter Gewalt. Zwischen 96 Prozent (sexuelle Nötigung) und
            annähernd 100 Prozent (Vergewaltigung) der Beschuldigten sind Männer.
          </p>
          <p>
            Wichtig zu wissen: Vor der Sexualstrafrechtsreform kannte der Straftatbestand Vergewaltigung ausschliesslich
            weibliche Betroffene und männliche Täter. Seit 1. Juli 2024 ist das Gesetz geschlechtsneutral definiert.
            Vergewaltigung umfasst jegliche Penetration gegen den Willen der betroffenen Person. Ausserdem ist es neu
            auch eine Vergewaltigung, wenn Täter_innen einen Schockzustand ausnutzen.
          </p>
        </div>
        <div v-if="!isMobile" style="height: 50vh;"></div>
      </div>
    </div>

    <!-- 4. section ort: Sketch Ort sticky + Text -->
    <div class="split-section" id="section-ort">
      <div class="split-left sticky-sketch" id="sketch-ort">
        <h2>Wo findet Sexualisierte Gewalt statt?</h2>
        <P5CanvasOrt :key="activeOrt + '-' + filteredOrt.length" :data="filteredOrt" :width="widthOrt"
          :height="heightOrt" :background="255" :font-family="'PxGroteskPan'" :isMobile="isMobile" />
        <div class="btns" v-if="!showHamburger">
          <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeOrt === s.key }"
            @click="activeOrt = s.key">{{ s.label }}</button>
          <button class="info-btn" @click="showInfoOrt = !showInfoOrt">i</button>
        </div>

        <!-- Info Pop-up -->
        <div v-if="showInfoOrt" class="info-popup">
          <button class="popup-close" @click="showInfoOrt = false">×</button>
          <h3>Anmerkungen</h3>
          <p>Darstellung: Ein Kreuz entspricht einer Straftat.</p>
          <p>Hinweis: Als privater Raum gelten ausschliesslich die eigenen vier Wände. Treppenhaus oder Waschküche
            gelten bereits als öffentlich. Delikte, bei denen kein Ort angegeben wurde, sind nicht dargestellt.</p>
          <p>Definitionen: Weitere Infos zu den einzelnen Straftaten findest du im Abschnitt <a
              href="#section-pks">«Über
              die Visualisierungen»</a>.</p>
          <p>Quelle: Polizeiliche Kriminalstatistik 2025, Bundesamt für Statistik.</p>
        </div>
      </div>

      <div class="split-right">
        <div v-if="!isMobile" style="height: 150vh;"></div>
        <div class="side-text scrollable-text">
          <h2>Das Zuhause ist kein sicherer Ort</h2>
          <p>
            Die Taten Sexualisierter Gewalt finden überwiegend im privaten Umfeld statt. Ausgenommen sind sexuelle
            Belästigung und Exhibitionismus.
          </p>
          <p>
            Sexuelle Nötigung, Vergewaltigung und sexuelle Übergriffe finden überwiegend im privaten Umfeld statt. Das
            steht im Widerspruch zu verbreiteten Vergewaltigungsmythen, die den Täter als fremden Mann im Dunkeln
            zeichnen.
          </p>
        </div>
        <div v-if="!isMobile" style="height: 50vh;"></div>
      </div>
    </div>

    <!---||||||||||||||||||||SPÄTER FREIGEBEN und inhaltlich noch anpassen||||||||||||||||||||||||
   |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
   |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||-->

    <!-- 5. section beziehung: Sketch Beziehung sticky + Text
    <div class="split-section" id="section-beziehung">
      <div class="split-left sticky-sketch" id="sketch-beziehung">
        <h2>Welche Beziehung haben Beschuldigte und Geschädigte?</h2>
        <P5CanvasBeziehung :key="activeBeziehung + '-' + filteredBeziehung.length" :data="filteredBeziehung"
          :width="widthBeziehung" :height="heightBeziehung" :background="255" :font-family="'PxGroteskPan'"
          :mouse-radius="150" :repel-radius="80" :attract-power="1.5" />
        <div class="btns" v-if="!showHamburger">
          <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeBeziehung === s.key }"
            @click="activeBeziehung = s.key">{{ s.label }}</button>
          <button class="info-btn" @click="showInfoBeziehung = !showInfoBeziehung">i</button>
        </div>

        <div v-if="showInfoBeziehung" class="info-popup">
          <button class="popup-close" @click="showInfoBeziehung = false">×</button>
          <h3>Beziehung</h3>
          <p>Darstellung: Ein Kreuz entspricht einer geschädigten Person</p>
          <p>Quelle:Polizeiliche Kriminalstatistik (PKS) 2024, Bundesamt für Statistik</p>
          <p>Kategorien: Partner (inkl. Ex), verwandt, bekannt, Arbeit/Ausbildung, keine Beziehung,
            andere Beziehung</p>
        </div>
      </div>

      <div class="split-right">
        <div v-if="!isMobile" style="height: 150vh;"></div>
        <div class="side-text scrollable-text">
          <h2>Täter*innen sind selten fremd</h2>
          <p>
            Die Visualisierung zeigt anhand der Anzahl Geschädigten die Beziehung zu den Beschuldigten auf. Die sechs
            Kategorien sind: </p>
          <ul class="cross-list">
            <li>Partner (Partner*innen und Ex-Partner*innen)</li>
            <li>verwandt</li>
            <li>bekannt (Kolleg*innen, Freund*innen, Bekannte)</li>
            <li>Arbeit (Arbeit und Ausbildung)</li>
            <li>keine Beziehung</li>
            <li>andere Beziehung (Amtsverhältnis, gesetzliche Vertretung, ärztlicher Kontext, ohne Angabe und
              unaufgeklärte Straftaten)</li>
          </ul>
          <p>
            Es bestätigt sich, was die Daten zur Örtlichkeit andeuten. Die Taten Sexualisierter Gewalt finden vor allem
            in vertrautem Umfeld statt. Einzig bei Exhibitionismus und sexueller Belästigung besteht keine Beziehung.
            Sexuelle Belästigung findet jedoch überall statt, auch im Bekanntenkreis,
            bei der Arbeit oder in der Ausbildungsstätte.
          </p>
        </div>
        <div v-if="!isMobile" style="height: 50vh;"></div>
      </div>
    </div> -->

    <!-- 6. section dunkelziffer: Sketch Dunkelziffer fullscreen -->
    <div class="fullscreen-section" id="section-dunkelziffer">
      <div class="fullscreen-sketch" id="sketch-dunkelziffer">
        <h2 class="dunkelziffer-title">Angezeigte vs. tatsächliche Sexualisierte Gewalt</h2>
        <div class="dunkelziffer-canvas-container">
          <P5CanvasDunkelziffer :key="activeDunkelziffer + '-' + filteredDunkelziffer.length"
            :data="filteredDunkelziffer" :width="widthDunkelziffer" :height="heightDunkelziffer"
            :background="'transparent'" :font-family="'PxGroteskPan'" :dunkelziffer="dunkelzifferMode"
            :isMobile="isMobile" :mouse-radius="80" :repel-radius="100" :attract-power="10" />
        </div>
        <!-- Info-Popup entfernt, nur noch expanding Button -->
        <div v-if="!isMobile" style="height: 50vh;"></div>
      </div>
      <div class="btns fullscreen-buttons" v-if="!showHamburger">
        <div class="filter-buttons-with-info">
          <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeDunkelziffer === s.key }"
            @click="activeDunkelziffer = s.key">{{ s.label }}</button>
        </div>
        <div class="dunkelziffer-toggle-container">
          <button :class="['toggle-btn', { 'active-dunkelziffer': dunkelzifferMode === 'hell' }]"
            @click="dunkelzifferMode = 'hell'">Angezeigt</button>
          <button :class="['toggle-btn', { 'active-dunkelziffer': dunkelzifferMode === 'dunkel' }]"
            @click="dunkelzifferMode = 'dunkel'">Tatsächlich</button>
        </div>
        <div class="info-btn-absolute-wrapper">
          <button class="info-btn" @click="showInfoDunkelziffer = !showInfoDunkelziffer">i</button>
          <div v-if="showInfoDunkelziffer" class="info-popup info-popup-dunkelziffer">
            <button class="popup-close" @click="showInfoDunkelziffer = false">×</button>
            <h3>Anmerkungen</h3>
            <p>Darstellung: Ein Kreuz entspricht einer betroffenen Person.</p>
            <p>Hinweis: «Angezeigt» stellt das Hellfeld, also die Anzahl polizeilich registrierter Betroffener dar.
              «Tatsächlich» zeigt die Anzahl Betroffener, wenn sowohl Hellfeld als auch Dunkelfeld berücksichtigt
              werden.</p>
            <p>Definitionen: Weitere Infos zu den einzelnen Straftaten findest du im Abschnitt <a
                href="#section-pks">«Über die Visualisierungen»</a>.</p>
            <p>Quellen: Polizeiliche Kriminalstatistik 2025, Bundesamt für Statistik (Hellfeld). Crime Survey 2022 –
              Studie im Auftrag der Konferenz der Kantonalen Polizeikommandanten (Dunkelfeld).</p>
          </div>
        </div>
      </div>
    </div>


    <!-- 7. section dunkelziffer text: Erklärungstext als Overlay/Stacking -->
    <section class="text-overlay-section">
      <div class="text-overlay-content">
        <h2>Das meiste bleibt im Dunkeln</h2>
        <p>
          Die Dunkelziffern für Sexualisierte Gewalt bewegen sich zwischen 88% (Vergewaltigung) und 93% (sexuelle Belästigung). Das heisst, nur rund eine von zehn Personen geht zur Polizei.
          Straftaten im Bereich Sexualisierte Gewalt haben damit die geringste Anzeigerate. Zum Vergleich:
          Autodiebstahl hat eine Dunkelziffer von 18%.
        </p>
        <h2 class="h2-spaced">Warum ist das so?</h2>
        <p>
          Viele Betroffene sehen aus Scham, Schuldgefühlen oder aus Angst, dass ihnen nicht geglaubt wird, von einer
          Anzeige ab. Das hängt unter anderem damit zusammen, dass die meisten Tatpersonen aus dem nahen Umfeld der
          Geschädigten stammen. Betroffene sind sich oft unsicher, ob sie überhaupt Anzeige erstatten können. Dass es
          sich bei Sexualisierter Gewalt um einen massiven, gewaltvollen Eingriff in die Intimsphäre eines Menschen
          handelt, trägt weiter zur geringen Anzeigerate bei. Vielen Betroffenen fällt es schwer, über das Erlebte zu
          sprechen. In der Gleichung zwischen Selbstschutz und Recht überwiegt die Angst vor einer Retraumatisierung.
        </p>
      </div>
    </section>

    <!-- 8. Finale Forderungen Section mit P5 Canvas im Vordergrund -->
    <section class="final-text-overlay-section" id="section-forderungen">
      <!-- Canvas moved to bestellen section -->
      <div class="text-overlay-content">
        <h2 class="h2-spaced">Wir fordern</h2>
        <ul class="cross-list">
          <li>Präventionsarbeit, wie zum Beispiel die aktuelle nationale Präventionskampagne und Arbeit mit Tatpersonen
          </li>
          <li>Konsequenter Opferschutz, beispielsweise durch Krisenzentren und 24h-Beratungsstellen</li>
          <li>Bessere Strafverfolgung durch eine konsequente und lückenlose Umsetzung des neuen Sexualstrafrechts</li>
          <li>Finanzielle Ressourcen – eine professionelle und nachhaltige Umsetzung von Massnahmen steht und fällt mit
            der Finanzierung</li>
        </ul>
      </div>
    </section>


    <!-- 10. Neue Text-Overlay-Section über pks -->
    <section class="text-overlay-section" id="section-pks">
      <div class="text-overlay-content">
        <!-- Hier kannst du deinen Text über pks oder weitere Inhalte einfügen -->
        <h2>Über die Visualisierungen</h2>
        <p>In vier Visualisierungen betrachten wir zentrale Delikte Sexualisierter Gewalt. Unter dem Begriff der
          Sexualisierten Gewalt verstehen wir Straftatbestände, welche Gewalt und
          sexualisierte Handlungen beinhalten. Diese werden ohne ausdrückliches Einverständnis und gegen den Willen
          der betroffenen Person angedroht, aufgedrängt oder aufgezwungen.</p>
        <p>Für die interaktiven Grafiken haben wir uns auf die häufigsten Delikte konzentriert. Sexuelle Handlungen
          mit Kindern haben wir nicht berücksichtigt, da diese eine gesonderte Analyse und besondere Schutzmassnahmen erfordern.
          <!-- Vertiefte Informationen hierzu bietet <a
            href="https://www.kinderschutz.ch/themen/sexualisierte-gewalt" target="_blank">Kinderschutz Schweiz</a>.-->
            Zudem wichtig zu wissen: Die Statistik registriert nur zwei Geschlechter.</p>

        <p>Folgende Straftaten haben wir analysiert:<br /></p>

        <div class="accordion-list">
          <div class="accordion-item">
            <div class="accordion-header" @click="toggleAccordion('sexuellerUebergriff')">
              <span class="accordion-icon" :class="{ 'open': openAccordions.sexuellerUebergriff }">+</span>
              <span>Sexueller Übergriff und sexuelle Nötigung</span>
            </div>
            <div class="accordion-content" :class="{ 'open': openAccordions.sexuellerUebergriff }">
              <p>Sexueller Übergriff: Sexuelle Handlung gegen den Willen oder Ausnutzen eines Schockzustands.</p>
              <p>Sexuelle Nötigung: Zu sexueller Handlung zwingen (Drohung, Gewalt, psychischer Druck,
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
        <!-- <h2>Datenquellen</h2>
        <p>Die Visualisierungen basieren auf den Daten der Polizeilichen Kriminalstatistik 2025, welche vom Bundesamt
          für Statistik herausgegeben wird. Die Statistik zählt alle angezeigten bzw. polizeilich registrierten Fälle.
          Wichtig zu wissen: Die
          Statistik registriert nur zwei Geschlechter.</p>
        <p>
          Die Kriminalstatistik zählt ausschliesslich, was polizeilich erfasst wird. Was nicht angezeigt wird,
          verbleibt im Dunkeln. Um neben dem Hellfeld auch das Dunkelfeld zu erfassen, werden in der Schweiz regelmässig
          Prävalenzstudien durchgeführt. Eine repräsentative Stichprobe in der Schweizer Bevölkerung wird befragt, ob
          sie eine Straftat erlebt hat, unabhängig davon, ob sie diese auch zur Anzeige gebracht hat. Die aktuellste
          Prävalenzstudie, die wir auch in unserer Analyse verwenden, ist der <a
            href="https://www.unisg.ch/de/universitaet/schools/law/forschung/sk-hsg/resultate-des-swiss-crime-survey-2022/"
            target="_blank">Crime Survey 2022</a>.</p> -->

      </div>

    </section>

    <!-- 9. Bestell-Section: Kartenset bestellen -->
    <section class="final-text-overlay-section" id="section-bestellen">
      <div class="forderungen-canvas-container">
        <P5CanvasForderungen :width="widthForderungen" :height="heightForderungen" :background="'transparent'"
          :font-family="'PxGroteskPan'" :trigger-fall="triggerFallForderungen" :reset-counter="resetForderungen" />
      </div>
      <div class="text-overlay-content">
        <h2>Jetzt Kartenset bestellen</h2>
        <p>
          Bestelle jetzt ein Set mit drei Postkarten und mache sichtbar, was oft verborgen bleibt. Schreibe Menschen in
          deinem Umfeld und fordere konsequentes und kollektives Handeln gegen sexualisierte Gewalt.
        </p>
        <div class="bestellung-form-success-wrapper">
          <div v-if="!submitted">
            <form class="kontakt-form" @submit.prevent="handleFormSubmit">
              <div class="form-row">
                <div class="form-field">
                  <label for="email">E-Mail*</label>
                  <input id="email" name="email" v-model="form.email" autocomplete="off" />
                  <span v-if="errors.email" class="form-error">{{ errors.email }}</span>
                </div>
              </div>
              <div class="form-row two-cols">
                <div class="form-field">
                  <label for="vorname">Vorname*</label>
                  <input id="vorname" name="vorname" v-model="form.vorname" autocomplete="off" />
                  <span v-if="errors.vorname" class="form-error">{{ errors.vorname }}</span>
                </div>
                <div class="form-field">
                  <label for="name">Name*</label>
                  <input id="name" name="name" v-model="form.name" autocomplete="off" />
                  <span v-if="errors.name" class="form-error">{{ errors.name }}</span>
                </div>
              </div>
              <div class="form-row">
                <div class="form-field">
                  <label for="adresse">Adresse*</label>
                  <input id="adresse" name="adresse" v-model="form.adresse" autocomplete="off" />
                  <span v-if="errors.adresse" class="form-error">{{ errors.adresse }}</span>
                </div>
              </div>
              <div class="form-row two-cols">
                <div class="form-field">
                  <label for="plz">Postleitzahl*</label>
                  <input id="plz" name="plz" v-model="form.plz" autocomplete="off" />
                  <span v-if="errors.plz" class="form-error">{{ errors.plz }}</span>
                </div>
                <div class="form-field">
                  <label for="ort">Ort*</label>
                  <input id="ort" name="ort" v-model="form.ort" autocomplete="off" />
                  <span v-if="errors.ort" class="form-error">{{ errors.ort }}</span>
                </div>
              </div>
              <div class="form-row">
                <div class="form-field">
                  <label for="kommentar">Kommentar</label>
                  <textarea id="kommentar" name="kommentar" rows="4" v-model="form.kommentar"></textarea>
                </div>
              </div>
              <label class="checkbox-field" for="newsletter">
                <input id="newsletter" type="checkbox" name="newsletter" v-model="form.newsletter" />
                Updates erhalten und auf dem Laufenden bleiben. Eine Abmeldung ist jederzeit möglich.
              </label>
              <button type="submit" class="fall-button">
                Bestellen
              </button>
            </form>
          </div>
          <div v-else class="bestellung-success-message">
            <span>Danke für deine Bestellung!</span>
          </div>
        </div>
      </div>
    </section>

    <!-- FooterBrava nur anzeigen, wenn ganz unten -->
    <FooterBrava class="footer-brava" :class="{ 'footer-visible': showFooter }" />

    <!-- Filter-Bottom-Sheet für Mobile -->
    <FilterBottomSheet :show="showFilterSheet" @close="showFilterSheet = false">
      <div class="filter-sheet-list">
        <!-- Angezeigt/Tatsächlich Toggle (nur bei Dunkelziffer) -->
        <div v-if="activeSection === 'dunkelziffer'" class="dunkelziffer-toggle-mobile">
          <button :class="['dz-toggle-btn', { active: dunkelzifferMode === 'hell' }]" @click="dunkelzifferMode = 'hell'; showFilterSheet = false">Angezeigt</button>
          <button :class="['dz-toggle-btn', { active: dunkelzifferMode === 'dunkel' }]" @click="dunkelzifferMode = 'dunkel'; showFilterSheet = false">Tatsächlich</button>
        </div>
        <button v-for="s in STRAFTATEN" :key="s.key"
          :class="['filter-sheet-btn', { active: (activeSection === 'beschuldigte' ? activeBeschuldigte : activeSection === 'ort' ? activeOrt : activeSection === 'beziehung' ? activeBeziehung : activeSection === 'dunkelziffer' ? activeDunkelziffer : activeGeschaedigte) === s.key }]"
          @click="activeSection === 'beschuldigte' ? activeBeschuldigte = s.key : activeSection === 'ort' ? activeOrt = s.key : activeSection === 'beziehung' ? activeBeziehung = s.key : activeSection === 'dunkelziffer' ? activeDunkelziffer = s.key : activeGeschaedigte = s.key; showFilterSheet = false">
          <span class="filter-sheet-btn-label">{{ s.label }}</span>
        </button>
        <!-- Info-Button im gleichen Stil -->
        <button class="filter-sheet-btn" @click="showMobileInfo = true">
          <span class="filter-sheet-btn-label">Info</span>
        </button>
        <!-- <button class="filter-sheet-info-btn" @click="showInfoGeschaedigte = !showInfoGeschaedigte">Info</button> -->
        <!-- <button class="info-btn" @click="showMobileInfo = true">i</button> -->
      </div>
    </FilterBottomSheet>

    <!-- Info-Overlay nur für Mobile -->
    <div v-if="showMobileInfo && showHamburger" class="mobile-info-overlay">
      <button class="close-btn" @click="showMobileInfo = false">×</button>
      <div class="mobile-info-content">
        <h3>Anmerkungen</h3>
        <template v-if="activeSection === 'beschuldigte'">
          <p>Darstellung: Ein Kreuz entspricht einer beschuldigten Person.</p>
          <p>Definitionen: Weitere Infos zu den einzelnen Straftaten findest du im Abschnitt <a href="#section-pks">«Über die Visualisierungen»</a>.</p>
          <p>Quelle: Polizeiliche Kriminalstatistik 2025, Bundesamt für Statistik.</p>
        </template>
        <template v-else-if="activeSection === 'ort'">
          <p>Darstellung: Ein Kreuz entspricht einer Straftat.</p>
          <p>Hinweis: Als privater Raum gelten ausschliesslich die eigenen vier Wände. Treppenhaus oder Waschküche gelten bereits als öffentlich. Delikte, bei denen kein Ort angegeben wurde, sind nicht dargestellt.</p>
          <p>Definitionen: Weitere Infos zu den einzelnen Straftaten findest du im Abschnitt <a href="#section-pks">«Über die Visualisierungen»</a>.</p>
          <p>Quelle: Polizeiliche Kriminalstatistik 2025, Bundesamt für Statistik.</p>
        </template>
        <template v-else-if="activeSection === 'beziehung'">
          <p>Darstellung: Ein Kreuz entspricht einer geschädigten Person.</p>
          <p>Kategorien: Partner (inkl. Ex), verwandt, bekannt, Arbeit/Ausbildung, keine Beziehung, andere Beziehung.</p>
          <p>Definitionen: Weitere Infos zu den einzelnen Straftaten findest du im Abschnitt <a href="#section-pks">«Über die Visualisierungen»</a>.</p>
          <p>Quelle: Polizeiliche Kriminalstatistik 2025, Bundesamt für Statistik.</p>
        </template>
        <template v-else-if="activeSection === 'dunkelziffer'">
          <p>Darstellung: Ein Kreuz entspricht einer betroffenen Person.</p>
          <p>Hinweis: «Angezeigt» stellt das Hellfeld, also die Anzahl polizeilich registrierter Betroffener dar. «Tatsächlich» zeigt die Anzahl Betroffener, wenn sowohl Hellfeld als auch Dunkelfeld berücksichtigt werden.</p>
          <p>Definitionen: Weitere Infos zu den einzelnen Straftaten findest du im Abschnitt <a href="#section-pks">«Über die Visualisierungen»</a>.</p>
          <p>Quellen: Polizeiliche Kriminalstatistik 2025, Bundesamt für Statistik (Hellfeld). Crime Survey 2022 (Dunkelfeld).</p>
        </template>
        <template v-else>
          <p>Darstellung: Ein Kreuz entspricht einer geschädigten bzw. betroffenen Person.</p>
          <p>Definitionen: Weitere Infos zu den einzelnen Straftaten findest du im Abschnitt <a href="#section-pks">«Über die Visualisierungen»</a>.</p>
          <p>Quelle: Polizeiliche Kriminalstatistik 2025, Bundesamt für Statistik.</p>
        </template>
      </div>
    </div>

  </div>
</template>




<style scoped>
/* =========================
   FILTER-BUTTON (nur Mobile)
   ========================= */

/* Zusätzlicher Fix: Alle Buttons in der Filter-Liste immer eckig */


.filter-btn-mobile {
  position: fixed;
  left: 0px;
  right: 0px;
  bottom: 0px;
  width: auto;
  z-index: 30000;
  background: #000;
  color: #fff;
  border: none;
  padding: 16px 0;
  font-size: 1.1em;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  font-family: inherit;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s, color 0.2s, border 0.2s;
  display: block;
  text-align: center;
}


.filter-btn-mobile:active {
  background: #000;
  color: #fff;
  border-color: #000;
}

/* Dunkelziffer Toggle Mobile */
.dunkelziffer-toggle-mobile {
  display: flex;
  flex-direction: row;
  width: 100vw;
  margin-left: -24px;
  margin-right: -24px;
  border-bottom: 2px solid #000;
  margin-bottom: 0;
}

.dz-toggle-btn {
  flex: 1;
  background: #fff;
  color: #000;
  border: none;
  padding: 12px 0;
  font-size: 1.1em;
  font-family: inherit;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  border-radius: 0 !important;
  text-align: center;
}

.dz-toggle-btn:first-child {
  border-right: 1px solid #000;
}

.dz-toggle-btn.active {
  background: #000;
  color: #fff;
}

/* FilterBottomSheet mobile Filter-Liste */
.filter-sheet-list {
  display: flex;
  flex-direction: column;
  gap: 0px;
  padding: 0px 0 0px 0;
  align-items: stretch;
}


.filter-sheet-btn {
  background: #fff;
  color: #000;
  border: none;
  padding: 10px 0;
  font-size: 1.1em;
  font-family: inherit;
  font-weight: 700;
  text-align: left;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  width: 100vw;
  margin-left: -24px;
  margin-right: -24px;
  border-radius: 0 !important;
  box-sizing: border-box;
  z-index: 30001;
}

.filter-sheet-btn-label {
  display: block;
  padding: 0 24px;
}

.filter-sheet-btn.active {
  background: #000 !important;
  color: #fff;
  box-shadow: none;
  border-radius: 0;
}



.mobile-info-overlay {
  position: fixed;
  inset: 0;
  background: #fff;
  color: #000;
  z-index: 40000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 2.5em 1.2em 1.2em 1.2em;
}

.mobile-info-content {
  max-width: 500px;
  width: 100%;
  padding-top: 5em;
}

.mobile-info-overlay h3 {
  font-size: 1.6em;
  margin-top: 0;
  margin-bottom: 0.7em;
}

.mobile-info-overlay p {
  font-size: 1.1em;
  margin: 0.7em 0;
}

.close-btn {
  position: absolute;
  top: 0.2em;
  right: 0.2em;
  background: none;
  border: none;
  font-size: 2.5em;
  color: #000;
  cursor: pointer;
}



/* =========================
   STICKY NAVIGATION
   ========================= */

.dot-nav {
  position: fixed;
  right: 30px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 20px;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.dot-nav.nav-hidden {
  opacity: 0;
  transform: translateY(-50%) translateX(50px);
  pointer-events: none;
}

.dot-item {
  position: relative;
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  transition: all 0.2s ease;
}

.dot {
  width: 28px;
  height: 5px;
  border-radius: 0;
  background: rgba(0, 0, 0, 1);
  border: none;
  transition: all 0.3s ease;
  position: relative;
}

.dot-item:hover .dot {
  background: rgba(0, 0, 0, 1);
  transform: none;
}

.dot-item.dot-active .dot {
  width: 28px;
  height: 5px;
  background: #000;
  border: none;
}

.dot-item.dot-active .dot::before {
  content: '';
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 5px;
  height: 28px;
  background: #000;
  transition: all 0.3s ease;
}

.dot-label {
  position: absolute;
  right: 45px;
  white-space: nowrap;
  background: rgba(0, 0, 0);
  color: #fff;
  padding: 6px 12px;
  border-radius: 0px;
  opacity: 0;
  transform: translateX(10px);
  transition: all 0.2s ease;
  pointer-events: none;
}

.dot-item:hover .dot-label {
  opacity: 1;
  transform: translateX(0);
}

/* font-weight removed, now global */

/* =========================
   HAMBURGER-MENÜ (nur Mobile)
   ========================= */

.hamburger-menu {
  position: fixed;
  top: 18px;
  right: 18px;
  left: auto;
  z-index: 20000;
  display: block;
}

.hamburger-btn {
  width: 50px;
  height: 50px;
  background: none;
  border: none;
  border-radius: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 36000;
  position: relative;
  padding: 0;
  transition: background 0.7s cubic-bezier(.4, 2, .6, 1), border 0.7s cubic-bezier(.4, 2, .6, 1);
}

.hamburger-btn.open {
  background: transparent;
  border: none;
  box-shadow: none;
}

/* Hamburger offen : nur ein Kreuz (X) anzeigen */
.hamburger-btn.open .hamburger-icon {
  background: transparent;
}

.hamburger-btn.open .hamburger-icon::before {
  background: #fff;
  transform: rotate(45deg) translate(0px, 0px);
  top: 0;
}

.hamburger-btn.open .hamburger-icon::after {
  background: #fff;
  transform: rotate(-45deg) translate(0px, -0px);
  top: 0;
}

.hamburger-icon {
  width: 35px;
  height: 4.2px;
  background: #000;
  position: relative;
  display: block;
  transition: background 0.7s cubic-bezier(.4, 2, .6, 1);

}

.hamburger-icon::before,
.hamburger-icon::after {
  content: '';
  position: absolute;
  left: 0;
  width: 35px;
  height: 4.2px;
  background: #000;
  transition: 0.3s;
}

.hamburger-icon::before {
  top: -12px;
}

.hamburger-icon::after {
  top: 12px;
}

.hamburger-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 1);
  z-index: 35000;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.hamburger-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5em;
  align-items: flex-start;
  justify-content: flex-start;
  height: 100%;
  padding-top: 4.4em;
}

.hamburger-link {
  background: none;
  border: none;
  color: #fff;
  font-size: 2.2em;
  font-family: inherit;
  font-weight: 700;
  cursor: pointer;
  padding: 5px 30px;
  transition: color 0.2s;
  text-align: left;
}

@media (max-width: 768px) {
  .hamburger-link {
    font-size: 1.6em;
    padding: 5px 20px;
  }
}

.hamburger-link:active,
.hamburger-link:focus {
  background: #fff;
  color: #000;
  outline: none;
}


/* --- MOBILE: Dot-Navigation ausblenden, Hamburger kommt später --- */





/* Nächster Schritt: Hamburger-Menü für Mobile ergänzen */

/* =========================
   SCROLL & LAYOUT SYSTEM
   ========================= */

/* Main Scroll Container */
.main-scroll {
  scroll-snap-type: y mandatory;
  overflow-y: auto;
  height: 100vh;
  background: #fff;
  scroll-behavior: smooth;
}

@media (max-width: 768px) {
  #section-dunkelziffer.fullscreen-section {
    padding-left: 0 !important;
    padding-right: 0 !important;
  }
}

/* Scroll Snap Behavior - stark */
.main-scroll>section,
.main-scroll>.fullscreen-section,
.main-scroll>.split-section {
  scroll-snap-align: start;
  scroll-snap-stop: always;
  min-height: 100vh;
}

/* Finale Sektion - reduzierte Höhe */
/* Spezifischer: Nur finale Section innerhalb von .main-scroll */
.main-scroll>.final-text-overlay-section {
  min-height: 100vh;
  padding-bottom: 300px;
  /* Überschreibt die 150vh von oben */
}


/* =========================
   FULLSCREEN SECTIONS (bereinigt)
   ========================= */


/* Spezifischer: Nur fullscreen-section direkt in .main-scroll */
.main-scroll>.fullscreen-section {
  min-height: 350vh;
  /* Erweitert für längeren Text-Overlay */
  position: relative;
  scroll-snap-align: start;
  z-index: 1;
}

/* Nur die Dunkelziffer-Fullscreen-Section kleiner machen, nicht das Titelblatt */
.main-scroll>#section-dunkelziffer.fullscreen-section {
  min-height: 60vh;
}

#section-intro {
  min-height: 100vh;
}

#section-intro .fullscreen-sketch {
  justify-content: flex-start;
  align-items: flex-start;
  padding-left: 60px;
  padding-top: 40px;
}


@media (max-width: 768px) {
  #section-intro .fullscreen-sketch {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding-left: 0;
    padding-top: 0;
    height: 100vh !important;
  }

  .titelblatt-text {
    text-align: left;
    width: fit-content;
    max-width: calc(100vw - 40px);
  }

  #section-intro .fullscreen-sketch h1,
  #section-intro .fullscreen-sketch h2 {
    text-align: left;
    width: fit-content;
    max-width: calc(100vw - 40px);
  }
}

#section-intro .fullscreen-sketch h1 {
  margin-bottom: 20px;
}

#section-intro .fullscreen-sketch h2 {
  margin-top: 0;
}

/*
  !important ist für height: 90vh zwingend notwendig!
  Grund: P5.js-Komponenten, dynamische oder Inline-Styles (z.B. durch Canvas-Frameworks oder Vue) überschreiben sonst die Höhe.
  Ohne !important wird die Höhe von .fullscreen-sketch nicht zuverlässig gesetzt, wodurch die Buttons (z.B. Filterbuttons bei Dunkelziffer) in den Canvas rutschen und das Layout zerreißt.
  Höhere Spezifität reicht nicht aus, da Inline-Styles und Framework-Styles Vorrang haben.
  Nur so bleibt die Section stabil, Sticky-Layout und Buttons funktionieren wie gewünscht.
*/
.fullscreen-sketch {
  width: 100vw;
  height: 90vh !important;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  position: sticky;
  top: 0;
  display: block;
}

#sketch-dunkelziffer {
  position: relative;
  width: 100%;
  height: 90%;
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
  background: #fff;
  color: #000;
  padding: 24px;
  opacity: 0.95;
  z-index: 2;
  border: 3px solid #fff;
  pointer-events: none;
}

.dunkelziffer-title {
  position: absolute;
  top: 30px;
  left: 0;
  right: 0;
  z-index: 1;
  color: #000;
  text-align: center;
  margin: 0;
  pointer-events: none;
}

@media (max-width: 768px) {
  .dunkelziffer-title {
    left: 20px;
    transform: none;
    text-align: left;
  }
}

.dunkelziffer-annotation {
  position: absolute;
  top: 75px;
  left: 18.4%;
  z-index: 1;
  margin: 0;
  pointer-events: none;
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


.split-section {
  min-height: 100vh;
  display: flex;
  flex-direction: row;
  align-items: stretch;
  scroll-snap-align: start;
  background: #fff;
  position: relative;
}

.split-left {
  flex: 1 1 60%;
  display: flex;
  flex-direction: column;
  align-items: left;
  justify-content: left;
  background: #fff;
  margin-left: 60px;
}

.sticky-sketch {
  position: sticky;
  top: 0;
  height: 100vh;
  z-index: 1;
  background: #fff;
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
  background: #fff;
  color: #000;
  padding: 3em;
  position: relative;
}

.side-text {
  margin: auto 0;
  padding: 3em;
  color: #000;
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
BUTTONS
========================= */

/* Wrapper für Filter-Buttons mit Info-Button */
.filter-buttons-with-info {
  display: flex;
  gap: 5px;
  align-items: center;
  flex-wrap: wrap;
  position: relative;
}

/* Sicherstellen, dass alle Buttons in fullscreen-buttons anklickbar bleiben */
.fullscreen-buttons button {
  pointer-events: auto;
}

/* Button-Container in Split-Sections - mehr Abstand vom unteren Rand */
.btns {
  margin-bottom: 60px;
  /* Abstand vom unteren Rand der sticky-Elemente */
  position: relative;
}



/* Info Button absolut positioniert für Overlay-Effekt */
.info-btn-absolute-wrapper {
  position: relative;
  margin-left: 15px;
  display: flex;
  align-items: flex-end;
  /* kein z-index, damit Popup unabhängig ist */
}

.info-btn-absolute-wrapper .info-btn {
  width: 35px;
  height: 35px;
  padding: 0 16px;
  background-color: #fff;
  color: #000;
  border: 2.5px solid #000;
  cursor: pointer;
  border-radius: 0;
  transition: all 0.3s cubic-bezier(.4, 2, .6, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: visible;
  position: relative;
  z-index: 1;
  z-index: 10001;
}

/* Info-Popup für Dunkelziffer wie in Ort-Section, rechtsbündig über dem Button */

.popup-close {
  position: absolute;
  top: 8px;
  right: 8px;
  background: none;
  border: none;
  font-size: 1.8em;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #000;
}


/* =========================
   TEXT OVERLAY SECTIONS
   ========================= */

/* Text Overlay Section - scrollt über vorherige Section mit sanftem Übergang */
.text-overlay-section {
  min-height: 100vh;
  background: none;
  color: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  scroll-snap-align: start;
  scroll-snap-stop: always;
  margin: 0;
  position: relative;
  z-index: 5;
  margin-top: 0;
  padding-top: 0;
}

.text-overlay-section:first-of-type {
  margin-top: 12vh;
}

/* Speziell: Weniger Weißraum vor Dunkelziffer-Text (zweite .text-overlay-section) */
.text-overlay-section:nth-of-type(2) {
  min-height: 60vh;
  margin-top: 18vh;
  padding-top: 0;
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
  /* Gleich wie andere Sektionen */
  background: #fff;
  color: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  scroll-snap-align: start;
  scroll-snap-stop: always;
  /* Auch hier starkes Kleben */
  margin: 0;
  position: relative;
  z-index: 4;
}

/* Forderungen Canvas Container - Vollbild Canvas, zentriert */
.forderungen-canvas-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100vw;
  height: 100vh;
  z-index: 10;
  /* Hoch genug über dem Text */
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  /* Canvas selbst nicht klickbar, damit Button durchklickbar bleibt */
}

/* Canvas innerhalb des Containers soll interaktiv bleiben */
.forderungen-canvas-container canvas {
  pointer-events: auto;
}

/* –––––––––– FORMULAR –––––––––––*/

.kontakt-form {
  margin-top: 28px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  position: relative;
  z-index: 20;
}

.form-row {
  width: 100%;
}

.form-row.two-cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}


.form-field input,
.form-field textarea {
  width: 100%;
  border: 3px solid #000;
  background: transparent;
  color: #000;
  padding: 8px 10px;
  border-radius: 0;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .form-field input,
.form-field textarea {
    border: 2px solid #000;
    padding: 5px 8px;
  }
  .form-field textarea {
    min-height: 70px;
  }
  .kontakt-form {
    gap: 8px;
  }
  .form-field {
    gap: 3px;
  }
  .form-row.two-cols {
    gap: 8px;
  }
}

.form-field textarea {
  resize: vertical;
  min-height: 110px;
}

/* Fehlermeldungen schlicht unter dem Feld */

/* Erfolgsmeldung nach Bestellung */

.checkbox-field {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  width: fit-content;
}

.checkbox-field input[type='checkbox'] {
  width: 18px;
  height: 18px;
  margin: 0;
  background: transparent;
  border-radius: 0;
  border: 3px solid #000;
  appearance: none;
  -webkit-appearance: none;
  outline: none;
  cursor: pointer;
  position: relative;
}

.checkbox-field input[type='checkbox']:checked::after {
  content: '';
  display: block;
  width: 15px;
  height: 15px;
  background: #000;
  position: absolute;
  top: 0px;
  left: 0px;
}

.footer-brava.footer-visible {
  opacity: 1;
  pointer-events: auto;
  animation: footer-fade-in 1.2s cubic-bezier(.4, 2, .6, 1);
}

@media (max-width: 768px) {
  .footer-brava.footer-visible {
    animation: none !important;
    transform: none !important;
    position: static !important;
  }
}

@keyframes footer-fade-in {
  0% {
    opacity: 0;
    transform: translateY(40px);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}




@media (max-width: 768px) {

  /* Alle Sections auf Mobile: volle Breite, keine Splits */
  .split-section,
  .fullscreen-section,
  .text-overlay-section,
  .final-text-overlay-section {
    width: 100vw !important;
    max-width: 100vw !important;
    min-width: 0 !important;
    flex-direction: column !important;
    align-items: stretch !important;
    margin: 0 !important;
    padding: 0 !important;
    border: none !important;
    box-sizing: border-box;
  }

  .split-left,
  .split-right,
  .sticky-sketch {
    width: 100% !important;
    margin: 0 !important;
    padding: 0 0 24px 0 !important;
    min-width: 0 !important;
    box-sizing: border-box;
    position: static !important;
    z-index: auto !important;
    height: auto !important;
    margin-left: 0px !important;

  }

  .btns {
    margin-bottom: 20px !important;
  }


  @media (max-width: 768px) {

    .split-section,
    .fullscreen-section,
    .text-overlay-section,
    .final-text-overlay-section {
      min-height: 100vh !important;
      margin-top: 5em !important;
    }
  }

  @media (max-width: 768px) {
    .text-overlay-content {
      max-width: 100vw !important;
      padding: 0 !important;
    }

  }
}

@media (max-width: 768px) {

  .split-section,
  .fullscreen-section,
  .text-overlay-section,
  .final-text-overlay-section {
    padding-left: 20px !important;
    padding-right: 20px !important;
    box-sizing: border-box;
    flex-direction: column !important;
  }

  .text-overlay-content {
    padding-left: 0 !important;
    padding-right: 0 !important;
  }

  .text-overlay-section,
  .final-text-overlay-section {
    align-items: flex-start !important;
    justify-content: flex-start !important;
    padding-top: 3em !important;
  }

  .split-section,
  .fullscreen-section:not(#section-intro) {
    padding-top: 3em !important;
  }

  .split-left,
  .split-right {
    padding-top: 3em !important;
  }

  .dot-nav {
    display: none !important;
  }

  /* Mobile: split-section selbst kein Snap-Punkt – die Kinder übernehmen das */
  .split-section {
    scroll-snap-align: none !important;
    scroll-snap-stop: normal !important;
    min-height: 0 !important;
    overflow: visible !important;
  }

  /* Sketch-Teil: eigene 100vh Slide */
  .split-left,
  .sticky-sketch {
    height: 100vh !important;
    min-height: 100vh !important;
    scroll-snap-align: start !important;
    scroll-snap-stop: always !important;
    overflow: hidden !important;
  }

  /* Text-Teil: eigene 100vh Slide */
  .split-right {
    height: 100vh !important;
    min-height: 100vh !important;
    scroll-snap-align: start !important;
    scroll-snap-stop: always !important;
    overflow-y: auto !important;
  }

  /* scrollable-text: kein sticky auf Mobile */
  .scrollable-text {
    position: static !important;
    top: auto !important;
    min-height: auto !important;
    height: auto !important;
  }

  /* side-text: kein Padding auf Mobile */
  .side-text {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
  }
}
</style>