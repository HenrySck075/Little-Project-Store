import random

sortedl = list(range(10))
hi = list(range(10))
random.shuffle(hi)

while hi != sortedl:
    print(hi, end="\r")
    random.shuffle(hi)

print("Done")
