# 🏷️ OpenSCAD Nametag Generator

Automatische Generierung von 3D-druckbaren Namensschildern mit erhabenem Text, elegantem Ring-Design und runder Befestigungsseite.

## Features

- 🎨 **Erhöhter Text** - Name steht aus der Oberfläche heraus
- 💍 **Erhabener Ring** - Eleganter Randring um das Design
- ⭕ **Runde Seite** - Halbkreis-Ende mit zentralem Befestigungsloch
- ⚡ **Batch-Generierung** - Hunderte Namensschilder mit einem Befehl
- 📊 **CSV-Import** - Namen und Parameter aus CSV-Dateien

---

## Installation

### 1. Python 3.6+

**Prüfen:**
```bash
python --version
```

**Installation falls nötig:**
- **Windows/macOS**: [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt install python3`

### 2. OpenSCAD

**Windows:**
- Download: [openscad.org/downloads. html](https://openscad. org/downloads.html)
- Installer ausführen (Standard-Pfad: `C:\Program Files\OpenSCAD\`)

**macOS:**
```bash
brew install openscad
```

**Linux:**
```bash
sudo apt-get install openscad
```

---

## Schnellstart

### Einzelnes Namensschild

1.  Öffne `nametag.scad` in OpenSCAD
2.  Ändere `name = "YOUR NAME";` zu deinem Namen
3. Drücke **F5** für Vorschau, **F6** zum Rendern
4. Exportiere: **File → Export → Export as STL**

### Batch-Generierung

1. Erstelle `names.csv`:
   ```csv
   name
   Max Mustermann
   Anna Schmidt
   Peter Müller
   ```

2. Führe aus:
   ```bash
   python generate_nametags.py
   ```

3. Finde STL-Dateien in `generated_nametags/`

---

## Verwendung

### Parameter anpassen

Bearbeite den Anfang von `nametag.scad`:

```scad
name = "Dein Name";           // Name auf dem Schild
nametag_width = 80;            // Breite in mm
nametag_height = 30;           // Höhe in mm
nametag_thickness = 3;         // Basis-Dicke in mm
text_size = 8;                 // Schriftgröße
text_height = 1.5;             // Text-Höhe über Ring
ring_width = 3;                // Ring-Breite in mm
ring_height = 1.2;             // Ring-Höhe in mm
mounting_hole_diameter = 4;    // Loch-Durchmesser in mm
corner_radius = 3;             // Ecken-Radius in mm
```

### Empfohlene Kombinationen

**Standard:**
```scad
nametag_width = 80; nametag_height = 30; text_size = 8;
```

**Groß (lange Namen):**
```scad
nametag_width = 110; nametag_height = 35; text_size = 10;
```

**Klein (kompakt):**
```scad
nametag_width = 70; nametag_height = 25; text_size = 7;
```

---

## CSV-Format

### Einfach (nur Namen)

```csv
name
Alice Johnson
Bob Smith
Charlie Brown
```

### Erweitert (mit Parametern)

```csv
name,nametag_width,nametag_height,text_size,ring_width,ring_height
Max Mustermann,100,35,10,4,1.5
Anna Schmidt,80,30,8,3,1.2
Peter Müller,90,32,9,3. 5,1.3
```

### Verfügbare Spalten

| Spalte | Pflicht | Standard | Beschreibung |
|--------|---------|----------|--------------|
| `name` | ✅ | - | Name auf dem Schild |
| `nametag_width` | ❌ | 80 | Breite in mm |
| `nametag_height` | ❌ | 30 | Höhe in mm |
| `nametag_thickness` | ❌ | 3 | Basis-Dicke in mm |
| `text_size` | ❌ | 8 | Schriftgröße |
| `text_height` | ❌ | 1.5 | Text-Höhe in mm |
| `ring_width` | ❌ | 3 | Ring-Breite in mm |
| `ring_height` | ❌ | 1.2 | Ring-Höhe in mm |
| `mounting_hole_diameter` | ❌ | 4 | Loch-Durchmesser in mm |
| `corner_radius` | ❌ | 3 | Ecken-Radius in mm |

**Hinweis:** Fehlende oder leere Spalten verwenden automatisch die Standardwerte.

---

## 3D-Druck

### Empfohlene Einstellungen

```
Schichthöhe: 0.15-0.2mm
Infill: 25-30%
Support: Nicht erforderlich
Orientierung: Flach, Text nach oben
Material: PLA, PETG oder ABS
```

### Orientierung

**✅ RICHTIG:**
```
     ╔═══════════╗
     ║   NAME    ║
─────╚═══════════╝────── ← Druckbett
```

---

## Troubleshooting

### "OpenSCAD not found"

```bash
# Windows
"C:\Program Files\OpenSCAD\openscad.exe" --version

# macOS/Linux
openscad --version
```

Falls nicht gefunden: Installiere OpenSCAD und stelle sicher, dass es im PATH ist.

### "CSV file not found"

Erstelle `names.csv` im gleichen Ordner wie das Script:
```bash
echo "name" > names.csv
echo "Test Name" >> names.csv
```

### STL-Datei kann nicht geöffnet werden

- Öffne die `. scad` Datei in OpenSCAD und prüfe auf Fehler
- Rendere manuell mit F6
- Prüfe Parameter-Kombinationen

---

## Beispiel

**CSV für Event mit 50 Teilnehmern:**
```csv
name,text_size
Dr. Sarah Johnson,8
Michael Chen,9
Prof.  Anna Müller,7
María García,9
```

**Ausführen:**
```bash
python generate_nametags.py
```

**Ergebnis:** 50 personalisierte STL-Dateien in ~5 Minuten

---

## Lizenz

Frei verwendbar für persönliche und kommerzielle Projekte. 

---

*Happy Printing!  🖨️✨*

## Mehr Projekte und Anleitungen findest du [hier](https://wiki.mint-labs.de/)
