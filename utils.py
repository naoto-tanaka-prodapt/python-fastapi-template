import random
import string

## Utils
def create_random_file_name(extention):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    print(random_string)
    return random_string + extention