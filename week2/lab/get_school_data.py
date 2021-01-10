# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 21:00:04 2020

@author: lenaw
"""
#use python request module to perform request in Schoolwijyer API
import requests
import json
from osgeo.osr import SpatialReference, CoordinateTransformation
from osgeo import ogr, gdal

# import the data
schools = requests.get('https://schoolwijzer.amsterdam.nl/api/v1/lijst/po', verify=False)
schools = schools.json()

# Task: Create a Python script get_school_data.py that executes an API request to the OpenData API, 
# and writes the result to a file named schools.json. 
# Use Python’s json module to write the file to disk.

with open('schools.json', 'w') as f:
    json.dump(schools, f)
f.close()

# Assign CRS
rdNew = SpatialReference()
rdNew.ImportFromEPSG(28992)

rdWSG84 = SpatialReference()
rdWSG84.ImportFromEPSG(4326)

# Create dataset and add layer
ogr_ds = ogr.GetDriverByName('GPKG').CreateDataSource('schools.gpkg')
point_layer = ogr_ds.CreateLayer('locations', srs=rdNew, geom_type=ogr.wkbPoint)

with open('schools.json') as f:
    school_data = json.load(f)
    
print(type(school_data))

# Task: Complete your Python script to create the school layer and run it.

wgs_to_rd = CoordinateTransformation(rdWSG84, rdNew) # create transformation for the reference systems

# For better orientation name, id and bring were added to the layer:
field1 = ogr.FieldDefn('name', ogr.OFTString) 
field2 = ogr.FieldDefn('id', ogr.OFTInteger)
field3 = ogr.FieldDefn('brin', ogr.OFTString)

# Add the fields to the layer: 
point_layer.CreateField(field1)
point_layer.CreateField(field2)
point_layer.CreateField(field3)

#defenition for the layer
feature_def = point_layer.GetLayerDefn()

for i in school_data.get('results'): # loop through all schools
    coordinaten = i.get('coordinaten') # dict.
    latitude = coordinaten.get('lat') # latitude
    longitude = coordinaten.get('lng') # longitude
    
    
    if latitude != 0 and longitude != 0:  # only coordinates not zero:
        schoolpoint = wgs_to_rd.TransformPoint(latitude, longitude) # transform RS
        rd_x = schoolpoint[0]  # get the x and y an name it
        rd_y = schoolpoint[1]
        
        feature = ogr.Feature(feature_def) # initialize feature
        point = ogr.Geometry(ogr.wkbPoint) # initialize point
        point.AddPoint(rd_x, rd_y) # set values to point
        feature.SetGeometry(point) # add point to feature
        
        name = i.get('naam') # name school
        school_id = i.get('id') # id school
        brin = i.get('brin') # brin school
        
        # add values of fields to feature: 
        feature.SetField('name', name)
        feature.SetField('id', school_id)
        feature.SetField('brin', brin)
        point_layer.CreateFeature(feature)
        
        
        