import dis

abc = ("a", "b", "c")


def concat_a_1():
    for letter in abc:
        abc[0] + letter


def concat_a_2():
    a = abc[0]
    for letter in abc:
        a + letter


print("Disassembling concat_a_1")
dis.dis(concat_a_1)

print("Disassembling concat_a_2")
dis.dis(concat_a_2)
