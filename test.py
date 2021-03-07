from pyclick import HumanClicker
import pytweening
import pyautogui
from pyclick.humancurve import HumanCurve
hc = HumanClicker()
curve = HumanCurve(pyautogui.position(),(1000,1000), distortionFrequency=0, tweening=pytweening.easeInOutQuad, offsetBoundaryY=0, offsetBoundaryX=0)
hc.move((100,100), duration=0.1, humanCurve=curve)
