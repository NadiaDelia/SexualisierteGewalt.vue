<template>
  <section class="text-overlay-section">
    <div class="text-overlay-content">
      <h2>Das meiste bleibt im Dunkeln.</h2>
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
</template>

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
</style>