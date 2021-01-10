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
          pass
      
      
nrOfTimeSteps=10
myModel = MyFirstModel()
dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
dynamicModel.run()

  