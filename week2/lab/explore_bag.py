# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 14:32:58 2020

@author: lenaw
"""
# 2.1 

from osgeo import gdal, ogr

# loading the data
filename = 'Amsterdam_BAG.gpkg'
data_source = ogr.GetDriverByName('GPKG').Open(filename, update=0)

#Task1: Print the number of Layers Included in Dataset:
# get number of layers with
print("Task1: ",data_source.GetLayerCount())
print("End TASK \n")

# print the CRS for the layers
layer = data_source.GetLayerByIndex()
srs = layer.GetSpatialRef()
print("Task2: Used CRS \n\n", srs)
print("End Task2 \n")

# print feature count of each layer
buildings = data_source.GetLayerByName('Verblijfsobject')
number_ft_buildings = buildings.GetFeatureCount()
print("Feature count of Verblijfsobject:\n", number_ft_buildings)

surface_area = data_source.GetLayerByName('Pand')
number_ft_area = surface_area.GetFeatureCount()
print("Feature count of Pand:\n", number_ft_area)

districts = data_source.GetLayerByName('Wijken')
number_ft_districts = districts.GetFeatureCount()
print("Feature count of Wijken:\n", number_ft_districts )
print("End Task3 \n")


locations_def= buildings.GetLayerDefn()
surface_def= surface_area.GetLayerDefn()
districts_def =districts.GetLayerDefn()

# buildings
print("Definition of Layer buildings:\n", buildings.GetLayerDefn())
# number of fields in the layer
print("Number of fields in buildings:\n", locations_def.GetFieldCount())

# surface_area
print("Definition of Layer surface_area:\n", surface_area.GetLayerDefn())
# number of fields in the layer
print("Number of fields in surface_areas:\n\n", surface_def.GetFieldCount())

# districts
print("Definition of Layer districts:\n", districts.GetLayerDefn())
# number of fields in the layer
print("Number of fields in district:\n\n", districts_def.GetFieldCount())

# Names and Type of each layer
# buildings
print("Name of field: \n", locations_def.GetFieldDefn(1).GetName())
print("Type of field:\n", locations_def.GetFieldDefn(1).GetTypeName())     
print("End Task4 \n")

#task 4: print the name and type of each field in the layer
num_fields = locations_def.GetFieldCount()
print("Task4: Number of fields ",num_fields, "\n")

# just layer Verblijfsobject 
for i in range(0,num_fields):
    print("Name of field:",locations_def.GetFieldDefn(i).GetName())
    print("Type of field", locations_def.GetFieldDefn(i).GetTypeName())


# task 5: value of field "oppervlakte" (surface area) with all features in the layer added up
num_features = buildings.GetFeatureCount()
print("Number of features:", num_features)

field_name = "oppervlakte"
area = 0
for i in range(1,num_features+1):
    
    feature = buildings.GetFeature(i)
    field_value = feature.GetField(field_name)
    area = area + field_value
print("Total area:", area, "\n\n")
# Question: What is the total surface area given in the location layer?
# Anwer: The total surface area in the location layer is "Total area: 59255192"     

# query individual features with index through geometry
feature = buildings.GetFeature(439774)
geometry = feature.GetGeometryRef()
print(geometry)
print("X coordinate", geometry.GetX())
print("Y coordinate", geometry.GetY()) 

# Question: What is the coordinate of the feature with the index 439774
# Answer: POINT (121815.991 487912.647 0)
# X 121815.991
# Y 487912.647



