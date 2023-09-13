"""
Defining functions in functions
Another bad habit I have often encountered when reviewing code is defining
functions inside functions for no reason. It has a cost, as the function is
going to be redundantly redefined over and over again.
"""
import dis


def x():
    return 42


print("Disassembling x")
dis.dis(x)


def z():
    def y():
        return 42

    return y()


print("Disassembling z")
dis.dis(z)
