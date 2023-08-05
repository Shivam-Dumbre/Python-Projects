import pyautogui as p   
print("Playing") 
y = 1 
while True: 
    x = p.pixel(500,223) 
    if x!=y: 
        p.press('space') 
        y = x  