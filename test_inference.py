# test_inference.py
from ml.predict import predict_single_ticket

# 1. Normal delivery delay with Sinhala/Singlish
sample_1 = predict_single_ticket(
    channel="chat",
    subject="",
    text="order eka godak late salli refund ekak denna puluwanda",
    ticket_id="TF-TEST-001"
)
print("Sample 1 Output:\n", sample_1)

# 2. Urgent safety incident
sample_2 = predict_single_ticket(
    channel="call_transcript",
    subject="",
    text="driver wahane nawathwanne na accident ekak wenna yanne please help",
    ticket_id="TF-TEST-002"
)
print("\nSample 2 Output:\n", sample_2)

# 3. Spam ticket check
sample_3 = predict_single_ticket(
    channel="email",
    subject="fictional project",
    text="imaginary moon rocks wikunanawa ada ganna",
    ticket_id="TF-TEST-003"
)
print("\nSample 3 Output:\n", sample_3)