<template>
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
</template>

<script setup>
import { ref } from 'vue'

// Accordion-State
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
</script>

<style scoped>
/* Text Overlay Section */
.text-overlay-section {
  min-height: 250vh;
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
}

.text-overlay-content {
  max-width: 800px;
  padding: 60px;
  text-align: left;
}

.text-overlay-content h2 {
  margin-bottom: 3px;
}

.h2-spaced {
  margin-top: 2em !important;
}

/* Accordion Styles */
.accordion-list {
  margin: 1em 0;
}

.accordion-item {
  border-bottom: 1px solid #eee;
  margin-bottom: 0.5em;
}

.accordion-header {
  display: flex;
  align-items: center;
  padding: 1em 0;
  cursor: pointer;
  font-weight: bold;
  font-size: 1.1em;
}

.accordion-icon {
  margin-right: 0.8em;
  font-weight: bold;
  transition: transform 0.3s ease;
  width: 1.2em;
  text-align: center;
}

.accordion-icon.open {
  transform: rotate(45deg);
}

.accordion-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
  padding-left: 2em;
}

.accordion-content.open {
  max-height: 200px;
  padding-bottom: 1em;
}

.accordion-content p {
  margin: 0;
  font-size: 0.95em;
  line-height: 1.5;
}
</style>