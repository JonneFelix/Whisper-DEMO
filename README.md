# Whisper Transcription Demo

Dieses Repository bietet eine einfache Möglichkeit, das OpenAI-Whisper-Modell zu testen und eine benutzerfreundliche Streamlit-Anwendung zu nutzen. Die folgende Anleitung zeigt dir, wie du schnell starten kannst.

## Anleitung

### 1. Repository klonen

Klonen des Repositories in einen bestimmten Ordner:
```bash
# Ersetze <ziel_ordner> mit deinem gewünschten Verzeichnis
git clone https://github.com/JonneFelix/Whisper-DEMO.git <ziel_ordner>
cd <ziel_ordner>
```

### 2. Virtuelle Umgebung erstellen

Erstelle eine virtuelle Umgebung mit dem Namen `whisper_venv`:
```bash
python3 -m venv whisper_venv
```

### 3. Virtuelle Umgebung aktivieren

Aktiviere die virtuelle Umgebung:
```bash
source whisper_venv/bin/activate
```

### 4. Abhängigkeiten installieren

Installiere die erforderlichen Abhängigkeiten:
```bash
pip install -r requirements.txt
```

### 5. Programm starten

#### Test-Skript starten
Führe das Test-Skript aus, um das Whisper-Modell direkt zu testen:
```bash
python3 Test_Alle_Modelle.py
```
- **Funktionalität:** Wähle das gewünschte Modell und eine Audiodatei aus dem Ordner `audio_samples` aus. Die Ergebnisse werden im entsprechenden Unterordner von `Outputs` gespeichert.
- **Benchmark:** Die Datei `Benchmark.csv` dokumentiert alle Transkriptionsergebnisse mit Details zu Zeit und Pfaden.

#### Streamlit-Anwendung starten
Alternativ kannst du die Streamlit-Benutzeroberfläche nutzen:
```bash
streamlit run app.py
```

### 6. Streamlit-Anwendung verwenden

Die Streamlit-Anwendung bietet eine intuitive Oberfläche mit den folgenden Features:

#### **1. Audioquelle auswählen**
Es gibt drei Möglichkeiten, eine Audiodatei auszuwählen:
- **Audio auswählen:** Wähle eine bestehende Audiodatei aus dem Ordner `audio_samples` aus.
- **Audio hochladen:** Lade eine neue Audiodatei direkt in die Anwendung hoch.
- **Audio aufnehmen:** Nimm eine neue Audiodatei direkt über dein Mikrofon auf.

#### **2. Modell auswählen**
Für jede Audioquelle kannst du aus den Modellen `tiny`, `base`, `small`, `medium` und `large` auswählen.

#### **3. Transkription starten**
Mit einem Klick auf den Transkriptions-Button wird die Audiodatei verarbeitet. Der Fortschritt wird live angezeigt, inklusive einer Stoppuhr.

#### **4. Transkriptionen anzeigen**
Nach Abschluss der Transkription kannst du die Ergebnisse im Bereich "Transkriptionen Übersicht" einsehen:
- **Audio abspielen:** Spiele die Original-Audiodatei direkt in der Anwendung ab.
- **Transkript anzeigen:** Klappe den Text mit einem Klick auf den Button aus, um das Transkript zu lesen.
- **Details:** Zeitinformationen und Pfade zur Audiodatei und zum Transkript werden ebenfalls angezeigt.

## Hinweis
- Stelle sicher, dass alle Audiodateien im Ordner `audio_samples` abgelegt sind, wenn du die Test-Skripte nutzt.
- Die Ergebnisse der Transkription werden im entsprechenden Unterordner von `Outputs` gespeichert (`Tiny`, `Base`, etc.).
- Die Datei `Benchmark.csv` dokumentiert alle Transkriptionen.

Viel Erfolg beim Testen und Erkunden der Whisper-Funktionen! 🎉
