# math_helper.py

# हिंदी शब्द → अंक mapping
number_map = {
    "शून्य": "0", "एक": "1", "दो": "2", "तीन": "3", "चार": "4",
    "पाँच": "5", "छह": "6", "सात": "7", "आठ": "8", "नौ": "9",
    "दस": "10", "ग्यारह": "11", "बारह": "12", "तेरह": "13", 
    "चौदह": "14", "पंद्रह": "15", "सोलह": "16", "सत्रह": "17",
    "अठारह": "18", "उन्नीस": "19", "बीस": "20"
}

# हिंदी शब्द → ऑपरेटर mapping
operator_map = {
    "प्लस": "+",
    "जोड़": "+",
    "माइनस": "-",
    "घटाव": "-",
    "गुना": "*",
    "भाग": "/",
    "बटा": "/"
}

def hindi_to_math(expr: str) -> str:
    """
    Convert a Hindi math expression like 'दो प्लस तीन' → '2+3'
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
            # ignore unknown words
            pass
    return result

def solve_hindi_math(expr: str) -> str:
    """
    Evaluate Hindi math expression and return result
    """
    try:
        math_expr = hindi_to_math(expr)
        if not math_expr:
            return "मैं इसे गणित के रूप में नहीं समझ पाया।"
        result = eval(math_expr)
        return f"उत्तर है {result}"
    except Exception:
        return "माफ़ कीजिये, मैं यह गणित हल नहीं कर पाया।"
