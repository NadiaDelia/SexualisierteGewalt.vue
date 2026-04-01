#!/usr/bin/env python3
"""Fix z-index stacking for Dunkelziffer filter buttons vs canvas."""

with open('src/views/SexualDelikte.vue', 'r') as f:
    content = f.read()

# === 1. Template: restructure buttons to separate info btn from filter btns ===
old_tmpl = '''      <div class="btns fullscreen-buttons" v-if="!showHamburger">
        <div class="filter-buttons-with-info">
          <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeDunkelziffer === s.key }"
            @click="activeDunkelziffer = s.key" v-html="s.htmlLabel ?? s.label"></button>
        </div>
        <div class="dunkelziffer-toggle-container">
          <button :class="[\'toggle-btn\', { \'active-dunkelziffer\': dunkelzifferMode === \'hell\' }]"
            @click="dunkelzifferMode = \'hell\'">Angezeigt</button>
          <button :class="[\'toggle-btn\', { \'active-dunkelziffer\': dunkelzifferMode === \'dunkel\' }]"
            @click="dunkelzifferMode = \'dunkel\'">Tatsächlich</button>
        </div>
        <div class="info-btn-absolute-wrapper">
          <button ref="dunkelzifferInfoBtnEl" class="info-btn" @click="toggleDunkelzifferInfo()">i</button>
          <div v-if="showInfoDunkelziffer && !showHamburger" class="info-popup info-popup-dunkelziffer">
            <button class="popup-close" @click="showInfoDunkelziffer = false">×</button>
            <h3>Anmerkungen</h3>
            <p>Darstellung: Ein Kreuz entspricht einer betroffenen Person.</p>
            <p>Hinweis: «Angezeigt» stellt das Hellfeld, also die Anzahl polizeilich registrierter Betroffener dar.
              «Tatsächlich» zeigt die Anzahl Betroffener, wenn sowohl Hellfeld als auch Dunkelfeld berücksichtigt
              werden.</p>
            <p>Definitionen: Weitere Infos zu den einzelnen Straftaten findest du im Abschnitt <a href="#section-pks">«Über
                die Visualisierungen»</a>.</p>
            <p>Quellen: Polizeiliche Kriminalstatistik 2025, Bundesamt für Statistik (Hellfeld). Crime Survey 2022 –
              Studie im Auftrag der Konferenz der Kantonalen Polizeikommandanten (Dunkelfeld).</p>
          </div>
        </div>
      </div>'''

new_tmpl = '''      <div class="dunkelziffer-controls-row" v-if="!showHamburger">
        <div class="btns fullscreen-buttons">
          <div class="filter-buttons-with-info">
            <button v-for="s in STRAFTATEN" :key="s.key" :class="{ active: activeDunkelziffer === s.key }"
              @click="activeDunkelziffer = s.key" v-html="s.htmlLabel ?? s.label"></button>
          </div>
          <div class="dunkelziffer-toggle-container">
            <button :class="[\'toggle-btn\', { \'active-dunkelziffer\': dunkelzifferMode === \'hell\' }]"
              @click="dunkelzifferMode = \'hell\'">Angezeigt</button>
            <button :class="[\'toggle-btn\', { \'active-dunkelziffer\': dunkelzifferMode === \'dunkel\' }]"
              @click="dunkelzifferMode = \'dunkel\'">Tatsächlich</button>
          </div>
        </div>
        <div class="dunkelziffer-info-cell">
          <div class="info-btn-absolute-wrapper">
            <button ref="dunkelzifferInfoBtnEl" class="info-btn" @click="toggleDunkelzifferInfo()">i</button>
            <div v-if="showInfoDunkelziffer && !showHamburger" class="info-popup info-popup-dunkelziffer">
              <button class="popup-close" @click="showInfoDunkelziffer = false">×</button>
              <h3>Anmerkungen</h3>
              <p>Darstellung: Ein Kreuz entspricht einer betroffenen Person.</p>
              <p>Hinweis: «Angezeigt» stellt das Hellfeld, also die Anzahl polizeilich registrierter Betroffener dar.
                «Tatsächlich» zeigt die Anzahl Betroffener, wenn sowohl Hellfeld als auch Dunkelfeld berücksichtigt
                werden.</p>
              <p>Definitionen: Weitere Infos zu den einzelnen Straftaten findest du im Abschnitt <a href="#section-pks">«Über
                  die Visualisierungen»</a>.</p>
              <p>Quellen: Polizeiliche Kriminalstatistik 2025, Bundesamt für Statistik (Hellfeld). Crime Survey 2022 –
                Studie im Auftrag der Konferenz der Kantonalen Polizeikommandanten (Dunkelfeld).</p>
            </div>
          </div>
        </div>
      </div>'''

if old_tmpl in content:
    content = content.replace(old_tmpl, new_tmpl, 1)
    print('OK: Template restructured')
else:
    print('FAIL: Template old string not found')

# === 2. CSS: change .btns.fullscreen-buttons z-index from 20 to 5 ===
old_css1 = '''/* Dunkelziffer-Buttons: z-index über dem Canvas (z-index:15), damit Info-Popup sichtbar ist.
   Canvas hat pointer-events: none → Buttons bleiben klickbar trotz visuellem Überlapp. */
.btns.fullscreen-buttons {
  position: relative;
  justify-content: center;
  z-index: 20;
}'''

new_css1 = '''/* Dunkelziffer-Controls-Row: kein z-index am Wrapper (kein Stacking-Context), damit
   Filter-Buttons (z-index:5) visually UNTER dem Canvas (z-index:15) bleiben,
   und Info-Zelle (z-index:25) ÜBER dem Canvas erscheint. */
.btns.fullscreen-buttons {
  position: relative;
  justify-content: center;
  z-index: 5;
  /* unter Canvas (z-index:15) – Kreuze erscheinen vor Buttons */
}

/* Dunkelziffer: Wrapper ohne z-index (kein eigener Stacking-Context) */
.dunkelziffer-controls-row {
  display: flex;
  flex-direction: row;
  align-items: stretch;
  justify-content: center;
  flex-wrap: wrap;
  gap: 30px;
  margin: 20px 0;
  width: 100%;
  pointer-events: auto;
}

/* Btns inside wrapper: width auto (not full width) */
.dunkelziffer-controls-row > .btns.fullscreen-buttons {
  width: auto !important;
  flex: 0 1 auto;
  margin: 0 !important;
}

/* Info-Zelle: hoher z-index damit i-Button und Popup ÜBER Canvas erscheinen */
.dunkelziffer-info-cell {
  position: relative;
  z-index: 25;
  display: flex;
  align-items: stretch;
  pointer-events: auto;
}'''

if old_css1 in content:
    content = content.replace(old_css1, new_css1, 1)
    print('OK: CSS .btns.fullscreen-buttons updated + new classes added')
else:
    print('FAIL: CSS old string not found')
    idx = content.find('.btns.fullscreen-buttons')
    print(repr(content[idx-100:idx+200]))

# === 3. CSS: update small desktop media query ===
old_css2 = '''  /* 8. Dunkelziffer: Buttons sticky am unteren Rand, ÜBER Canvas-Kreuzen (z-index > 15) */
  /* Canvas hat pointer-events:none → Buttons bleiben klickbar */
  .btns.fullscreen-buttons {
    position: sticky;
    bottom: 0;
    z-index: 20;
    background: #fff;
    padding: 8px 20px;
    gap: 12px !important;
    justify-content: center !important;
    flex-wrap: wrap;
  }'''

new_css2 = '''  /* 8. Dunkelziffer: Controls-Row sticky am unteren Rand mit weissem Hintergrund */
  /* Canvas hat pointer-events:none → Buttons bleiben klickbar */
  .dunkelziffer-controls-row {
    position: sticky;
    bottom: 0;
    z-index: 20;
    background: #fff;
    padding: 8px 20px;
    gap: 12px !important;
    justify-content: center !important;
    flex-wrap: wrap;
    margin: 0 !important;
  }
  .dunkelziffer-controls-row > .btns.fullscreen-buttons {
    position: static !important;
    background: none !important;
    padding: 0 !important;
    margin: 0 !important;
    width: auto !important;
    flex: 0 1 auto;
  }'''

if old_css2 in content:
    content = content.replace(old_css2, new_css2, 1)
    print('OK: Small desktop media query updated')
else:
    print('FAIL: Small desktop media query old string not found')
    idx = content.find('fullscreen-buttons')
    while idx >= 0:
        snippet = content[idx-50:idx+100]
        if 'sticky' in snippet:
            print(repr(snippet))
        idx = content.find('fullscreen-buttons', idx+1)

with open('src/views/SexualDelikte.vue', 'w') as f:
    f.write(content)

print('DONE: File written.')
