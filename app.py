import streamlit as st
import os
import pandas as pd
import whisper
import time
import uuid
from threading import Thread
from queue import Queue
import tempfile
from datetime import datetime
from scipy.io import wavfile

# Paths
AUDIO_DIR = "audio_samples"
OUTPUT_DIR = "Outputs"
MODEL_OUTPUT_DIRS = {
    "tiny": os.path.join(OUTPUT_DIR, "Tiny"),
    "base": os.path.join(OUTPUT_DIR, "Base"),
    "small": os.path.join(OUTPUT_DIR, "Small"),
    "medium": os.path.join(OUTPUT_DIR, "Medium"),
    "large": os.path.join(OUTPUT_DIR, "Large"),
}
BENCHMARK_FILE = os.path.join(OUTPUT_DIR, "Benchmark.csv")
MODEL_OPTIONS = ["tiny", "base", "small", "medium", "large"]
audio_files = [f for f in os.listdir(AUDIO_DIR) if f.lower().endswith((".mp3", ".wav", ".m4a", ".flac"))]

# Ensure Outputs folder and subfolders exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
for dir_path in MODEL_OUTPUT_DIRS.values():
    os.makedirs(dir_path, exist_ok=True)

# Load Benchmark data
def load_benchmark():
    if os.path.exists(BENCHMARK_FILE):
        return pd.read_csv(BENCHMARK_FILE)
    return pd.DataFrame(columns=["Original Audio", "Transkript", "Zeit", "Transkript Pfad", "Original Audio Pfad"])

# Save Benchmark data
def save_benchmark(data):
    data.to_csv(BENCHMARK_FILE, index=False)

# Format time for display
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

# Transcription function
def transcribe_audio(audio_path, model_choice):
    st.info(f"Starte Transkription mit Modell: {model_choice}")

    timer_placeholder = st.empty()

    def timer():
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            timer_placeholder.metric("Verstrichene Zeit", format_time(elapsed_time))
            time.sleep(1)

    timer_thread = Thread(target=timer, daemon=True)
    timer_thread.start()

    # Load Whisper model
    model = whisper.load_model(model_choice)

    # Transcribe
    transcription_start = time.time()
    result = model.transcribe(audio_path)
    transcription_end = time.time()

    # Stop timer
    timer_placeholder.empty()

    # Determine output directory for the model
    model_output_dir = MODEL_OUTPUT_DIRS[model_choice]

    # Generate unique identifier
    unique_id = str(uuid.uuid4())[:8]

    # Save transcription
    transcript_filename = f"{os.path.splitext(os.path.basename(audio_path))[0]}_{model_choice}_{unique_id}.txt"
    transcript_path = os.path.join(model_output_dir, transcript_filename)
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    # Update Benchmark
    benchmark_data = load_benchmark()
    new_entry = pd.DataFrame({
        "Original Audio": [os.path.basename(audio_path)],
        "Transkript": [transcript_filename],
        "Zeit": [format_time(transcription_end - transcription_start)],
        "Transkript Pfad": [transcript_path],
        "Original Audio Pfad": [audio_path]
    })
    benchmark_data = pd.concat([benchmark_data, new_entry], ignore_index=True)
    save_benchmark(benchmark_data)

    st.success("Transkription abgeschlossen!")
    st.write(f"Transkript gespeichert: {transcript_filename}")

# Streamlit UI
st.header(":red[W]HISPER :red[T]RANSKRIPTION :red[I]NTERFACE")

# Tabs for different audio input methods
tab1, tab2, tab3 = st.tabs(["🔊 Audio Auswählen", "📤 Audio Hochladen", "🎤 Audio direkt aufnehmen"])

with tab1:
    st.header("Audio Datei Auswählen")
    with st.form("audio_auswählen"):
        selected_audio = st.selectbox("Wähle eine Audio-Datei:", options=audio_files, index=None, placeholder="Audio-Datei auswählen")
        selected_model = st.selectbox("Wähle ein Modell:", options=MODEL_OPTIONS, index=None, placeholder="Modell auswählen")
        if st.form_submit_button("Transkription starten"):
            if selected_audio and selected_model:
                audio_path = os.path.join(AUDIO_DIR, selected_audio)
                transcribe_audio(audio_path, selected_model)

with tab2:
    st.header("Audio Hochladen")
    with st.form("audio_hochladen"):
        uploaded_file = st.file_uploader("Lade eine neue Audio-Datei hoch:", type=["mp3", "wav", "m4a", "flac"])
        selected_model = st.selectbox("Wähle ein Modell:", options=MODEL_OPTIONS, index=None, placeholder="Modell auswählen")
        if st.form_submit_button("Transkription starten"):
            if uploaded_file and selected_model:
                uploaded_path = os.path.join(AUDIO_DIR, uploaded_file.name)
                with open(uploaded_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"{uploaded_file.name} hochgeladen.")
                transcribe_audio(uploaded_path, selected_model)

with tab3:
    st.header("Audio direkt aufnehmen")
    with st.form("audio_aufnehmen"):
        audio_value = st.audio_input("Starte die Aufnahme")
        selected_model = st.selectbox("Wähle ein Modell:", options=MODEL_OPTIONS, index=None, placeholder="Modell auswählen")
        if st.form_submit_button("Transkription starten"):
            if audio_value and selected_model:
                # Generate filename
                today_date = datetime.now().strftime("%d_%m_%Y")
                temp_audio_path = os.path.join(AUDIO_DIR, f"temp_audio_{uuid.uuid4().hex[:8]}.wav")

                with open(temp_audio_path, "wb") as f:
                    f.write(audio_value.getvalue())

                # Get duration using scipy
                sample_rate, audio_data = wavfile.read(temp_audio_path)
                audio_duration = len(audio_data) / sample_rate
                minutes = int(audio_duration // 60)
                seconds = int(audio_duration % 60)
                duration_str = f"{minutes}:{seconds:02d}"

                # Rename file with proper duration
                audio_filename = f"Audio_{today_date}_{duration_str}.wav"
                final_audio_path = os.path.join(AUDIO_DIR, audio_filename)
                os.rename(temp_audio_path, final_audio_path)

                st.success(f"Aufgenommene Audio-Datei gespeichert: {final_audio_path}")
                transcribe_audio(final_audio_path, selected_model)

# Divider and Transcription Display
st.divider()
st.header("Transkriptionen Übersicht")
benchmark_data = load_benchmark()
if not benchmark_data.empty:
    for index, row in benchmark_data.iterrows():
        with st.expander(f"{row['Transkript']} - Dauer der Transkription: {row['Zeit']}"):
            st.markdown(f"**Original Audio:** {row['Original Audio']}")
            st.audio(row['Original Audio Pfad'], format="audio/wav")
            with open(row['Transkript Pfad'], "r", encoding="utf-8") as transcript_file:
                st.text_area("Transkript:", transcript_file.read(), height=400)
else:
    st.info("Keine Transkriptionen vorhanden.")
