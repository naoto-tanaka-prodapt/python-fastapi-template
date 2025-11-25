import random
import string

## Utils
def create_random_string(length):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    print(random_string)
    return random_string