<?php
// save_form.php
// Speichert Formulardaten als CSV auf dem Server

// Nur POST zulassen
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo 'Method Not Allowed';
    exit;
}

// Felder auslesen und bereinigen
$fields = [
    'vorname', 'name', 'adresse', 'adresszusatz', 'plz', 'ort', 'kommentar', 'newsletter'
];
$data = [];
foreach ($fields as $field) {
    $data[] = isset($_POST[$field]) ? str_replace(["\r","\n",";"], ' ', trim($_POST[$field])) : '';
}

// CSV-Datei Pfad (im gleichen Verzeichnis, ggf. anpassen)

$file = __DIR__ . '/bestellungen.csv';

// Datei anlegen, falls nicht vorhanden, und Header schreiben
if (!file_exists($file)) {
    file_put_contents($file, "Vorname;Name;Adresse;Adresszusatz;PLZ;Ort;Kommentar;Newsletter\n");
}

// Daten als neue Zeile anhängen
$line = implode(';', array_map(function($v) {
    return '"' . str_replace('"', '""', $v) . '"';
}, $data)) . "\n";
file_put_contents($file, $line, FILE_APPEND);

// Erfolgsmeldung
header('Content-Type: application/json');
echo json_encode(['success' => true]);
