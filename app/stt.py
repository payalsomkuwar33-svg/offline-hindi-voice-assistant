# app/stt.py

import queue
import sounddevice as sd
import json
import platform
from vosk import Model, KaldiRecognizer

q = queue.Queue()
OS_NAME = platform.system()

# Try loading Vosk model
try:
    model = Model("models/vosk-model-small-hi-0.22")
    rec = KaldiRecognizer(model, 16000)
except Exception as e:
    print("Vosk model not loaded:", e)
    model = None
    rec = None

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen(duration=5):
    """
    Dual-mode listen:
    - If mic available → record voice
    - If mic not available (Codespace) → ask user to type
    """
    if OS_NAME == "Linux" and model is not None:
        # Attempt real microphone listening
        try:
            with sd.RawInputStream(
                samplerate=16000,
                blocksize=8000,
                dtype='int16',
                channels=1,
                callback=callback
            ):
                print("Listening...")
                frames = 0
                max_frames = int(duration * 16000 / 8000)
                while frames < max_frames:
                    data = q.get()
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        return result.get("text", "")
                    frames += 1
                # return partial result
                result = json.loads(rec.FinalResult())
                return result.get("text", "")
        except Exception as e:
            print("Mic not available, switching to text input:", e)

    # Fallback for Codespace / no mic
    text = input("Type your command (Hindi): ")
    return text
