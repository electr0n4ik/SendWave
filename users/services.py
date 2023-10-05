from random import randint


def generate_verification_token():
    """Creating token for email verification, without him user is not_active=False, and he can't log in"""
    token = ''.join(str(randint(0, 9)) for _ in range(20))
    return token
