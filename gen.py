import wave
import numpy as np
import os

# Constants
SAMPLE_RATE = 44100  # Samples per second
DURATION = 0.40463   # Duration of each note in seconds
VOLUME = 0.5         # Volume (0.0 to 1.0)
FADE_DURATION = 0.1  # Fade-out duration in seconds

# Note frequencies for C3 to B5
NOTE_FREQUENCIES = {
    "C3": 130.81, "Cs3": 138.59, "D3": 146.83, "Ds3": 155.56, "E3": 164.81, "F3": 174.61, "Fs3": 185.00,
    "G3": 196.00, "Gs3": 207.65, "A3": 220.00, "As3": 233.08, "B3": 246.94,
    "C4": 261.63, "Cs4": 277.18, "D4": 293.66, "Ds4": 311.13, "E4": 329.63, "F4": 349.23, "Fs4": 369.99,
    "G4": 392.00, "Gs4": 415.30, "A4": 440.00, "As4": 466.16, "B4": 493.88,
    "C5": 523.25, "Cs5": 554.37, "D5": 587.33, "Ds5": 622.25, "E5": 659.25, "F5": 698.46, "Fs5": 739.99,
    "G5": 783.99, "Gs5": 830.61, "A5": 880.00, "As5": 932.33, "B5": 987.77
}

# Output directory
OUTPUT_DIR = "notes"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_note_wave(frequency, duration, sample_rate, volume, fade_duration):
    """Generate a sine wave for a given frequency and duration."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave_data = np.sin(2 * np.pi * frequency * t) * volume
    
    # Apply fade-out to avoid clipping noise
    fade_samples = int(sample_rate * fade_duration)
    fade = np.linspace(1, 0, fade_samples)
    wave_data[-fade_samples:] *= fade

    return (wave_data * 32767).astype(np.int16)  # Convert to 16-bit PCM

def save_wave(filename, wave_data, sample_rate):
    """Save wave data to a file."""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())

# Generate and save notes
for note, freq in NOTE_FREQUENCIES.items():
    wave_data = generate_note_wave(freq, DURATION, SAMPLE_RATE, VOLUME, FADE_DURATION)
    file_path = os.path.join(OUTPUT_DIR, f"{note}.wav")
    save_wave(file_path, wave_data, SAMPLE_RATE)
    print(f"Generated: {file_path}")

print("All notes have been generated!")
