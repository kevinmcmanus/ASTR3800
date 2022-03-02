import numpy as np
import matplotlib.pyplot as plt


class Model:
    def __init__(self,name="undefined"):
        self.name = name
        self.npt = 0
        self.x = []
        self.y = []
        self.cumy = []
        self.dx = []

    def __repr__(self):
        reprstr = f'Object type: {type(self)}; name: {self.name}'
        return reprstr

        
    def Xarray(self,npt=10,xmin=0.,xmax=1.):
        self.npt = npt
        self.x = np.linspace(xmin, xmax, npt, endpoint=False)
        self.dx = (xmax-xmin)/(npt)
        
    def PlotModel(self):
        plt.title(self.name)
        plt.plot(self.x,self.y)
        plt.show()

   

