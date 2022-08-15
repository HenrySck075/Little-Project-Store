import time


textbox = []
text = input("please input text here (in 1 line):\n")
width = int(input("text width (how many character appear)(int value):\n"))
interval = float(input("scrolling time (float value):\n"))
direction = input("direction (left or right): ")

loop = True
error = False
IndexErrorFirstOccur = 0
textchar = list(text)
textchar.append(" ")
textchar.append(" ")
characteramount = len(textchar)
brandnewintvar = characteramount+1

for i in range(width*2):
    if error:
        item = i - characteramount
    if not error:
        item = i
    try:
        textbox.append(textchar[item])
    except IndexError:
        print(item)
        if IndexErrorFirstOccur == 0:
            item = -1
            error = True
            IndexErrorFirstOccur = 1

if direction == "left":
    idx = width*2
    while loop:
        
        del textbox[0]
        try:
            textbox.append(textchar[idx])
        except IndexError:
            idx = characteramount-characteramount
            textbox.append(textchar[idx])
        idx = idx + 1
        print('    | {0} |         '.format(''.join(textbox)), end="\r")
        time.sleep(interval)

if direction == "right":
    idx = width*2
    while loop:
        
        del textbox[width*2-1]
        try:
            textbox.insert(0, textchar[-(idx+1)])
        except IndexError:
            idx = characteramount-characteramount
            textbox.insert(0, textchar[-(idx+1)])
        idx = idx + 1
        print('    | {0} |         '.format(''.join(textbox)), end="\r")
        time.sleep(interval)