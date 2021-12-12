## CircuitPython Animation Tester for the S2 Nugget by @KodyKinzie
## Add .BMP images to /frames folder to start animation
import os
import board
import neopixel
from board import SCL, SDA
import busio
import displayio
import adafruit_framebuf
import adafruit_displayio_sh1106
import time

defaultDelay = 0 ## Here you can adjust the amount of time between frames loading
num_pixels = 1 ## How many neopixels are attached?

animation = []

for files in os.listdir("/frames/"): ## Creating the animation
    if '._' in files: ## Remove hidden files that would break this
        pass
    else:
        animation.append(files) ## Add valid files to animation

## Screen setup and function to change image on the screen

displayio.release_displays()
WIDTH = 130 # Change these to the right size for your display!
HEIGHT = 64
BORDER = 1
i2c = busio.I2C(SCL, SDA) # Create the I2C interface.
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = adafruit_displayio_sh1106.SH1106(display_bus, width=WIDTH, height=HEIGHT) # Create the SH1106 OLED class.

def NugEyes(IMAGE): ## Make a function to put eyes on the screen
    filepath = "/frames/{}".format(IMAGE)
    bitmap = displayio.OnDiskBitmap(filepath) # Setup the file as the bitmap data source
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader) # Create a TileGrid to hold the bitmap
    group = displayio.Group() # Create a Group to hold the TileGrid
    group.append(tile_grid) # Add the TileGrid to the Group
    display.show(group) # Add the Group to the Display
    time.sleep(defaultDelay)

pixel_pin = board.IO12    # Specify the pin that the neopixel is connected to (GPIO 12)
pixel = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3)   # Create neopixel and set brightness to 30%

def SetAll(color):   # Define function with one input (color we want to set)
    for i in range(0, num_pixels):   # Addressing all 1 neopixels in a loop
        pixel[i] = (color)   # Set all neopixels a color

def startAnimation():
    for frames in animation:
        try: NugEyes(frames)
        except ValueError: pass

if len(animation) != 0:
    SetAll([0,10,0])
    while True:
        startAnimation()
else:
    print("No Images Found!"); SetAll([10,0,0])
