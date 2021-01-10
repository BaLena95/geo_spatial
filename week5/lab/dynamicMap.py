from pcraster import *
from pcraster.framework import *

os.chdir(r"C:\Users\lenaw\Documents\data\dynmod\snowmelt")

class MyFirstModel(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)
    setclone('dem.map')

  def initial(self):
      pass
      dem = self.readmap('dem')
      slopeOfDem = slope(dem)
      self.report(slopeOfDem,'gradient')
  
  def dynamic(self):
    timeStep = self.currentTimeStep()
    print('running the dynamic for time step: ', timeStep)
    precip = self.readmap("precip")
    #Add a statement converting from m/day to mm/day
    precip = precip * 1000
    self.report(precip, "pmm")
      
      
nrOfTimeSteps=181
myModel = MyFirstModel()
dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
dynamicModel.run()


aguila('--timesteps=[1,181,1]','precip', 'pmm')

