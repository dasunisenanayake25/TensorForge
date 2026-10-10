from app.config import MODEL_VERSION_TAG

# Fixed mapping from your OpenAPI specs
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
    """
    Dummy prediction logic. Member 1's model goes here later.
    """
    predicted_category = "delivery_delay"  # Dummy primary category
    
    return {
        "ticket_id": ticket_id,
        "category": predicted_category,
        "secondary_category": None,
        "team": TEAM_MAP[predicted_category],
        "is_urgent": False,
        "confidence": 0.85, # Dummy confidence
        "model_version": MODEL_VERSION_TAG
    }