import sys
from PIL import Image

img = Image.open('resources/images/probharath_elephant.png')
img.save('resources/images/ProBharath.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
img.save('resources/images/OrcaSlicer.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
img.save('resources/images/OrcaSlicerTitle.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
print("Icons generated!")
