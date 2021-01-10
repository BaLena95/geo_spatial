# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 14:07:33 2020

@author: lenaw
"""

from osgeo.osr import SpatialReference, CoordinateTransformation
from osgeo import ogr, gdal

# Add a new layer away to your dataset.
# Afterwards, use the appropriate OGR operation to fill the away layer.

# add CRS
rdNew = SpatialReference()
rdNew.ImportFromEPSG(28992)

# data sources for layers
# merge
data_source = ogr.GetDriverByName('GPKG').Open('schools.gpkg', update=1)

# districts
districts = data_source.CreateLayer('districts', srs=rdNew, geom_type=ogr.wkbMultiPolygon)

# Compute the area far from schools:
merge_layer = merge
districts_layer = districts

# and add a new layer away 
away = data_source.CreateLayer('away', srs=rdNew, geom_type=ogr.wkbMultiPolygon)
away_feature_def = away.GetLayerDefn() # define new layer
away_feature = ogr.Feature(away_feature_def)

districts_layer.SymDifference(merge_layer, away)

feature_away = away.GetFeature(1)
gem_away = feature_away.GetGeometryRef()

print('The area "far away" from schools in m2 is: ', gem_away.GetArea())


