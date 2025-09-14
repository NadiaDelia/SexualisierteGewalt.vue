# Sexualised Violence in Switzerland

**Data Visualization Project**  
*Bern Academy of the Arts – Generative Data Design*

This project visualizes the incidence of sexualised violence in Switzerland using official statistics and explores interaction-driven forms of data representation.

---

## Project Description

The visualizations focus on five key offences and show who the victims and perpetrators are by gender, place, and relationship. The project also addresses unreported cases (the "dark figure"). Particle systems and mouse interaction are used to move beyond conventional bar charts and present sensitive data with care.

---

## Purpose & Goals

- Visualize official crime data using generative, non-traditional techniques  
- Work with data from the Swiss Federal Statistical Office (SFSO)  
- Use particle systems and interactive behaviors to represent individuals and incidents  
- Explore visual metaphors of covering and exposing  
- Embed the visualizations in a contextual mini-website  
- Integrate p5.js, D3.js, and Vue.js

---

## Data Sources & Structure

### 1) Official Crime Statistics – sexualised Violence

- **Source**: Police Crime Statistics, Swiss Federal Statistical Office  
  <https://www.bfs.admin.ch/bfs/en/home/statistics/crime-criminal-justice/police/sexualised-violence.html>
- **File**: `data_sg.csv`  
- **Time Period**: Data from 2024, published March 2025  
- **Scope**: Officially registered sexualised-violence crimes in Switzerland  
- **Filtered offences**:
  - Sexual abuse and indecent assault (Art. 189)
  - Rape (Art. 190)
  - Abuse of persons incapable of judgment or resistance (Art. 191)
  - Indecent conduct (Art. 194)
  - Sexual harassment (Art. 198)

### 2) Dark Figure (Unreported Cases)

- **Source**: Crime Survey by Dirk Baier and Nora Markwalder, commissioned by the Conference of Cantonal Police Commanders of Switzerland  
  PDF: <https://www.unisg.ch/fileadmin/user_upload/HSG_ROOT/_Kernauftritt_HSG/Universitaet/Crime_Survey_2022_Hauptbericht.pdf>
- **File**: `data_sg.csv`  
- **Time Period**: Survey 2021, published 2022  
- **Scope**: Nationally representative survey on crime prevalence  
- **Note**: Dark-figure values available for all listed offences except Art. 191.

### Data Structure (example fields)

```json
{
  "straftat": "sexuelle_noetigung",
  "anzeigerate": 12.4,
  "geschaedigte_total": 732,
  "geschaedigte_f": 613,
  "geschaedigte_m": 119,
  "geschaedigte_f_dz": 4944,
  "geschaedigte_m_dz": 960,
  "beschuldigte_total": 595,
  "beschuldigte_m": 572,
  "beschuldigte_f": 23,
  "ort_rate_privat": 0.5114,
  "ort_rate_oeffentlich": 0.4886,
  "beziehung_partner_rate": 0.21,
  "beziehung_bekannt_rate": 0.31
}
```

## How It Works

Raw CSV data is transformed into animated visualizations using physics-inspired particle systems. Each particle represents an individual or incident and responds to user input (attraction and repulsion) to reveal patterns and context.

### Visualization Components

- **Title Animation** (`P5CanvasTitelblatt`) — Ambient intro animation for the landing page
- **Victims by Gender** (`P5CanvasGeschaedigte`) — Split-screen view of female/male victims  
- **Perpetrators by Gender** (`P5CanvasBeschuldigte`) — Split-screen view of female/male perpetrators  
- **Location of Incidents** (`P5CanvasOrt`) — Private vs. public, with gender filter  
- **Relationship Context** (`P5CanvasBeziehung`) — 3x2 grid of victim–perpetrator relationships for reported victims
- **Dark Figure (Unreported Cases)** (`P5CanvasDunkelziffer`) — Reported vs. estimated victims (dark figure)

---

## Technologies

- **p5.js** — Particle animation and interaction  
- **D3.js** — CSV parsing  
- **Vue.js** — Component-driven app structure  
- **HTML/CSS** — Semantic structure and styling

---

## Setup and Installation

### Prerequisites

- Node.js v16 or newer  
- npm or yarn  
- VS Code (recommended) with Vue Language Features extension

### Installation Steps
1. **Clone the repository to your local machine:**
```bash
   git clone https://github.com/NadiaDelia/SexualisierteGewalt.vue.git
   cd SexualisierteGewalt.vue
```
2. Open the project folder in VS Code
3. Install the Vue extension (recommended for syntax highlighting and IntelliSense)
4. Install dependencies in Terminal:
```bash
npm install
```
5. Start development server in Terminal:
```bash
npm run dev
```
Open in browser: Navigate to http://localhost:5173 (or the port shown in terminal)

### Build for Production
```bash
npm run build
```
The built files will be in the dist/ directory, ready for deployment.

**Project Structure**
src/
├── components/           # P5.js visualization components
│   ├── P5CanvasGeschaedigte.vue    # Victim statistics
│   ├── P5CanvasBeschuldigte.vue    # Perpetrator statistics
│   ├── P5CanvasOrt.vue             # Location analysis
│   ├── P5CanvasBeziehung.vue       # Relationship context
│   ├── P5CanvasDunkelziffer.vue    # Dark figure estimation
│   └── P5CanvasTitelblatt.vue      # Title animation
├── assets/
│   └── data_sg.csv       # Source data
├── App.vue               # Main application component
└── main.js              # Application entry point

---

## Live Demo
View the live visualization at: [Coming Soon]

---

## Project Status
Status: In Development
Last Updated: September 2025
Version: 1.0
