# Sexualized Violence in Switzerland

**Data Visualisation Project**: This repository is the result of the continuous training course Generative Data Design at the Bern Academy of the Arts. It shows the incidence of Sexual Violence in Switzerland based on official statistics.

## Project Description

This project visualizes sexual violence in Switzerland based on five of the crucial offences. It shows who is victim an perpetrator of violence focusing on gender, place and relationship. Furthermore it targets the topic of dark figures. The visualisations use particle systems and mouse interactions and are embedded in a mini website giving necessary context information.

## Purpose & Goal

This project explores inusual ways of visualising violence data – beyond conventional bar charts:
- Working with official data from the police crime statistics of the Swiss Federal Statistical Office
- Using particle systems and mouse interaction for data visualization
- Exploring visual metaphors of covering and exposing
- Contextualising the single visualisations in a mini website
- Integrating multiple web technologies (p5.js, d3.js, vue)

## Data Sources & Information

### Data on registered crimes on Sexual Violence
- **Source**: Police Crime Statistics, Swiss Federal Statistical Office (https://www.bfs.admin.ch/bfs/en/home/statistics/crime-criminal-justice/police/sexualised-violence.html) 
- **File**: `data_sg.csv`
- **Time Period**: Data collection from 2024, published in March 2025
- **Coverage**: Officially registered crimes on Sexual Violence in Switzerland
- **Usage**: Filtered to show the following crimes: Sexual abuse and indecent assault (Art. 189), rape (Art. 190), abuse of persons incapable of proper judgement or resistanceindecent conduct (Art. 191), indecent conduct (Art. 194) sexual harassment (Art. 198), 


### Dark figure
- **Source**: Crime Survey by Dirk Baier and Nora Markwalder commissioned by the Conference of Cantonal Police Commanders of Switzerland (https://www.unisg.ch/fileadmin/user_upload/HSG_ROOT/_Kernauftritt_HSG/Universitaet/Crime_Survey_2022_Hauptbericht.pdf)
- **File**: `data_sg.csv` 
- **Time Period**: Data collection 2021, publication 2022 
- **Coverage**: National representative survey on prevalence of crime in Switzerland
- **Usage**: Filtered to show dark figures for sexual abuse and indecent assault,  rape, indecent conduct, sexual harassment (dark figure for Abuse of persons incapable of proper judgement or resistance not available)

### Data Structure
Each crime of the five entries contains:
```anzeigerate
: 
12.4
beschuldigte_f
: 
23
beschuldigte_m
: 
572
beschuldigte_total
: 
595
beziehung_andere
: 
106
beziehung_andere_rate
: 
0.14
beziehung_arbeit
: 
30
beziehung_arbeit_rate
: 
0.04
beziehung_bekannt
: 
227
beziehung_bekannt_rate
: 
0.31
beziehung_keine
: 
158
beziehung_keine_rate
: 
0.22
beziehung_partner
: 
151
beziehung_partner_rate
: 
0.21
beziehung_verwandt
: 
60
beziehung_verwandt_rate
: 
0.08
dunkelziffer
: 
87.6
geschaedigte_f
: 
613
geschaedigte_f_dz
: 
4944
geschaedigte_m
: 
119
geschaedigte_m_dz
: 
960
geschaedigte_total
: 
732
ort_oeffentlich_f
: 
300
ort_oeffentlich_m
: 
58
ort_oeffentlich_total
: 
358
ort_privat_f
: 
313
ort_privat_m
: 
61
ort_privat_total
: 
374
ort_rate_oeffentlich
: 
0.4886
ort_rate_privat
: 
0.5114
straftat
: 
"sexuelle_noetigung"
```

## How It Works

This project visualizes sexual violence statistics through interactive particle animations. Each dataset is represented by animated crosses (particles) that respond to mouse interactions, creating an engaging way to explore sensitive data.

**Core Concept**
- CSV data is parsed and converted into animated particles
- Each particle represents a data point (victim, perpetrator, location, etc.)
- Particles use physics-based interactions (attraction, repulsion) for mouse responsiveness
- Real-time animations show data loading and filtering effects

**Visualization Components**
- Victims by Gender (P5CanvasGeschaedigte) - Split-screen showing male/female victims
- Perpetrators by Gender (P5CanvasBeschuldigte) - Split-screen showing male/female perpetrators 
- Location Analysis (P5CanvasOrt) - Private vs. public incidents with gender filtering
- Relationship Context (P5CanvasBeziehung) - 3x2 grid showing perpetrator-victim relationships
- Dark Figure Estimation (P5CanvasDunkelziffer) - Unreported cases visualization
- Title Animation (P5CanvasTitelblatt) - Static particle animation for landing page

## Technologies Used

- **p5.js**: Canvas rendering and particle system animation
- **d3.js**: Geographic projections and spatial data structures
- **vue.js**
- **CSV parsing**: Direct data import and processing
- **CSS**: Responsive styling and typography
- **HTML**: Structure and semantic markup

## Setup & Installation

### Prerequisites
- Node.js (version 16 or higher)
- npm or yarn package manager

### Installation Steps
1. Clone the repository to your local machine:
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
6. Open in browser: Navigate to http://localhost:5173 (or the port shown in terminal)



### Prerequisites
- VS Code with the p5.vscode extension (which includes Live Server)

### Running the Project
1. Clone this repository to your local machine
2. Open the project folder in VS Code
3. Install the p5.vscode extension if not already installed
4. Click "Go Live" button in the VS Code status bar
5. The project will open in your browser at `http://localhost:5500`

## Live Demo

View the live visualization at: [xxx.www.www]

## Project Status

**Status**: not completed
**Last Updated**: September 2025  
**Version**: 1.0

---
