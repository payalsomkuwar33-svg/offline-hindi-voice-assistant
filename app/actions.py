# actions.py

import time
from datetime import datetime
import os
import psutil
from math_helper import solve_hindi_math  #  import

def perform_action(intent, text=None):

    if intent == "greeting":
        return "नमस्ते! मैं आपका ऑफलाइन हिंदी असिस्टेंट हूँ।"

    elif intent == "time":
        current_time = datetime.now().strftime("%H:%M:%S")
        return f"अभी का समय है {current_time}"

    elif intent == "date":
        today = datetime.now().strftime("%d-%m-%Y")
        return f"आज की तारीख है {today}"

    elif intent == "who_are_you":
        return "मैं एक ऑफलाइन, प्राइवेसी-प्रिज़र्विंग हिंदी वॉइस असिस्टेंट हूँ।"

    elif intent == "capital_india":
        return "भारत की राजधानी नई दिल्ली है।"

    elif intent == "prime_minister":
        return "भारत के वर्तमान प्रधानमंत्री नरेंद्र मोदी हैं।"

    elif intent == "joke":
        return "टीचर: होमवर्क क्यों नहीं किया? छात्र: सर, कल लाइट चली गई थी।"

    elif intent == "story":
        return "एक समय की बात है, एक छोटा सा गाँव था जहाँ लोग मिलजुल कर रहते थे।"

    elif intent == "cpu":
        cpu_usage = psutil.cpu_percent()
        return f"वर्तमान CPU उपयोग {cpu_usage} प्रतिशत है।"

    elif intent == "math":
        return solve_hindi_math(text)  # ← अब Hindi math handle करेगा

    elif intent == "exit":
        return "अलविदा! फिर मिलेंगे।"

    else:
        return "मुझे समझ नहीं आया। कृपया दोबारा पूछें।"
