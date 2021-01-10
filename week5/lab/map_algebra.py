# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 10:09:50 2020

@author: lenaw
"""
#lab can be found here:
    #http://karssenberg.geo.uu.nl/labs/mapalgebra/pcrasterMaps.html

#load pcraster
from pcraster import *

import os
print(os.getcwd())

#change the directory to the maps data
os.chdir(r"C:\Users\lenaw\Documents\data\mapalgebra")
print(os.getcwd())

#load a map
waterMap=readmap("water.map")

#visualize the map
aguila(waterMap)

#read isroad.map
isroadMap=readmap("isroad.map")
#visualize map
aguila(isroadMap)

#to have the same cursor position on Maps
# open at once
aguila(isroadMap, waterMap)

#read topo map
topoMap=readmap("topo.map")
aguila(topoMap)

#1.1.3 Data types
#Question: What is the data type of buildg.map?

#load the map
buildMap= readmap("buildg.map")
aguila(buildMap)

#Answer: B  
# It's a nominal data type as the buildings are classified with different 
# categories but without order

# 1.2.1 Introduction
#read all maps and assignes corresponding variable names
#reload all maps with this after closing python
############################
exec(open("openmaps.py").read())

# new maps can be created from existing like:
resultMap = slope(topoMap) * (1 + phreaticMap)
aguila(resultMap)

#1.2.2 Quantitative computation with scalar maps
# to create overlay with depth of unsaturated zon
#subtract phreatic level from each raster cell
unsatMap = topoMap - phreaticMap
aguila(unsatMap)

# calculate map with depth of unsaturated zone in mm
unsatmmMap= unsatMap*100
aguila(unsatmmMap)

# try to determine a map with the infiltration rate
# on basis of the soil type
infilMap = soilsMap * unsatMap

#doesn't work:
#RuntimeError: pcrmul: left operand of operator '*': type is nominal, legal type is scalar

#Question: Why is it not possible to multiply soilsMap with unsatMap?
#B The data type of soilsMap is nominal, and nominal data types do not allow multiplication.

#1.2.3 Boolean algebra operations
# find bridges were water and roads intersect
isbridgeMap = isroadMap & iswaterMap

# display 
aguila(isroadMap, iswaterMap, isbridgeMap)
#true = bridges

#other boolean operators
x1Map = isroadMap & iswaterMap 
x2Map = isroadMap | iswaterMap 
x3Map = isroadMap ^ iswaterMap 
x4Map = isroadMap & ~ iswaterMap 

#visualize maps
aguila(x1Map, x2Map, x3Map, x4Map)
aguila(x1Map)

#Question: Which of the cross tables belongs to x1Map = isroadMap and iswaterMap?
#A table A

#Question: Which of the cross tables belongs to x2Map = isroadMap | iswaterMap?
aguila(x2Map)
# C Table C

# Question: Which of the cross tables belongs to x3Map = isroadMap ^ iswaterMap?
aguila(x3Map)
# D Table D

# Question: Which of the cross tables belongs to x4Map = isroadMap & ~ iswaterMap?
aguila(x4Map)
# B Table B

#1.2.4. Comparison operators resulting in boolean maps
# true/false boolean assigned cells
highMap = topoMap > 40
aguila(highMap)

# example for building map
testMap = topoMap > (0.234 * 19)

# same map with buildings
aguila(buildMap)

#create mao with mines in it
# legend =5
isMineMap=buildMap==5
aguila(isMineMap)

#Question: What command did you use to get isMineMap.
# B #isMineMap=buildMap==5

#1.2.5 Conditional operators with a boolean map

#ifthen operator
# elevation at the mine
topatminMap = ifthen(isMineMap, topoMap)
aguila(topatminMap)

#ifthenelse operator
topoNewMap=ifthenelse(isMineMap, topoMap-20, topoMap)
aguila(topoMap)

#Question What is the lowest elevation value on toponewMap?
# a. 1.0

#1.3. Area operations for descriptive statistics
#average elevation in the same class 
soiltopoMap = areaaverage(topoMap, soilsMap)
aguila(soiltopoMap, topoMap, soilsMap)

#Question: What is calcualated by the areaaverage operation in this case?
# A. The operation assigns to each cell the average elevation value of cells in a map that belong to the same area (class on soilsMap) as the cell itself.

# to assign the area of the soil class to which each cell belongs
soilareaMap = areaarea(soilsMap)
aguila(soilareaMap, soilsMap)

#Question: What is name or cell code of the soil class that covers the largest area in the study area?
# c Boulder clay, with cell code 10.

#1.3.3 Finding continuous areas; a study problem

# voolean map with true cell values for patches with pine that is big enough
# for logging and FALSE for cells of remaining area

aguila(treesMap)

#open, code 0
#pine, code 1
#deciduous, code 2
#mixed wood, code 3

pineMap=treesMap==1
aguila(pineMap)

# to determine size of each patch of pine-trees
# separation in continuous areas in pineMap
# using clump operator
pineclumMap = clump(pineMap)
aguila(pineclumMap, pineMap)

# calculate map that contains the area of each clump
# in the map with areaarea operator
pineareaMap=areaarea(pineclumMap)
aguila(pineareaMap,pineMap)

#changing the values of area without pine trees to 0
pineare2Map = ifthenelse(pineMap, pineareaMap, 0)
aguila(pineMap, pineare2Map)

#Question What is the data type of pineare2Map?
# NOT B ordinal 
#submitted wrong answer

# find contiguous areas with pines larger than 4 hectares
pines4hec=ifthen(pineare2Map> 40000, pineare2Map)
aguila(pines4hec)
# B 2

# 1.4. Neighbourhood operations:
    #windows, frictions paths, visibility analysis

#window average operation
#Result = windowaverage(expression, windowlength) 
#use unsatMap
unsatMap = topoMap - phreaticMap

#windowaverage
unsat150Map  = windowaverage(unsatMap,150)
unsat250Map  = windowaverage(unsatMap,250)

#Question: What is the size of the window, counted in number of cells,
# used for the calculation of unsat150Map? 
# Keep in mind that the size of one cell is equal to 50 by 50 metres!
150/50
# C 3 cells by 3 cells

#Question: How does the windowaverage operator affect the frequency distribution of the values in the maps?
# A The windowaverage operator decreases the variation in the map and thus the frequency distribution. The larger the window, the more the variation is diminished.

#spatial diversity of area can be studied with windowdiversity operator
# input expression must have a data type boolean, nominal or ordinal
soidi150Map = windowdiversity(soilsMap,150)
aguila(soidi150Map)

#Question: Explain the operation performed by the windowdiversity operator.
#A The windowdiversity operator finds the number of different cell values within a window and assigns this number to the cell for the result.

#1.4.3 Entire neighbourhood operations:
    #absolute distance calculation
# calculate for each cell the shortest distance to non zero cell values on a boolean, nominal or ordinal map    
# Result = spread(pointsexpression, initialdist, friction)    

aguila(wellsMap)
welldistMap = spread(wellsMap,0,1)
aguila(welldistMap)

#create boolean map wellprotMap True for area within 200m distance to well
wellprotMap= ifthen(welldistMap<200, welldistMap)
aguila(wellprotMap)

#Question: For how many wells do their protection zones overlap (or are connected)?
# A 2
#fo under 200m, when 201 it's 4

#1.4.4 Entire neighbourhood operations:relative distance calculation

#calculating travel time of water from the nearest well to each cell
# 3 seconds per meter
welltimeMap = spread(wellsMap,0,3)
aguila(welltimeMap)
#shows for each cell how long the water would take to get there from the nearest well

#1.5. Neighbourhood operations: DEm and catchment analysis
#1.5.2 Creating slope and spects maps

#slope operator generated slope map of digital elevation
slopeMap = slope(topoMap)
aguila(slopeMap, topoMap)

#atan operator - slope given as an angle
slopedegMap = atan(slopeMap)

#gives change in slope
slope2Map = slope(slopeMap)

#map of slope aspect in degrees
aspectMap = aspect(topoMap)

#1.5.3 Creating the local drain direction map

#lddcreate operator is used to generate a local drain direction map
#Result = lddcreate(dem, outflowdepth, corevolume, corearea, precipitation)

#pit removing thresholds to zero
ldd0Map = lddcreate(topoMap,0,0,0,0)
aguila(topoMap, ldd0Map)

# A pit cell is surrounded by cells at a greater elevation than the pit cell itself. 
# As result, a pit cell cannot drain to a neighbouring cell

pit0Map = pit(ldd0Map)
aguila(topoMap, pit0Map)

# flow paths of water and were they stop (drain direction map)
aguila(pointsMap)
pathzeroMap = path(ldd0Map,pointsMap)
aguila(ldd0Map, pointsMap, pit0Map, pathzeroMap)

# pit always at the cell with the smallest elevation 
#contains water when filled until overflow point is reached
#fill pits in elevation model with lddcreatedem
topomodiMap = lddcreatedem(topoMap,1e31,1e31,1e31,1e31)

#differences between topoMap and topomodiMap
coredeptMap = topomodiMap - topoMap
aguila(coredeptMap)

#Question: What is the maximum depth of the largest core in the map (in metres)?
# d. 3

#remove the pits form local drain direction map
#pits with dimesnions smaller than thresholds dimensions will be removed

#removes all pits except with depth larger or equal to 2 metre
ldd2Map = lddcreate(topoMap,2,1e31,1e31,1e31)
pit2Map = pit(ldd2Map)

#removing pits on sides with high threshols values 
lddMap = lddcreate(topoMap,10,1e31,1e31,1e31)

#calculate downstream paths
pathMap = path(lddMap, pointsMap)
aguila(pathMap)
#paths end at outflow cell 

#1.5.4. Catchment analysis and routing with the ldd map

#catchment of all outflow points determined with the catchment operator

#use pit operator to create nonimnal map with outflow points
outpoMap=pit(lddMap)
#then catchment 
catchmsMap = catchment(lddMap,outpoMap)
aguila(catchmsMap)

#main use is routing of surface water in downstram direction
#Result = accuflux(ldd,material)

#rainstorMap gives amount and dis. of rain 
#discharge in study area as a result of rainsorms is calculated as
dischMap = accuflux(lddMap,rainstorMap)
aguila(dischMap, rainstorMap, lddMap)

#Question: What is the maximum value of the total discharge (m3) as a result of the thunderstorm? 
#a 1179.69

#better picture of the spatial pattern of the discharge
#use logarithm
dischlogMap = log10(dischMap)
aguila(dischlogMap)


#area of each cell to calculate upstram area
#contains catchment that drains into each cell
upareMap = accuflux(lddMap,2500)
aguila(upareMap, lddMap)

