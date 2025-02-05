import random

def send_sms(to_phone):
    verification_code = random.randint(1000, 9999)
    print(f"Verification code sent to {to_phone}: {verification_code}")
    return verification_code