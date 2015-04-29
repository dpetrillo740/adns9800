import serial
import numpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

ser = serial.Serial('/dev/cu.usbmodem1421')
raw = ser.readline()

def getmatrix():
    raw = ser.readline()
    raw = raw[:-3]
    raw = numpy.matrix(raw)
    raw = raw.astype(float)
    for x in numpy.nditer(raw, op_flags=['readwrite']):
        x[...] = x/127
    return raw

plt.ion()
plt.axis('off') # clear x- and y-axes
b = getmatrix()
pic = plt.imshow(b, cmap = cm.Greys_r)


for y in range(10000):
    b = getmatrix()
    pic.set_data(b)
    plt.draw()
