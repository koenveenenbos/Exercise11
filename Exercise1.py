# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from osgeo import gdal
from osgeo import osr
from osgeo import ogr
from osgeo.gdalconst import GA_ReadOnly, GDT_Float32
import numpy as np
import os


os.chdir('/home/ubuntu/userdata/Lesson11/ospy_data4/')

filename = './aster.img'
dataSource = gdal.Open(filename, GA_ReadOnly)

print '\nInformation about ' + filename
print 'Driver: ', dataSource.GetDriver().ShortName,'/', \
      dataSource.RasterCount
print 'Size is ',dataSource.RasterXSize,'x',dataSource.RasterYSize, \
      'x',dataSource.RasterCount

print '\nProjection is: ', dataSource.GetProjection()

print '\nInformation about the location of the image and the pixel size:'
geotransform = dataSource.GetGeoTransform()
if not geotransform is None:
    print 'Origin = (',geotransform[0], ',',geotransform[3],')'
    print 'Pixel Size = (',geotransform[1], ',',geotransform[5],')'

# Read data into an array
band2Arr = dataSource.GetRasterBand(2).ReadAsArray(0,0,dataSource.RasterXSize, dataSource.RasterYSize)
band3Arr = dataSource.GetRasterBand(3).ReadAsArray(0,0,dataSource.RasterXSize, dataSource.RasterYSize)
print type(band2Arr)

# Read data into an array
band2Arr=band2Arr.astype(np.float32)
band3Arr=band3Arr.astype(np.float32)

# Derive the NDVI
mask = np.greater(band3Arr+band2Arr,0)

# set np.errstate to avoid warning of invalid values (i.e. NaN values) in the divide 
with np.errstate(invalid='ignore'):
    ndvi = np.choose(mask,(-99,(band3Arr-band2Arr)/(band3Arr+band2Arr)))
print 'NDVI min and max values', ndvi.min(), ndvi.max()

# Check the real minimum value
print ndvi[ndvi>-99].min()


# Write the result to disk
driver = gdal.GetDriverByName('GTiff')
outDataSet = driver.Create('./ndvi.tif', dataSource.RasterXSize, dataSource.RasterYSize, 1, GDT_Float32)
outBand = outDataSet.GetRasterBand(1)
outBand.WriteArray(ndvi,0,0)
outBand.SetNoDataValue(-99)

# Set the projection and extent information of the dataset
outDataSet.SetProjection(dataSource.GetProjection())
outDataSet.SetGeoTransform(dataSource.GetGeoTransform())

# Save or Flush the data
outBand.FlushCache()
outDataSet.FlushCache()
