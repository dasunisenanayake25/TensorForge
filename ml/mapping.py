CATEGORY_TO_TEAM = {
    "safety_conduct": "safety_team",
    "payment_refund": "payments_team",
    "ride_trip_issue": "rides_support",
    "delivery_delay": "deliveries_team",
    "order_missing_wrong": "deliveries_team",
    "food_quality": "deliveries_team",
    "lost_item": "lost_and_found",
    "account_promo": "accounts_team",
    "app_technical": "technical_support",
    "general_inquiry": "general_support",
    "spam_irrelevant": "spam_desk"
}

def map_category_to_team(category: str) -> str:
    """
    Maps a predicted ticket category to its assigned operational team.
    Defaults to 'general_support' for unrecognized categories.
    """
    return CATEGORY_TO_TEAM.get(category, "general_support")