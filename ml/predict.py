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

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def predict_single_ticket(channel: str, text: str, subject: str = "", ticket_id: str = None) -> dict:
    raw_input = f"{channel or ''} {subject or ''} {text or ''}"
    features = vectorizer.transform([raw_input])
    
    # Calculate decision scores and convert to calibrated confidence via softmax
    decision_scores = model.decision_function(features)[0]
    probs = softmax(decision_scores)
    best_idx = int(np.argmax(probs))
    
    primary_category = model.classes_[best_idx]
    confidence = float(probs[best_idx])
    
    # Map to schema-compliant team
    team = map_category_to_team(primary_category)
    content_lower = f"{subject} {text}".lower()
    
    # Urgency rule
    is_urgent = any(kw in content_lower for kw in URGENT_KEYWORDS) or (primary_category == "safety_conduct")
    
    # Secondary category heuristic
    secondary_category = None
    if primary_category != "payment_refund" and any(k in content_lower for k in ["refund", "සල්ලි", "பணம்"]):
        secondary_category = "payment_refund"
    elif primary_category == "delivery_delay" and any(k in content_lower for k in ["missing", "අඩුයි", "குறைவாக"]):
        secondary_category = "order_missing_wrong"
        
    # Schema consistency rules
    if primary_category == "spam_irrelevant":
        is_urgent = False
        secondary_category = None

    response = {
        "category": primary_category,
        "secondary_category": secondary_category,
        "team": team,
        "is_urgent": bool(is_urgent),
        "confidence": round(float(confidence), 4),
        "model_version": "v1.2"
    }
    
    if ticket_id is not None:
        response["ticket_id"] = str(ticket_id)
        
    return response