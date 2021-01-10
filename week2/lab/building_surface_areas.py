# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 18:31:36 2020

@author: lenaw
"""
from osgeo import gdal, ogr
from osgeo.osr import SpatialReference

data_source = ogr.GetDriverByName('GPKG').Open("Amsterdam_BAG.gpkg", update=0)
surface = data_source.GetLayerByName('Pand')

# create a new layer to store the centroids
# assign a CRS to the new layer - Amersfoort / RD New (28992).
rdNew = SpatialReference()
rdNew.ImportFromEPSG(28992)

# Create the new dataset with an output layer centroids ny using the point geometry type:
centroid_source = ogr.GetDriverByName('GPKG').CreateDataSource('centroids.gpkg')
centroid_layer = centroid_source.CreateLayer('centroids', srs=rdNew, geom_type=ogr.wkbPoint)

# Task: Add field area the layer centroids.
field = ogr.FieldDefn('area', ogr.OFTReal)
centroid_layer.CreateField(field)

# first need to get feature definition
centroid_layer_def = centroid_layer.GetLayerDefn()


# Task: Calculate the area and the centroid location of each building.
# using a loop to iterate over each feature
for i in range(1, surface.GetFeatureCount()):
    feature = surface.GetFeature(i)
    house_geometry = feature.GetGeometryRef()
    point_feature = ogr.Feature(centroid_layer_def) # get the definition for the new feature 
    point = ogr.Geometry(ogr.wkbPoint)
    
    centroid = house_geometry.Centroid() # apply centroid
    point.AddPoint(centroid.GetX(), centroid.GetY()) #  point geometry for feature
    point_feature.SetGeometry(point) # place of the centroid to the new point
    
    house_area = house_geometry.GetArea()
    # set the value of a field and add feature to the layer
    point_feature.SetField('area', house_area)
    centroid_layer.CreateFeature(point_feature)