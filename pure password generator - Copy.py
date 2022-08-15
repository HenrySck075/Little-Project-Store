import random

text = [
    "abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "0123456789",
    "'\":;,.<>/?+=-_!@#$%^&*()~{\}[]"
]

text2 = list(''.join(text))
passstringitem = []
for i in range(random.randint(10,26)):
    passstringitem.append(random.choice(text2))
print(''.join(passstringitem))