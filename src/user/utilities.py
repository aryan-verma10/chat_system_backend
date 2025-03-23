import random


async def send_otp_helper_func(email:str) -> str:
    random_number = str(random.randint(10000, 99999))
    return random_number   