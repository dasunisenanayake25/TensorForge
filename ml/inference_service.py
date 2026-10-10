import joblib
import pandas as pd
from ml.mapping import map_category_to_team

model = joblib.load("ml/artifacts/model.joblib")
vectorizer = joblib.load("ml/artifacts/vectorizer.joblib")

URGENT_KEYWORDS = [
    "urgent", "danger", "accident", "emergency", "police", "threat", 
    "hospital", "fraud", "scam", "blood", "stolen", "lost child"
]

def predict_ticket(ticket_id: str, channel: str, subject: str, text: str, language: str = "en"):
    combined_text = f"{language} {subject or ''} {text or ''}"
    features = vectorizer.transform([combined_text])
    
    primary_category = model.predict(features)[0]
    assigned_team = map_category_to_team(primary_category)
    
    # Rule-based urgency detection aligned with DATA_NOTES
    full_content = (f"{subject} {text}").lower()
    is_urgent = any(word in full_content for word in URGENT_KEYWORDS) or (primary_category == "safety_conduct")
    
    # Secondary category heuristic
    secondary_category = None
    if primary_category == "delivery_delay" and ("refund" in full_content or "money" in full_content):
        secondary_category = "payment_refund"
    elif primary_category == "order_missing_wrong" and ("refund" in full_content):
        secondary_category = "payment_refund"

    return {
        "ticket_id": ticket_id,
        "category": primary_category,
        "secondary_category": secondary_category,
        "is_urgent": is_urgent,
        "team": assigned_team
    }