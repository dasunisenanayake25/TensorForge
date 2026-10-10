import os
import joblib
from app.config import MODEL_VERSION_TAG

# 1. Resolve paths to the ML models
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../../../ml/artifacts"))

MODEL_PATH = os.path.join(ARTIFACTS_DIR, "model.joblib")
VECTORIZER_PATH = os.path.join(ARTIFACTS_DIR, "vectorizer.joblib")

# 2. Load Models into Memory on startup
try:
    classifier_model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("INFO: ML Models loaded successfully!")
except Exception as e:
    print(f"WARNING: Could not load ML models. Error: {e}")
    classifier_model = None
    vectorizer = None

TEAM_MAP = {
    "payment_refund": "Payments & Refunds",
    "ride_trip_issue": "Ride Operations",
    "lost_item": "Lost & Found",
    "order_missing_wrong": "Food Operations",
    "delivery_delay": "Delivery Operations",
    "food_quality": "Restaurant Quality",
    "account_promo": "Account Services",
    "safety_conduct": "Trust & Safety",
    "app_technical": "Tech Support",
    "general_inquiry": "Front-line Support",
    "spam_irrelevant": "Auto-close / Spam Filter"
}

def predict_ticket_category(ticket_id: str, text: str) -> dict:
    predicted_category = "general_inquiry"
    confidence = 0.50

    if classifier_model and vectorizer:
        try:
            text_features = vectorizer.transform([text])
            predicted_category = classifier_model.predict(text_features)[0]
            
            if hasattr(classifier_model, "predict_proba"):
                probabilities = classifier_model.predict_proba(text_features)[0]
                confidence = round(float(max(probabilities)), 2)
        except Exception as e:
            print(f"ERROR: Prediction failed: {e}")

    if predicted_category not in TEAM_MAP:
        predicted_category = "general_inquiry"

    # OpenAPI Consistency Rule: If spam_irrelevant, secondary_category must be null, is_urgent must be false
    is_spam = (predicted_category == "spam_irrelevant")

    return {
        "ticket_id": ticket_id,
        "category": predicted_category,
        "secondary_category": None,
        "team": TEAM_MAP[predicted_category],
        "is_urgent": False, 
        "confidence": confidence,
        "model_version": MODEL_VERSION_TAG
    }