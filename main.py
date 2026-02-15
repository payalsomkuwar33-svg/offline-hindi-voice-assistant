# main.py
import os
import time
import json
from datetime import datetime

# ------------------ Try Voice Setup ------------------
try:
    from vosk import Model, KaldiRecognizer
    import sounddevice as sd
    use_voice = True
except ImportError:
    print("Voice libraries missing. Text mode activated.")
    use_voice = False

MODEL_PATH = "models/vosk-model-small-hi-0.22"

if use_voice:
    if not os.path.exists(MODEL_PATH):
        print("Vosk model not found. Switching to text mode.")
        use_voice = False
    else:
        model = Model(MODEL_PATH)
        recognizer = KaldiRecognizer(model, 16000)

# ------------------ Hindi Math Helper ------------------

# Hindi number words → digits
number_map = {
    "शून्य": "0", "एक": "1", "दो": "2", "तीन": "3", "चार": "4",
    "पाँच": "5", "छह": "6", "सात": "7", "आठ": "8", "नौ": "9",
    "दस": "10", "ग्यारह": "11", "बारह": "12", "तेरह": "13",
    "चौदह": "14", "पंद्रह": "15", "सोलह": "16", "सत्रह": "17",
    "अठारह": "18", "उन्नीस": "19", "बीस": "20"
}

# Hindi operators → symbols
operator_map = {
    "प्लस": "+", "जोड़": "+",
    "माइनस": "-", "घटाव": "-",
    "गुना": "*",
    "भाग": "/", "बटा": "/"
}

def hindi_to_math(expr: str) -> str:
    """
    Convert Hindi math expression like 'दो प्लस तीन' → '2+3'
    """
    expr = expr.lower().strip().split()
    result = ""
    for word in expr:
        if word in number_map:
            result += number_map[word]
        elif word in operator_map:
            result += operator_map[word]
        elif word.isdigit():
            result += word
        else:
            pass
    return result

def solve_hindi_math(expr: str) -> str:
    try:
        math_expr = hindi_to_math(expr)
        if not math_expr:
            return "मैं इसे गणित के रूप में नहीं समझ पाया।"
        result = eval(math_expr)
        return f"उत्तर है {result}"
    except:
        return "माफ़ कीजिये, मैं यह गणित हल नहीं कर पाया।"

# ------------------ Helper Functions ------------------

def get_time():
    return datetime.now().strftime("%H:%M:%S")

def get_date():
    return datetime.now().strftime("%d-%m-%Y")

def get_cpu_usage():
    try:
        import psutil
        return f"CPU उपयोग {psutil.cpu_percent()} प्रतिशत है।"
    except:
        return "CPU जानकारी उपलब्ध नहीं है।"

def assistant_speak(text):
    print("Assistant:", text)

# ------------------ Intent Detection ------------------

def detect_intent(text):
    text = text.lower()

    if any(word in text for word in ["हेलो", "नमस्ते", "hello"]):
        return "greet"
    if any(word in text for word in ["समय", "टाइम", "कितने बजे"]):
        return "time"
    if any(word in text for word in ["तारीख", "डेट", "आज की तारीख"]):
        return "date"
    if any(word in text for word in ["तुम कौन", "आप कौन"]):
        return "identity"
    if "भारत की राजधानी" in text:
        return "capital"
    if "प्रधानमंत्री" in text:
        return "pm"
    if any(word in text for word in ["जोक", "मजेदार"]):
        return "joke"
    if "कहानी" in text:
        return "story"
    if "cpu" in text or "प्रोसेसर" in text:
        return "cpu"
    if any(word in text for word in ["बंद करो", "exit", "quit", "बाहर"]):
        return "exit"
    # Check for math words
    math_words = set(number_map.keys()).union(set(operator_map.keys()))
    if any(word in text for word in math_words) or any(op in text for op in "+-*/"):
        return "math"
    return "unknown"

# ------------------ Action Handler ------------------

def handle_intent(intent, text):
    if intent == "greet":
        return "नमस्ते! मैं आपका ऑफलाइन हिंदी असिस्टेंट हूँ।"
    elif intent == "time":
        return f"अभी का समय {get_time()} है।"
    elif intent == "date":
        return f"आज की तारीख {get_date()} है।"
    elif intent == "identity":
        return "मैं एक ऑफलाइन और प्राइवेसी सुरक्षित हिंदी वॉइस असिस्टेंट हूँ।"
    elif intent == "capital":
        return "भारत की राजधानी नई दिल्ली है।"
    elif intent == "pm":
        return "भारत के वर्तमान प्रधानमंत्री नरेंद्र मोदी हैं।"
    elif intent == "math":
        return solve_hindi_math(text)
    elif intent == "joke":
        return "टीचर: होमवर्क क्यों नहीं किया? छात्र: सर, कल लाइट चली गई थी।"
    elif intent == "story":
        return "एक समय की बात है, एक छोटे से गाँव में लोग खुशी से रहते थे।"
    elif intent == "cpu":
        return get_cpu_usage()
    elif intent == "exit":
        return "अलविदा! फिर मिलेंगे।"
    else:
        return "मुझे समझ नहीं आया। कृपया दोबारा कहें।"

# ------------------ Voice Input ------------------

def listen_voice():
    duration = 4
    recording = sd.rec(int(duration * 16000), samplerate=16000, channels=1)
    sd.wait()
    if recognizer.AcceptWaveform(recording.tobytes()):
        result = json.loads(recognizer.Result())
        return result.get("text", "")
    return ""

# ------------------ MAIN LOOP ------------------

assistant_speak("नमस्ते! मैं आपका हिंदी असिस्टेंट हूँ। आप मुझसे बात कर सकते हैं।")

while True:
    try:
        start_time = time.time()

        if use_voice:
            print("Assistant: कृपया बोलें...")
            user_input = listen_voice()
        else:
            user_input = input("आप: ")

        user_input = user_input.strip().lower()
        if not user_input:
            continue

        intent = detect_intent(user_input)
        response = handle_intent(intent, user_input)

        assistant_speak(response)

        end_time = time.time()
        print(f"(Response Time: {round(end_time - start_time, 2)} sec)\n")

        if intent == "exit":
            break

    except KeyboardInterrupt:
        assistant_speak("अलविदा! फिर मिलेंगे।")
        break
