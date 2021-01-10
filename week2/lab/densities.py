# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 17:41:38 2020

@author: lenaw
"""

from osgeo import gdal, ogr
from osgeo.osr import SpatialReference
from tqdm import tqdm

# load the sources
data_source = ogr.GetDriverByName('GPKG').Open("Amsterdam_BAG.gpkg", update=0)
centroid_source = ogr.GetDriverByName('GPKG').Open('centroids.gpkg', update=1)


# open the surface layer Wijken 
layer_wijken = data_source.GetLayerByName('Wijken')
# open the centroids layer from centroid_source
centroids = centroid_source.GetLayerByName('centroids')
# open the density layer from centroid_source
density =  centroid_source.GetLayerByName('density') 


# create new output layer for density in the centroids dataset
# use the same CRS
rdNew = SpatialReference()
rdNew.ImportFromEPSG(28992)

# check to see of density layer already exists and remove it
if centroid_source.GetLayerByName('density'):
    centroid_source.DeleteLayer('density')
    print('Layer density removed!\n')
      
#add new layer to the dataset
density_layer = centroid_source.CreateLayer('density', srs=rdNew, geom_type=ogr.wkbPoint)

# add fields to the density layer
# name
field_name = ogr.FieldDefn('name', ogr.OFTString)
density_layer.CreateField(field_name)

# density
field_density = ogr.FieldDefn('density', ogr.OFTReal)
density_layer.CreateField(field_density)

# fraction
field_fraction = ogr.FieldDefn('fraction', ogr.OFTReal)
density_layer.CreateField(field_fraction)


#Look for the names ofs fields
locations_def = layer_wijken.GetLayerDefn()
num_fields = locations_def.GetFieldCount()
print("Task4: The number of fields ",num_fields)

#task 4: print the name and type of each field in the layer
for i in range(0,num_fields):
    print("Name of field:",locations_def.GetFieldDefn(i).GetName())
    print("Type of field", locations_def.GetFieldDefn(i).GetTypeName())
    
    
#3. Iterate over the districts. For each district
#a. Get the name and the size of the area of the current district, and initialise variables to store the
#number and areas of houses
layer_def = layer_wijken.GetLayerDefn()
num_fields = layer_def.GetFieldCount()
num_features = layer_wijken.GetFeatureCount()

for i in range(1,num_features+1):    
    feature = layer_wijken.GetFeature(i)
    name = feature.GetField('Buurtcombinatie')
    geometry = feature.GetGeometryRef()
    print(name, geometry.GetArea())

#b. Iterating over a layer works once. For a repeated iteration over a layer you need to use
#   ResetReading() before you attempt to iterate another time:
#   centroid_layer.ResetReading()
    
#c. For each centroid test whether it is in the current district geometry. 
#   If so, accumulate the number and area. 
#   You can use Within to test the geometries:
density_layer_def = density_layer.GetLayerDefn()
    
for x in tqdm(range(1, layer_wijken.GetFeatureCount()+1)):  #for each feature in the districts layer
    district_feature = layer_wijken.GetFeature(x) #get the specific feature of layer
    district_geometry = district_feature.GetGeometryRef() #get the geometry of the feature
    centroid = district_geometry.Centroid() # get the centroid of the geometry (feature)
    district_area = district_geometry.GetArea() #get the area of the geometry
    name = district_feature["Buurtcombinatie"] #get the district name
    
    houses = 0
    area = 0
    
    centroids.ResetReading() 
    
    for y in range(1, centroids.GetFeatureCount()+1):  #for each feature in centroids layer    

        centroid_feature = centroids.GetFeature(y) 
        centroid_geometry = centroid_feature.GetGeometryRef()
        
        if centroid_geometry.Within(district_geometry):
            houses += 1
            area += centroid_feature.area

    #d. Compute the density and fraction and assign these with the name of the 
    #   current district to the output layer               
    density = houses / (district_area / 1000000) 
    fraction = area / district_area * 100
    
    point_feature = ogr.Feature(density_layer_def) # create a new feature 
    point = ogr.Geometry(ogr.wkbPoint) # create a point geometry
    point.AddPoint(centroid.GetX(), centroid.GetY()) # set the coordinates of this point
    point_feature.SetGeometry(point)  
    point_feature.SetField('name', name) 
    point_feature.SetField('density', density)
    point_feature.SetField('fraction', fraction)
    
    density_layer.CreateFeature(point_feature)
            
#d. Compute the density and fraction and assign these with the name of the current district to the output
#layer    

## Question: What is the density of the district with feature id 54 (Museumkwartier)?
c_db = ogr.GetDriverByName('GPKG').Open("centroids.gpkg", update=0)
density = c_db.GetLayerByName('density')
density.GetFeature(54).GetField("density")

