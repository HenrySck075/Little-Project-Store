import random

text = [
    "abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "0123456789",
    "'\":;,.<>/?+=-_!@#$%^&*()~{\}[]"
]

text2 = list(''.join(text))
passstringitem = random.choices(text2,k=random.randint(10,26))
print(''.join(passstringitem))