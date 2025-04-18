import re
import math

with open("passwords.txt") as file:
    unaccepted_passwords = set(line.strip().lower() for line in file)


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
    score = 0
    reasons = []

    if password.lower() in unaccepted_passwords:
        print(f"⚠️ Password ({password}) is in the list of common passwords!")
        print(f"Your password ({password}) strength is: Very Weak")
        return

    if len(password) < 10:
        print("⚠️ Password too short! Minimum 10 characters.")
        print("Your password strength is: Very Weak")
        return
    elif len(password) >= 16:
        score += 2
        reasons.append("✅ Long password (16+ characters)")
    else:
        score += 1

    checks = [
        (r"[a-z]", "lowercase letter"),
        (r"[A-Z]", "uppercase letter"),
        (r"[0-9]", "digit"),
        (r"[!@#$%^&*()_+\-=\\[\]{};':\"|,.<>/?`~]", "symbol"),

    ]

    for pattern, description in checks:
        if re.search(pattern, password):
            score += 1
            reasons.append(f"✅ Contains {description}")
        else:
            reasons.append(f"❌ Missing {description}")

    if re.search(r"(.)\1{2,}", password) or re.search(r"(123|abc|qwerty)", password.lower()):
        score -= 1
        reasons.append("⚠️ Repeated characters or keyboard patterns found")

    entropy = calculate_entropy(password)
    reasons.append(f"🔐 Entropy: {entropy} bits")

    if entropy >= 60:
        score += 1
        reasons.append("✅ High entropy (60+ bits)")
    elif entropy < 30:
        score -= 1
        reasons.append("⚠️ Low entropy (<30 bits)")
    else:
        reasons.append("⚠️ Medium entropy (30–59 bits)")

    score = max(0, min(score, 6))
    strength = ["Very Weak", "Weak", "Moderate",
                "Strong", "Very Strong", "Excellent", "Top Tier"]
    print("\n".join(reasons))
    print(f"🔎 Final Score: {score}/6")
    print(f"🔐 Your password strength is: {strength[score]}")


check_password_strength("Write_YourSecured_Password_Here")
