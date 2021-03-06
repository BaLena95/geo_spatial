# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 21:12:39 2020

@author: lenaw
"""

import json
from osgeo.osr import SpatialReference, CoordinateTransformation
from osgeo import ogr, gdal

#Assign the CRS to Amersfoort
rdNew = SpatialReference()
rdNew.ImportFromEPSG(28992)

#Create the dataset and add a layer with:
#ogr_ds = ogr.GetDriverByName('GPKG').CreateDataSource('schools.gpkg')
#point_layer = ogr_ds.CreateLayer('locations', srs=rdNew, geom_type=ogr.wkbPoint)

# source for then new layers
school_source = ogr.GetDriverByName('GPKG').Open('schools.gpkg', update=1)
#check if it already exists and remove
if school_source.GetLayerByName('locations'):
    school_source.DeleteLayer('locations')
    print('Layer districts removed!!!') 
#create new layer  
point_layer = school_source.CreateLayer('locations', srs=rdNew, geom_type=ogr.wkbPoint)

# add a new layer buffer. The layer will be used to store the new features.
rdNew = SpatialReference()
rdNew.ImportFromEPSG(28992)

#check if buffer layer exists alreadry and remove it
if school_source.GetLayerByName('districts'):
    school_source.DeleteLayer('districts')
    print('Layer districts removed!!!')

#add new layer districts to the dataset
districts_layer = school_source.CreateLayer('districts', srs=rdNew, geom_type=ogr.wkbMultiPolygon)
districts_layer_def = districts_layer.GetLayerDefn()


#load data 
with open('schools.json') as json_file:
    school_data = json.load(json_file)

#set CRS
# schools data is given in WGS84
wgs84 = SpatialReference()
wgs84.ImportFromEPSG(4326)
wgs_to_rd = CoordinateTransformation(wgs84, rdNew)

point_layer_def = point_layer.GetLayerDefn()

#iterate over all schools and assign each school a latitude and longitude to a point
for s in school_data['results']:
    latitude=s['coordinaten']['lat']
    longitude=s['coordinaten']['lng']
    #eliminate 0,0 points to not add schools with no coordinates
    if not(latitude==0 and longitude==0):
        point = wgs_to_rd.TransformPoint(latitude, longitude)
        rd_x=point[0]
        rd_y=point[1]
        feature = ogr.Feature(point_layer_def)
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(rd_x, rd_y)
        feature.SetGeometry(point)
        point_layer.CreateFeature(feature)
        