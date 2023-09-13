import random


def sumRec(arr):
    if len(arr) == 0:
        return 0
    return arr[0] + sumRec(arr[1:])

def sumLin(arr):
    curSum = 0
    for x in arr:
        curSum += x
    return curSum

arr = [random.randint(0, 200) for i in range(500)]
print(sumRec(arr))
print(sumLin(arr))
