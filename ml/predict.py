import joblib
import numpy as np
from ml.mapping import map_category_to_team

model = joblib.load("ml/artifacts/model.joblib")
vectorizer = joblib.load("ml/artifacts/vectorizer.joblib")

URGENT_KEYWORDS = [
    "urgent", "danger", "accident", "emergency", "police", "threat", 
    "hospital", "fraud", "scam", "blood", "stolen", "lost child",
    "අනතුරක්", "තර්ජනය", "බයයි", "රෝහල", "marundhu", "mirattinaaru"
]

def predict_single_ticket(channel: str, text: str, subject: str = "", ticket_id: str = None) -> dict:
    raw_input = f"{channel or ''} {subject or ''} {text or ''}"
    features = vectorizer.transform([raw_input])
    
    # Predict category and true confidence
    probs = model.predict_proba(features)[0]
    best_idx = np.argmax(probs)
    primary_category = model.classes_[best_idx]
    confidence = float(probs[best_idx])
    
    # OpenAPI Consistency Rules
    team = map_category_to_team(primary_category)
    content_lower = f"{subject} {text}".lower()
    
    # Urgency detection
    is_urgent = any(kw in content_lower for kw in URGENT_KEYWORDS) or (primary_category == "safety_conduct")
    
    # Secondary Category heuristic (Must differ from primary)
    secondary_category = None
    if primary_category != "payment_refund" and ("refund" in content_lower or "සල්ලි" in content_lower or "பணம்" in content_lower):
        secondary_category = "payment_refund"
    elif primary_category == "delivery_delay" and ("missing" in content_lower or "අඩුයි" in content_lower):
        secondary_category = "order_missing_wrong"
        
    # Strict Schema Rule: If spam_irrelevant, is_urgent must be False and secondary_category must be None
    if primary_category == "spam_irrelevant":
        is_urgent = False
        secondary_category = None

    response = {
        "category": primary_category,
        "secondary_category": secondary_category,
        "team": team,
        "is_urgent": is_urgent,
        "confidence": round(confidence, 4),
        "model_version": "v1.2"
    }
    
    if ticket_id is not None:
        response["ticket_id"] = ticket_id
        
    return response