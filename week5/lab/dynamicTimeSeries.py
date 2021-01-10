from pcraster import *
from pcraster.framework import *

os.chdir(r"C:\Users\lenaw\Documents\data\dynmod\snowmelt")

class MyFirstModel(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)
    setclone('dem.map')

  def initial(self):
    pass

  def dynamic(self):
    precipitation=timeinputscalar('precip.tss',1)
    self.report(precipitation,'pre2_3')

#1 = to assign the values in the timeseries to the whole map

nrOfTimeSteps=181
myModel = MyFirstModel()
dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
dynamicModel.run()

aguila('--timesteps=[1,181,1]','pre2_3')
  




