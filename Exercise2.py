# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 10:50:44 2017

@author: ubuntu
"""

# Notebook magic to select the plotting method
# Change to inline to plot within this notebook
#%matplotlib inline 
import os

os.chdir('/home/ubuntu/userdata/Lesson11/ospy_data4/')

from osgeo import gdal
import matplotlib.pyplot as plt

dsll = gdal.Open("./ndvi_ll.tif")

ndvi = dsll.ReadAsArray(0, 0, dsll.RasterXSize, dsll.RasterYSize)

plt.imshow(ndvi, interpolation='nearest', vmin=0, cmap=plt.cm.gist_earth)
plt.show()

dsll = None
