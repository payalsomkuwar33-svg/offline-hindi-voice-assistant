import platform
import os

# Detect OS
OS_NAME = platform.system()

def speak(text, offline=True):
    """
    Speak the given text.

    Parameters:
    - text: string to speak
    - offline: if True, tries offline speech; if False, just prints

    Works in Codespace safely.
    """
    print("Assistant:", text)

    # If offline speech is disabled, just return
    if not offline:
        return

    # On local Linux machine with espeak installed
    if OS_NAME == "Linux":
        try:
            os.system(f'espeak -v hi "{text}"')
        except Exception as e:
            print("espeak not available:", e)

    # On Windows or other OS: try pyttsx3 if installed
    elif OS_NAME == "Windows":
        try:
            import pyttsx3
            engine = pyttsx3.init()
            # Try to set Hindi voice if available
            for v in engine.getProperty('voices'):
                if "hi" in v.id.lower():
                    engine.setProperty("voice", v.id)
                    break
            engine.setProperty("rate", 150)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("pyttsx3 not available:", e)

    # If no TTS available, just print
    else:
        print("(No offline TTS available, text printed instead)")
