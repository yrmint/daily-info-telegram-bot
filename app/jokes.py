import random


def get_joke():
    num = random.randint(0, 277)
    f = open(f"jokes\{num}.txt", "r")
    joke = f.read()
    f.close()
    return joke
