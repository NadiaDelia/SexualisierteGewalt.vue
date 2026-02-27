<script setup>
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
      form.value = { vorname: '', name: '', email: '', adresse: '', plz: '', ort: '', kommentar: '', newsletter: false };
      triggerCrossesFall();
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
  { id: 'intro', label: 'PKS' },
  { id: 'geschaedigte', label: 'Geschädigte' },
  { id: 'beschuldigte', label: 'Beschuldigte' },
  { id: 'ort', label: 'Ort' },
  { id: 'beziehung', label: 'Beziehung' },
  { id: 'dunkelziffer', label: 'Dunkelziffer' },
  { id: 'forderungen', label: 'Forderungen' }
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
  <!-- Dot Navigation -->
  <nav class="dot-nav" :class="{ 'nav-hidden': !showNav }">
    <button v-for="item in navItems" :key="item.id" class="dot-item"
      :class="{ 'dot-active': activeSection === item.id }" @click="scrollToSection(item.id)" :title="item.label">
      <span class="dot"></span>
      <span class="dot-label">{{ item.label }}</span>
    </button>
  </nav>

  <div class="main-scroll">
    <!-- 1a. Titelbild -->
    <div class="fullscreen-section" id="section-intro">
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
          In <a href="www.nadialanfranchi.ch">fünf Visualisierungen</a> betrachten wir zentrale Delikte Sexualisierter
          Gewalt. Dabei stützen wir uns auf die
          Daten der Kriminalstatistik, welche jeweils die angezeigten Fälle zählt. Zudem wichtig zu wissen: Die
          Statistik registriert nur zwei Geschlechter. Folgende Straftaten stehen im Zentrum:
        </p>
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
      </div>
    </section>

    <!-- 2. Split-Section: Sketch links sticky, rechts scrollt Text hoch -->
    <div class="split-section" id="section-geschaedigte">
      <div id="sketch-geschaedigte" class="split-left sticky-sketch">
        <h2>Wer ist von Sexualisierter Gewalt betroffen?</h2>
        <P5CanvasGeschaedigte :key="activeGeschaedigte + '-' + filteredGeschaedigte.length" :data="filteredGeschaedigte"
          :width="widthGeschaedigte" :height="heightGeschaedigte" :font-family="'PxGroteskPan'" :background="255" />
        <div class="btns">
          <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeGeschaedigte === s.key }"
            @click="activeGeschaedigte = s.key">{{ s.label }}</button>
          <button class="info-btn" @click="showInfoGeschaedigte = !showInfoGeschaedigte">i</button>
        </div>

        <!-- Info Pop-up -->
        <div v-if="showInfoGeschaedigte" class="info-popup">
          <button class="popup-close" @click="showInfoGeschaedigte = false">×</button>
          <h3>Geschädigte Personen</h3>
          <p><strong>Darstellung:</strong> Ein Kreuz entspricht einer geschädigten Person</p>
          <p><strong>Quelle:</strong> Polizeiliche Kriminalstatistik (PKS) 2024, Bundesamt für Statistik</p>
          <p><strong>Kontext:</strong> Die Visualisierung zeigt nur angezeigt Fälle. Die Dunkelziffer liegt deutlich
            höher.</p>
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
    <div class="split-section" id="section-beschuldigte">
      <div class="split-left sticky-sketch" id="sketch-beschuldigte">
        <h2>Wer übt Sexualisierte Gewalt aus?</h2>
        <P5CanvasBeschuldigte :key="activeBeschuldigte + '-' + filteredBeschuldigte.length" :data="filteredBeschuldigte"
          :width="widthBeschuldigte" :height="heightBeschuldigte" :background="255" :font-family="'PxGroteskPan'"
          :show-labels="true" left-field="beschuldigte_f" right-field="beschuldigte_m" left-label="Frauen"
          right-label="Männer" :mouse-radius="150" :repel-radius="80" :attract-power="1.5" />
        <div class="btns">
          <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeBeschuldigte === s.key }"
            @click="activeBeschuldigte = s.key">{{ s.label }}</button>
          <button class="info-btn" @click="showInfoBeschuldigte = !showInfoBeschuldigte">i</button>
        </div>

        <!-- Info Pop-up -->
        <div v-if="showInfoBeschuldigte" class="info-popup">
          <button class="popup-close" @click="showInfoBeschuldigte = false">×</button>
          <h3>Beschuldigte Personen</h3>
          <p><strong>Darstellung:</strong> Ein Kreuz entspricht einer beschuldigten Person</p>
          <p><strong>Quelle:</strong> Polizeiliche Kriminalstatistik (PKS) 2024, Bundesamt für Statistik</p>
          <p><strong>Kontext:</strong> Eine beschuldigte Person ist nicht automatisch schuldig. Es handelt sich um
            Verdachtsfälle.</p>
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
            Vergewaltigung umfasst jegliche Penetration gegen den Willen der betroffenen Person. Ausserdem ist es neu
            auch eine Vergewaltigung, wenn Täter_innen eine Schockzustand ausnutzen.
          </p>
        </div>
        <div style="height: 50vh;"></div>
      </div>
    </div>

    <!-- 4. section ort: Sketch Ort sticky + Text -->
    <div class="split-section" id="section-ort">
      <div class="split-left sticky-sketch" id="sketch-ort">
        <h2>Wo findet Sexualisierte Gewalt statt?</h2>
        <P5CanvasOrt :key="activeOrt + '-' + filteredOrt.length" :data="filteredOrt" :width="widthOrt"
          :height="heightOrt" :background="255" :font-family="'PxGroteskPan'" />
        <div class="btns">
          <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeOrt === s.key }"
            @click="activeOrt = s.key">{{ s.label }}</button>
          <button class="info-btn" @click="showInfoOrt = !showInfoOrt">i</button>
        </div>

        <!-- Info Pop-up -->
        <div v-if="showInfoOrt" class="info-popup">
          <button class="popup-close" @click="showInfoOrt = false">×</button>
          <h3>Tatort</h3>
          <p><strong>Darstellung:</strong> Ein Kreuz entspricht einer Straftat</p>
          <p><strong>Quelle:</strong> Polizeiliche Kriminalstatistik (PKS) 2024, Bundesamt für Statistik</p>
          <p><strong>Kontext:</strong> Als privater Raum gelten ausschliesslich die eigenen vier Wände. Treppenhaus oder
            Waschküche gelten bereits als öffentlich.</p>
        </div>
      </div>

      <div class="split-right">
        <div style="height: 150vh;"></div>
        <div class="side-text scrollable-text">
          <h2>Das Zuhause ist kein sicherer Ort</h2>
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
    <div class="split-section" id="section-beziehung">
      <div class="split-left sticky-sketch" id="sketch-beziehung">
        <h2>Welche Beziehung haben Beschuldigte und Geschädigte?</h2>
        <P5CanvasBeziehung :key="activeBeziehung + '-' + filteredBeziehung.length" :data="filteredBeziehung"
          :width="widthBeziehung" :height="heightBeziehung" :background="255" :font-family="'PxGroteskPan'"
          :mouse-radius="150" :repel-radius="80" :attract-power="1.5" />
        <div class="btns">
          <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeBeziehung === s.key }"
            @click="activeBeziehung = s.key">{{ s.label }}</button>
          <button class="info-btn" @click="showInfoBeziehung = !showInfoBeziehung">i</button>
        </div>

        <!-- Info Pop-up -->
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
        <div style="height: 150vh;"></div>
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
        <div style="height: 50vh;"></div>
      </div>
    </div>

    <!-- 6. section dunkelziffer: Sketch Dunkelziffer fullscreen -->
    <div class="fullscreen-section" id="section-dunkelziffer">
      <div class="fullscreen-sketch" id="sketch-dunkelziffer">
        <h2 class="dunkelziffer-title">Angezeigte vs. tatsächliche Sexualisierte Gewalt</h2>
        <div class="dunkelziffer-canvas-container">
          <P5CanvasDunkelziffer :key="activeDunkelziffer + '-' + filteredDunkelziffer.length"
            :data="filteredDunkelziffer" :width="widthDunkelziffer" :height="heightDunkelziffer"
            :background="'transparent'" :font-family="'PxGroteskPan'" :dunkelziffer="dunkelzifferMode"
            :mouse-radius="80" :repel-radius="100" :attract-power="10" />
        </div>
        <!-- Info-Popup entfernt, nur noch expanding Button -->
        <div style="height: 50vh;"></div>
      </div>
      <div class="btns fullscreen-buttons">
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
            <h3>Dunkelziffer</h3>
            <p><strong>Darstellung:</strong> Ein Kreuz entspricht einer geschädigten Person</p>
            <p><strong>Quellen:</strong> PKS 2024 (Hellfeld), Prävalenzstudien (Dunkelfeld)</p>
            <p><strong>Kontext:</strong> Die Dunkelziffer zeigt, wie viele Straftaten tatsächlich passieren im Vergleich
              zu den angezeigten Fällen. Nur etwa 10% werden angezeigt.</p>
          </div>
        </div>
      </div>
    </div>


    <!-- 7. section dunkelziffer text: Erklärungstext als Overlay/Stacking -->
    <section class="text-overlay-section">
      <div class="text-overlay-content">
        <h2>Das meiste bleibt im Dunkeln</h2>
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

    <!-- 8. Finale Forderungen Section mit P5 Canvas im Vordergrund -->
    <section class="final-text-overlay-section" id="section-forderungen">
      <div class="forderungen-canvas-container">
        <P5CanvasForderungen :width="widthForderungen" :height="heightForderungen" :background="'transparent'"
          :font-family="'PxGroteskPan'" :trigger-fall="triggerFallForderungen" :reset-counter="resetForderungen" />
      </div>
      <div class="text-overlay-content">
        <h2 class="h2-spaced">Wir fordern</h2><br />
        <p>Präventionsarbeit: Beispielsweise in Form von nationalen
          Präventionskampagnen und Arbeit mit Tatpersonen</p>
        <p>Konsequenter Opferschutz: Beispielsweise durch Krisenzentren und
          24h-Beratungsstellen</p>
        <p>Bessere Strafverfolgung: durch eine konsequente und lückenlose
          Umsetzung des neuen Sexualstrafrechts</p>
        <p>Finanzielle Ressourcen: eine professionelle und nachhaltige Umsetzung
          von Massnahmen steht und fällt mit der Finanzierung</p>
        <br />
        <h2>Hilf mit!</h2>
        <p>
          Bestelle jetzt ein Postkarten-Set und schreibe Freund*innen, Politiker*innen und Behörden an.
          Fordere sie auf, Sexualisierte Gewalt konsequent zu bekämpfen. Oder unterstütze unsere Arbeit mit einer
          Spende.
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
              <button type="submit" class="fall-button" style="margin-top:18px; display: block;">
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
  </div>
</template>




<style scoped>
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
  font-family: 'PxGroteskPan', sans-serif;
  font-size: 0.85em;
  font-weight: 500;
  opacity: 0;
  transform: translateX(10px);
  transition: all 0.2s ease;
  pointer-events: none;
}

.dot-item:hover .dot-label {
  opacity: 1;
  transform: translateX(0);
}

.dot-item.dot-active .dot-label {
  font-weight: 700;
}

/* =========================
   SCROLL & LAYOUT SYSTEM
   ========================= */

/* Main Scroll Container */
.main-scroll {
  scroll-snap-type: y mandatory;
  /* Starkes Scroll-Snap wie ursprünglich */
  overflow-y: auto;
  height: 100vh;
  background: #fff;
  /* scroll-behavior entfernt für stärkeres Snap */
}

/* Scroll Snap Behavior - stark */
.main-scroll>section,
.split-section,
.fullscreen-section {
  scroll-snap-align: start;
  scroll-snap-stop: always;
  /* Noch stärkeres Kleben */
  min-height: 150vh;
}

/* Finale Sektion - reduzierte Höhe */
.final-text-overlay-section {
  min-height: 100vh !important;
  /* Überschreibt die 150vh von oben */
}

/* =========================
   FULLSCREEN SECTIONS
   ========================= */

/* Erste Section - gleiche Struktur wie Dunkelziffer, erweitert für Overlay */
.fullscreen-section:first-of-type {
  min-height: 350vh !important;
  /* Erweitert für längeren Text-Overlay */
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
  background: #fff;
  color: #000;
  padding: 24px;
  opacity: 0.95;
  z-index: 2;
  font-size: 1.2em;
  border: 3px solid #fff;
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
   FULLSCREEN SECTIONS
   ========================= */

/* Fullscreen Dunkelziffer Section - erweitert für Text-Overlay */
.fullscreen-section {
  min-height: 350vh !important;
  /* Erweitert für längeren Text-Overlay */
  position: relative;
  scroll-snap-align: start;
  z-index: 1;
}

.fullscreen-sketch {
  width: 100vw !important;
  height: 90vh !important;
  margin: 0 !important;
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

.dunkelziffer-title {
  position: absolute;
  top: 30px;
  left: 50%;
  transform: translateX(-68%);
  z-index: 1;
  color: #000;
  text-align: left;
  margin: 0;
  pointer-events: none;
}

.dunkelziffer-annotation {
  position: absolute;
  top: 75px;
  left: 18.4%;
  z-index: 1;
  color: #000;
  ;
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
  font-family: 'PxGroteskPan', sans-serif;
  font-weight: bold;
  font-size: 1em;
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

/* Text Overlay Section - scrollt über vorherige Section mit sanftem Übergang */
.text-overlay-section {
  min-height: 250vh;
  /* Mehr Höhe für besseres Snap-Verhalten und mehr Weißraum */
  background: linear-gradient(to bottom,
      transparent 0%,
      rgba(255, 255, 255, 0.3) 8%,
      rgba(255, 255, 255, 0.7) 20%,
      rgba(255, 255, 255, 0.9) 28%,
      #fff 35%,
      #fff 100%);
  color: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  scroll-snap-align: start;
  margin: 0;
  position: relative;
  z-index: 5;
  margin-top: -100vh;
  padding-top: 50vh;
  /* Mehr Weißraum vor dem Text */
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

.form-field label {
  font-size: 1rem;
}

.form-field input,
.form-field textarea {
  width: 100%;
  border: 3px solid #000;
  background: transparent;
  color: #000;
  padding: 8px 10px;
  font-family: 'PxGroteskPan', sans-serif;
  font-size: 1.4rem;
  border-radius: 0;
  box-sizing: border-box;
}

.form-field textarea {
  resize: vertical;
  min-height: 110px;
}

/* Fehlermeldungen schlicht unter dem Feld */
.form-error {
  color: #000 !important;
  font-size: 1em !important;
  margin-top: 4px !important;
  margin-bottom: 0 !important;
  padding: 0 !important;
  display: block !important;
  text-align: left !important;
  background: none !important;
  border: none !important;
  box-shadow: none !important;
  position: static !important;
  z-index: auto !important;
}

/* Erfolgsmeldung nach Bestellung */
.bestellung-success-message {
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  font-size: 2.2em;
  font-weight: bold;
  color: #000;
  background: none;
  padding: 0px 0;
  margin-top: 60px;
  border-radius: 0;
}

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

@media (max-width: 768px) {
  .form-row.two-cols {
    grid-template-columns: 1fr;
  }
}

/* Verhindert das Springen nach dem Absenden des Formulars */
.bestellung-form-success-wrapper {
  min-height: 580px;
  position: relative;
}

/* Fall Button für Bestell-Formular */
.fall-button {
  margin-top: 30px;
  padding: 12px 24px;
  background-color: #fff;
  color: #000;
  border: 3px solid #000;
  font-family: 'PxGroteskPan', sans-serif;
  font-weight: bold;
  font-size: 1.4em;
  cursor: pointer;
  border-radius: 0;
  transition: all 0.3s ease;
  position: relative;
  z-index: 20;
  /* Höher als Canvas, damit Button klickbar bleibt */
  pointer-events: auto;
}



.fall-button:hover {
  background-color: #000;
  color: #fff;
}

.fall-button.submitted {
  background-color: #fff;
  color: #000;
}
</style>