import tenacity
from random import randint

password = randint(10, 99)
print("PWD:", password)


def crackPassworrd():
    to_check = randint(10, 99)
    if password != to_check:
        print("No luck yet with: ", to_check)
        raise RuntimeError
    print("Password Cracked!!! - ", to_check)


@tenacity.retry(wait=tenacity.wait_fixed(1))
def do_something_and_retry():
    crackPassworrd()


do_something_and_retry()
