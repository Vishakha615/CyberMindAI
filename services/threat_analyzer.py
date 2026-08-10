import re


def extract_features(text):

    text_lower = text.lower()

    features = {
        "urgent_words": 0,
        "credential_words": 0,
        "link_present": 0,
        "suspicious_words": 0,
        "financial_words": 0
    }

    urgent_words = [
        "urgent",
        "immediately",
        "now",
        "expire",
        "suspended",
        "warning"
    ]

    credential_words = [
        "password",
        "username",
        "otp",
        "login",
        "verify",
        "credential"
    ]

    suspicious_words = [
        "click",
        "claim",
        "winner",
        "prize",
        "free",
        "congratulations"
    ]

    financial_words = [
        "bank",
        "payment",
        "credit card",
        "debit card",
        "money",
        "account"
    ]

    features["urgent_words"] = sum(
        word in text_lower
        for word in urgent_words
    )

    features["credential_words"] = sum(
        word in text_lower
        for word in credential_words
    )

    features["suspicious_words"] = sum(
        word in text_lower
        for word in suspicious_words
    )

    features["financial_words"] = sum(
        word in text_lower
        for word in financial_words
    )

    features["link_present"] = int(
        bool(
            re.search(
                r"https?://|www\.",
                text_lower
            )
        )
    )

    return features


def calculate_threat_score(features):

    score = 0

    score += features["urgent_words"] * 15

    score += features["credential_words"] * 15

    score += features["suspicious_words"] * 10

    score += features["financial_words"] * 10

    score += features["link_present"] * 20

    return min(score, 100)


def classify_threat(score):

    if score >= 70:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    else:
        return "LOW"


def analyze_text(text):

    features = extract_features(text)

    score = calculate_threat_score(
        features
    )

    threat_level = classify_threat(
        score
    )

    return {
        "threat_level": threat_level,
        "score": score,
        "features": features
    }