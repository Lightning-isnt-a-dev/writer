import time, random, os
from tkinter.filedialog import askopenfilename
from ahk import AHK

def clearScreen():
  os.system("cls")

def loadtext():
    #file = input("path: ")
    with open(askopenfilename(filetypes=[("text file", ".txt")], initialdir=os.getcwd()), encoding="utf-8") as f:
        return f.read()

def writetext(text, DBG, delays, SaveDelay):
    ahk = AHK()
    for i in range(3, 0, -1):
        print(i)
        time.sleep(1)

    skips = 0
    for idx, char in enumerate(text):
        if skips > 0:
            skips -= 1
            continue

        #pause between tehtävät
        if char == "*" and text[idx+1] == "*":
            if text[idx:idx+9] == "**PAUSE**":
                time.sleep(random.uniform(delays["pauses"][0], delays["pauses"][1]))
                skips = 9
                continue
        
        #if shifts are needed
        if not char.isalnum() and char not in ",.-'´<+\n ":
            shift = True
        else:
            shift = False
        
        #if newline
        if char == "\n":
            char = "Enter"

        #if space
        if char == " ":
            char = "Space"


        #pauses between words
        if char == "Space":
            num = random.randrange(0, 11)
            if num % 2 == 0:
                time.sleep(random.uniform(delays["spaces"][0], delays["spaces"][1]))
            
        if char == "Enter":
            time.sleep(random.uniform(delays["newlines"][0], delays["newlines"][1]))

            #let docs save
            if random.randrange(0, 16) == 3 and SaveDelay:
                time.sleep(random.uniform(delays["saves"][0], delays["saves"][1]))

        #typing speed
        time.sleep(random.uniform(delays["characters"][0], delays["characters"][1]))

        #if is ? for example
        if shift:
            ahk.key_down("shift")

        ahk.key_press(char)

        if shift:
            ahk.key_release("shift")
            shift = False
    return



def loop(text, DBG, delays, SaveDelay):
    clearScreen()
    if not delays:
        delays = {
            "saves"      : (5.50, 6.90, (5.50, 6.90), "(randomly at newlines to let docs save, togglable)"),
            "pauses"     : (20.0, 25.0, (20.0, 25.0), "(pauses if it finds **PAUSE**)"),
            "spaces"     : (0.45, 0.75, (0.45, 0.75), "(delays between spaces)"),
            "newlines"   : (2.00, 3.25, (2.00, 3.25), "(delays between newlines)"),
            "characters" : (0.10, 0.30, (0.10, 0.30), "(delays between characters)")

        }
    if DBG is None:
        DBG = False
    
    if SaveDelay is None:
        SaveDelay = True

    print("l == load from txt file, w == write (3 SEC WAIT), d == delays, e == exit, docs = docs mode (only delay for enters)")
    a = str(input())


    if a == "dbg":
        DBG = True

    if a == "docs":
        delays["saves"]      = (0, 0, (5.50, 6.90), "(randomly at newlines to let docs save, togglable)")
        delays["pauses"]     = (60.0, 60.0, (20.0, 25.0), "(pauses if it finds **PAUSE**)")
        delays["spaces"]     = (0, 0, (0.45, 0.75), "(delays between spaces)")
        delays["newlines"]   = (0, 0, (2.00, 3.25), "(delays between newlines)")
        delays["characters"] = (0, 0, (0.10, 0.30), "(delays between characters)")
    

    if a == "d":
        for delayTYPE, (currentMIN, currentMAX, defaultTUPLE, context) in delays.items():
            clearScreen()
            print(f"{delayTYPE} {context}, current: {currentMIN}-{currentMAX}, default: {defaultTUPLE[0]}-{defaultTUPLE[1]}")

            inputMIN = float(input(f"new {delayTYPE} minimum: ")); inputMAX = float(input(f"new {delayTYPE} maximum: "))

            NewDictValue = (inputMIN, inputMAX, defaultTUPLE, context)
            delays[delayTYPE] = NewDictValue
        clearScreen()

        print("delay sometimes between enters:", SaveDelay)
        i = input("T = true, F = false: ")
        if i.lower() == "t":
            SaveDelay = True
        
        if i.lower() == "f":
            SaveDelay = False
        
        if DBG:
            print(delays, SaveDelay)
            input()
    

    if a == "l":
        clearScreen()
        text = loadtext()


    if a == "w":
        clearScreen()
        writetext(text, DBG, delays, SaveDelay)


    if a == "e":
        exit()
    
    loop(text, DBG, delays, SaveDelay)

if __name__ == "__main__":
    loop(None, None, None, None)