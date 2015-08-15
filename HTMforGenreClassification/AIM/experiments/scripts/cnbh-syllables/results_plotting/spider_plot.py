#!/usr/bin/env python
"""
spider_plot.py

Created by Thomas Walters on 2010-09-12.
"""

import sys
import getopt
import matplotlib as mpl
mpl.use('PDF')
import numpy as np
import pylab as p
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import cm
import matplotlib.ticker as ticker 

help_message = '''
Plot the spider.

Arguments:
-i --input_file
-o --output_file
'''

class Usage(Exception):
  def __init__(self, msg):
    self.msg = msg


def main(argv=None):
  if argv is None:
    argv = sys.argv
  try:
    try:
      opts, args = getopt.getopt(argv[1:], "hi:o:",
                                 ["help", "input_file=", "output_file="])
    except getopt.error, msg:
      raise Usage(msg)
  
    # defaults
    input_file = "results_iteration_15.txt"
    output_file = "results_iteration_15.png"
    
    # option processing
    for option, value in opts:
      if option in ("-h", "--help"):
        raise Usage(help_message)
      if option in ("-i", "--input_file"):
        input_file = value
      if option in ("-o", "--output_file"):
        output_file = value
  
  except Usage, err:
    print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
    print >> sys.stderr, "\t for help use --help"
    return 2
  
  central_vtl=15
  central_vtl_scaling=112.32
  
  # Read in a file with lines in the form
  # Pitch Scale Percentage
  xs=[]
  ys=[]
  zs=[]
  f = open(input_file, 'r')
  for line in f:
    if line[0] != "#":
      values = line.strip().split(' ')
      xs.append(central_vtl*central_vtl_scaling/float(values[1]))
      ys.append(float(values[0]))
      zs.append(float(values[2]))


  # Define a tiny sphere, centered on the origin, which
  # we'll shift to the desired position. 
  u=np.r_[0:2*np.pi:50j]
  v=np.r_[0:np.pi:50j]
  sx=0.01*np.outer(np.cos(u),np.sin(v))
  sy=0.01*np.outer(np.sin(u),np.sin(v))
  sz=2.5*np.outer(np.ones(np.size(u)),np.cos(v))

  fig=p.figure()
  ax = p3.Axes3D(fig, azim=-80, elev=60)

  colormap = cm.get_cmap('jet', 100)

  # Note: here I fake out the lack of proper logarihmic scales on 3D axes in
  # matplotlib by just plotting log values on a linear scale and renaming
  # the labels.
  # (This doesn't work: ax.w_yaxis.set_scale('log') ax.w_xaxis.set_scale('log'))

  # Plot the values seven at a time as dark lines.
  # These are the individual spokes of the spoke pattern.
  n=7
  for i in xrange(0,8):
    ax.plot(np.log(xs[i*n:(i+1)*n]), np.log(ys[i*n:(i+1)*n]), zs[i*n:(i+1)*n], color=[0,0,0])

  for x,y,z in zip(xs,ys,zs):
    ax.plot(np.log([x, x]), np.log([y, y]), [z, 0], color=[0.8,0.8,0.8])
    ax.plot_surface(sx+np.log(x),sy+np.log(y),sz+z, color=colormap(int(z)), linewidth=0)

  ax.set_ylabel('GPR/Hz')
  ax.set_xlabel('VTL/cm')
  ax.set_zlabel('Percent correct')
  ax.set_ylim3d(np.log([131,225]))
  ax.set_xlim3d(np.log([9.9, 22.1]))
  ax.set_zlim3d([-1, 101])
  ax.w_zaxis.set_major_locator(ticker.FixedLocator([0, 20, 40, 60, 80, 100]))

  ax.w_xaxis.set_major_locator(ticker.FixedLocator(np.log([10,15,22])))
  ax.w_xaxis.set_ticklabels(['10', '15', '22'])
  ax.w_yaxis.set_major_locator(ticker.FixedLocator(np.log([132, 172, 224])))
  ax.w_yaxis.set_ticklabels(['132', '172', '224'])

  #for a in ax.w_xaxis.get_ticklines()+ax.w_xaxis.get_ticklabels(): 
  #    a.set_visible(False) 

  #for a in ax.w_yaxis.get_ticklines()+ax.w_yaxis.get_ticklabels(): 
  #    a.set_visible(False) 


  #p.show()
  p.savefig(output_file)

if __name__ == "__main__":
  sys.exit(main())
