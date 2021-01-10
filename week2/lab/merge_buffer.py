# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 13:55:00 2020

@author: lenaw
"""

from osgeo.osr import SpatialReference, CoordinateTransformation
from osgeo import ogr, gdal

data_source = ogr.GetDriverByName('GPKG').Open('schools.gpkg', update=1)
buffer_layer = data_source.GetLayerByName('buffer')

# and add a new layer merge 
rdNew = SpatialReference()
rdNew.ImportFromEPSG(28992)

merge = data_source.CreateLayer('merge', srs=rdNew, geom_type=ogr.wkbMultiPolygon)
merge_feature_def = merge.GetLayerDefn() # define new layer
# Add a new feature, merge_feature and initialize it with the geometry of the first
# feature of the buffer layer. After that, iterate over the rest of the buffer layers
# to merge the rest of the buffer layer. 

buffer_feature = buffer_layer.GetNextFeature() # get first feature of buffer
buffer_geometry = buffer_feature.GetGeometryRef()

merge_feature = ogr.Feature(merge_feature_def) # initialize the merge_feature
merge_feature.SetGeometry(buffer_geometry)
merge_geometry = merge_feature.GetGeometryRef() # set the merge_geometry

for i in range(1,len(buffer_layer)):
    buffer_feature = buffer_layer.GetNextFeature()
    buffer_geometry = buffer_feature.GetGeometryRef()
    
    union = merge_geometry.Union(buffer_geometry)
    merge_feature.SetGeometry(union)
    merge_geometry = merge_feature.GetGeometryRef() 
    
# Save the new feature to the the merge layer
merge.CreateFeature(merge_feature)

