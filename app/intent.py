# app/intent.py

def process_intent(text):
    text = text.lower().strip()

    intents = {

        "greeting": ["हेलो", "नमस्ते", "hello"],
        "time": ["समय", "टाइम", "कितने बजे"],
        "date": ["तारीख", "डेट", "आज की तारीख"],
        "exit": ["बंद करो", "बाहर", "exit", "quit"],
        "who_are_you": ["तुम कौन हो", "आप कौन हो"],
        "capital_india": ["भारत की राजधानी"],
        "prime_minister": ["प्रधानमंत्री कौन"],
        "joke": ["जोक", "मजेदार"],
        "story": ["कहानी"],
        "cpu": ["cpu", "प्रोसेसर उपयोग"],
        "math": ["+", "-", "*", "/"],
    }

    # Check each intent
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in text:
                return intent

    return "unknown"
