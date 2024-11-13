# Whisper Transcription Demo

Dieses Repository bietet eine einfache Möglichkeit, das OpenAI-Whisper-Modell zu testen. Die folgende Anleitung zeigt dir, wie du schnell starten kannst.

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

Führe das Programm aus:
```bash
python3 Test_Alle_Modelle.py
```

## Hinweis
- Stelle sicher, dass alle Audiodateien im Ordner `audio_samples` abgelegt sind.
- Die Ergebnisse der Transkription werden im Ordner `Outputs` gespeichert.
- Eine Datei `Benchmark.csv` wird automatisch erstellt, um die Ergebnisse zu protokollieren.

Viel Erfolg beim Testen des Whisper-Modells! 🎉

