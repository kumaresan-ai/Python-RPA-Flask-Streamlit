import pyautogui

print("imported pyautogui")

#Mouse operations
#Find the position of the mouse pointer using below code and give it as the input to other functions like click, rightClick etc
# pyautogui.sleep(5)
# x, y = pyautogui.position()
# print(f'x: {x}, y: {y}')


# pyautogui.click(x, y)

# pyautogui.sleep(5)

# pyautogui.rightClick(200, 100)
# pyautogui.drag(100,100,200,200)
# pyautogui.scroll(500)

#keyboard operations
# pyautogui.write("sample text typed from keyboard")
# pyautogui.press("enter")
# pyautogui.sleep(3)
# pyautogui.click(374, 315)
# pyautogui.hotkey("ctrl", "a")
# pyautogui.sleep(2)
# pyautogui.hotkey("ctrl", "c")
# pyautogui.sleep(2)
# pyautogui.click(374, 315)
# pyautogui.sleep(2)
# pyautogui.hotkey("ctrl", "v")

#image operations
#install the package pip install opencv-python
# take a screenshot of the button and save it in the project.
# use the below code to locate the image in your screen and click it.

#code to locate the image. imagename.png is the file saved in the root directory of project.
location = pyautogui.locate("imagename.png", confidence=0.8)

pyautogui.click(pyautogui.center(location))

#to know the screen size.
pyautogui.size()

#to take screenshot of the screen
image = pyautogui.screenshot()
image.save("screenshot.png")

#Playright - Execute below commands to setup playright environment.
#pip install playwright
#playwright install