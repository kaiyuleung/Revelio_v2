import random
import string

def get_random_string():
    return ''.join(random.sample(string.ascii_letters + string.digits, 8))

def get_random_avatar():
    return f"https://xsgames.co/randomusers/assets/avatars/pixel/{random.randint(0,53)}.jpg"
