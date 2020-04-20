import cv2
import numpy as np

# getting info from user
path = input("Enter Image Path: ")
BlockSize = input("Enter block size: ")
BlockSize = int(BlockSize)
DataType = input("Enter DataType: ")

# reading the image
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

# flatting the image
flattened = [val for sublist in img for val in sublist]

if DataType == '16' or DataType == 'float16':
    print('16')
    probability = np.zeros(256, dtype=np.float16)
    if (len(flattened) % BlockSize) == 0:
        tags = np.zeros(int(len(flattened) / BlockSize), dtype=np.float16)
    else:
        tags = np.zeros((len(flattened) // BlockSize) + 1, dtype=np.float16)
elif DataType == '32' or DataType == 'float32':
    print('32')
    probability = np.zeros(256, dtype=np.float32)
    if (len(flattened) % BlockSize) == 0:
        tags = np.zeros(int(len(flattened) / BlockSize), dtype=np.float32)
    else:
        tags = np.zeros((len(flattened) // BlockSize) + 1, dtype=np.float32)
else:
    print('64')
    probability = np.zeros(256, dtype=np.float64)
    if (len(flattened) % BlockSize) == 0:
        tags = np.zeros(int(len(flattened) / BlockSize), dtype=np.float64)
    else:
        tags = np.zeros((len(flattened) // BlockSize) + 1, dtype=np.float64)


# getting Frequency
freq = {}
for x in range(256):
    freq[x] = 0
for char in flattened:
    freq[char] += 1


# calculating probability
for i in list(freq):
    if freq[i] == 0:
        freq.pop(i)
    else:
        freq[i] = freq[i]/(len(flattened))
        probability[i] = freq[i]

probability.tofile('prop.npy')

for x in range(256):
    print(x, probability[x])

# +++++++++++++++++++++++++
# ----arithmetic coding----
# +++++++++++++++++++++++++

print('Encoding ... ')

# initializing

index = 0
upper = constUpper = 1
lower = 0
tIndex = -1
prev = 0
counter = 0


# encoding
for index in flattened:
    for i in freq:
        if i == index:
            break
        prev += freq[i]
    if counter == BlockSize:
        counter = 0
        tIndex += 1
        tags[tIndex] = (lower + upper)/2
        lower = 0
        upper = 1
        constUpper = 1
    upper = lower + (upper-lower)*(prev + freq[index])
    lower = lower + (constUpper-lower)*prev
    constUpper = upper
    counter += 1
    prev = 0

tIndex += 1
tags[tIndex] = (lower + upper)/2
tags.tofile('tags.npy')
print(tags)