# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 10:32:15 2020

@author: lenaw
"""

#load pcraster
from pcraster import *
import os


print(os.getcwd())

#change the directory to the maps data
os.chdir(r"C:\Users\lenaw\Documents\data\dynmod\snowmelt")
print(os.getcwd())

#load dm Map
demMap=readmap("dem.map")
# load anArea Map
anAreaMap=readmap("anArea.map")

aguila(anAreaMap, demMap)
aguila("-3", "dem.map","+","anArea.map") 

aguila("dem.map","+","anArea.map")

# Question: What is shown on anArea.map?
# a True cells represent the higher part of the study area

#2.1.2. Temporal spatial data

#check directory in dataset
print(dir())

#display time steps
aguila('--timesteps=[1,181,1]','precip')

aguila('--timesteps=[60,181,10]', 'precip')
# 60 = first time step
# 181 = last time step
# 10 = number of time step between the maps

#Question: Compare the precipitation pattern with the elevation map 
# (open them in one view, using a single Aguila command). 
# What is the relation between precipitation and elevation?

# b The higher the elevation, the higher the precipitation. 
aguila(demMap)

# 2.1.3 Temporal non-spatial data

#check type
type("precip.tss")
# type str

aguila("precip.tss")

# 2.2 The dynamic modelling framework




