import cv2
import numpy as np
from mpmath import mpf, mp
from PIL import Image

mp.prec = 512
BlockSize = input("Enter block size: ")
width = input("Enter Width:")
height = input("Enter Height:")
width = int(width)
height = int(height)
DataType = input("Enter DataType: ")

if DataType == '16' or DataType == 'float16':
    flattened = np.fromfile('tags.npy', dtype=np.float16)
    prop = np.fromfile('prop.npy', dtype=np.float16)
elif DataType == '32' or DataType == 'float32':
    flattened = np.fromfile('tags.npy', dtype=np.float32)
    prop = np.fromfile('prop.npy', dtype=np.float32)
else:
    flattened = np.fromfile('tags.npy', dtype=np.float64)
    prop = np.fromfile('prop.npy', dtype=np.float64
                       )
for x in range(256):
    print(x, prop[x])
print('Decoding ... ')
# -------------------------
# -------- Decode ---------
# -------------------------
freq = {}
for x in range(256):
    if prop[x] == 0:
        list(prop).pop(x)
    else:
        freq[x] = prop[x]


image = [[0 for x in range(width)] for y in range(height)]
i = 0
lower = mpf(0)
upper = mpf(0)
wIndex = hIndex = 0
color = mpf(0)
for tag in flattened:
    lowerLimit = mpf(0)
    upperLimit = mpf(1)
    upper = lowerLimit
    for i in range(int(BlockSize)):
        for color in freq:
            lower = upper
            upper = lower + (upperLimit - lowerLimit)*freq[color]
            if (tag >= lower) and (tag <= upper):
                if hIndex == height:
                    break
                image[hIndex][wIndex] = color
                wIndex += 1
                if wIndex == width:
                    wIndex = 0
                    hIndex += 1
                lowerLimit = lower
                upperLimit = upper
                upper = lower
                break
        if (width * height) == (wIndex * hIndex):
            break
    if (width * height) == (wIndex * hIndex):
        break
im = Image.fromarray(np.array(image, dtype=np.uint8))
im.save("final.jpg")
