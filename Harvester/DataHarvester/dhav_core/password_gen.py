import random
import string


def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return "".join(random.choice(lettersAndDigits) for i in range(stringLength))


print("Generating a Random String including letters and digits")
print("First Random String is  ", randomStringDigits(60))

