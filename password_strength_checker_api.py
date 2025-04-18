import re
import math

with open("passwords.txt") as file:
    unaccepted_passwords = set(line.strip().lower() for line in file)

strength_levels = ["Very Weak", "Weak", "Moderate",
                        "Strong", "Very Strong", "Excellent", "Top Tier"]



def calculate_entropy(password):
    pool = 0
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[0-9]", password):
        pool += 10
    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]", password):
        pool += 32

    if pool == 0:
        return 0
    return round(len(password) * math.log2(pool), 2)


def check_password_strength(password):

    result = {"password": password, "rating": [], "score": 0, "reasons": []}

    if password.lower() in unaccepted_passwords:
        result["strength"] = "Very weak"
        result["rating"] = strength_levels
        result["reasons"].append(
            f"⚠️ Password ({password}) is in the list of common passwords!")
        return result
    if len(password) < 10:
        result["strength"] = "Very weak"
        result["rating"] = strength_levels
        result["reasons"].append(
            "⚠️ Password too short! Minimum 10 characters.")
        return result
    elif len(password) >= 16:
        result["score"] += 2
        result["reasons"].append("✅ Long password (16+ characters)")
    else:
        result["score"] += 1

    checks = [
        (r"[a-z]", "lowercase letter"),
        (r"[A-Z]", "uppercase letter"),
        (r"[0-9]", "digit"),
        (r"[!@#$%^&*()_+\-=\\[\]{};':\"|,.<>/?`~]", "symbol"),

    ]

    for pattern, description in checks:
        if re.search(pattern, password):
            result["score"] += 1
            result["reasons"].append(f"✅ Contains {description}")
        else:
            result["reasons"].append(f"❌ Missing {description}")

    if re.search(r"(.)\1{2,}", password) or re.search(r"(123|abc|qwerty)", password.lower()):
        result["score"] -= 1
        result["reasons"].append(
            "⚠️ Repeated characters or keyboard patterns found")

    entropy = calculate_entropy(password)
    result["reasons"].append(f"🔐 Entropy: {entropy} bits")

    if entropy >= 60:
        result["score"] += 1
        result["reasons"].append("✅ High entropy (60+ bits)")
    elif entropy < 30:
        result["score"] -= 1
        result["reasons"].append("⚠️ Low entropy (<30 bits)")
    else:
        result["reasons"].append("⚠️ Medium entropy (30–59 bits)")

    result["score"] = max(0, min(result["score"], 6))

    result["strength"] = strength_levels[result["score"]]
    result["rating"] = strength_levels

    return result
