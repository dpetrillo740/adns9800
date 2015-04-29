import sys, serial, argparse
from collections import deque
import numpy

import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import matplotlib.cm as cm

    
# plot class
class AnalogPlot:
  # constr
  def __init__(self, strPort):      
      # open serial port
      self.ser = serial.Serial(strPort)
      raw = self.ser.readline()

  # update plot
  def update(self, frameNum):

      try:
          raw = self.ser.readline()
          raw = raw[:-3]
          raw = numpy.matrix(raw)
          raw = raw.astype(float)
          for x in numpy.nditer(raw, op_flags=['readwrite']):
              x[...] = x/127

      except KeyboardInterrupt:
          print('exiting')
      
      return raw
  
  
  # clean up
  def close(self):
      # close serial
      self.ser.flush()
      self.ser.close()

# main() function
def main():
  # create parser
  parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
  parser.add_argument('--port', dest='port', required=True)

  # parse args
  args = parser.parse_args()
  
  #strPort = '/dev/tty.usbserial-A7006Yqh'
  strPort = args.port

  print('reading from serial port %s...' % strPort)

  # plot parameters
  analogPlot = AnalogPlot(strPort)

  print('plotting data...')

  # set up animation
  plt.ion()
  plt.axis('off') # clear x- and y-axes
  

  
  # show plot
  pic = plt.imshow(analogPlot.update(), cmap = cm.Greys_r)
  pic.set_data(analogPlot.update())
  plt.draw()
  
  fig = plt.figure()
  anim = animation.FuncAnimation(fig, analogPlot.update, interval=50)
  
  # clean up
  analogPlot.close()

  print('exiting.')
  

# call main
if __name__ == '__main__':
  main()
