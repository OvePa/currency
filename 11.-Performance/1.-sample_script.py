"""
In the following terminal, click Run and use the command <
python -m cProfile sample_script.py > to view the cProfile of
sample_script.py file.
"""
import time


def x():
    time.sleep(1)


def y():
    x()
    z()


def z():
    time.sleep(2)


def w():
    time.sleep(3)
    x()


def main():
    x()
    y()
    z()
    w()


main()

"""
You can use the -s option to sort by any fields, e.g. < -s > time sorts by internal 
time. Try using command < python -m cProfile -s time sample_script.py >
"""
