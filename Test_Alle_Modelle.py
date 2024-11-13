import os
import time
import whisper
import csv
import uuid
from pathlib import Path

# Define model directories
MODEL_DIRS = {
    "tiny": "Outputs/Tiny",
    "base": "Outputs/Base",
    "small": "Outputs/Small",
    "medium": "Outputs/Medium",
    "large": "Outputs/Large",
}

# Create output directories if they do not exist
for dir_path in MODEL_DIRS.values():
    Path(dir_path).mkdir(parents=True, exist_ok=True)

# Paths
AUDIO_DIR = "audio_samples"
OUTPUT_DIR = "Outputs"
BENCHMARK_FILE = os.path.join(OUTPUT_DIR, "Benchmark.csv")

# Initialize benchmark CSV
if not os.path.exists(BENCHMARK_FILE):
    with open(BENCHMARK_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Original Audio", "Transkript", "Zeit", "Transkript Pfad", "Original Audio Pfad"])

# List available audio files
audio_files = [f for f in os.listdir(AUDIO_DIR) if f.lower().endswith((".mp3", ".wav", ".m4a", ".flac"))]

# Model selection menu
def select_model():
    print("\nVerfügbare Modelle:")
    for idx, model in enumerate(MODEL_DIRS.keys(), start=1):
        print(f"{idx}. {model.capitalize()}")
    
    while True:
        try:
            choice = int(input("\nBitte die Nummer des gewünschten Modells eingeben: ").strip())
            if 1 <= choice <= len(MODEL_DIRS):
                return list(MODEL_DIRS.keys())[choice - 1]
            else:
                print("Ungültige Auswahl. Bitte eine gültige Nummer eingeben.")
        except ValueError:
            print("Ungültige Eingabe. Bitte eine Nummer eingeben.")

# Select model
model_choice = select_model()
print(f"Lade Modell: {model_choice}...")
model = whisper.load_model(model_choice)

# Format time for display and CSV
def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f} Sekunden"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        seconds = seconds % 60
        return f"{minutes} Minuten {seconds:.2f} Sekunden"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        return f"{hours} Stunden {minutes} Minuten {seconds:.2f} Sekunden"

# Process each audio file
for audio_file in audio_files:
    audio_path = os.path.join(AUDIO_DIR, audio_file)
    output_dir = MODEL_DIRS[model_choice]

    print(f"Transkribiere: {audio_file}...")

    # Benchmark timing
    start_time = time.time()
    while True:
        elapsed = time.time() - start_time
        print(f"Verstrichene Zeit: {format_time(elapsed)}", end="\r")
        time.sleep(0.5)
        if elapsed >= 1:  # Exit this loop when transcription starts
            break

    result = model.transcribe(audio_path)
    end_time = time.time()

    # Generate unique identifier
    unique_id = str(uuid.uuid4())[:8]

    # Output file paths
    transcript_filename = f"{Path(audio_file).stem}_{model_choice}_{unique_id}.txt"
    transcript_path = os.path.join(output_dir, transcript_filename)

    # Save transcription
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    # Log to benchmark CSV
    with open(BENCHMARK_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            audio_file,  # Original Audio
            transcript_filename,  # Transkript
            format_time(end_time - start_time),  # Zeit
            transcript_path,  # Transkript Pfad
            audio_path,  # Original Audio Pfad
        ])

    print(f"Transkription abgeschlossen: {transcript_filename}")

print("Alle Audiodateien wurden verarbeitet. Die Ergebnisse sind im Outputs-Ordner.")
