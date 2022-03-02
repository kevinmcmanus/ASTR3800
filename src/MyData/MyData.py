#From Chapter 3
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from copy import deepcopy
from scipy.interpolate import UnivariateSpline
from scipy.ndimage import convolve, gaussian_filter
from scipy import signal
from astropy.io import fits

class MyData:
    def __init__(self,filename='NoFile'):
        self.filename = filename
        self.ndim = 0 
        self.x = []
        self.nx = 0
        self.y = []
        self.ny = 0
        self.z = []
        self.nz = 0
        self.array = []
        self.header = []
        self.nxa = 0
        self.nya = 0
        
    def xline(self,xmin,xmax,nx):
        self.nx = nx
        self.ndim = 1
        self.x = np.linspace(xmin,xmax,nx)

    def yline(self,a,b):
        if(self.ndim == 1):
            self.ny = self.nx
            self.y = a + b*self.x
        else:
            print("x value not one dimensional")

    def plotxy(self):
        plt.cla()
        plt.title(self.filename)
        plt.plot(self.x,self.y)
        plt.show()

    def plotpoints(self, **kwargs):

        title = kwargs.pop('title', self.filename)
        ax = kwargs.pop('ax', None)
        # the rest of the kwargs go to ax.scatter

        if ax is None:
            fig, ax = plt.subplots()
        
        #plt.plot(self.x,self.y)
        ax.scatter(self.x, self.y, **kwargs)
        ax.set_title(title)


    def GetFits(self, filename):
        self.filename = filename
        hdul = fits.open(filename)
        self.array = fits.getdata(filename)
        self.header = hdul[0].header
        sh = np.shape(self.array)
        self.nxa = sh[0]
        self.nya = sh[1]
        self.ndim = 2
            
    def GetTableData(self, filename):
        self.filename = filename
        data_array=np.genfromtxt(filename)
        s = data_array.shape
        if len(s) == 1 :
            self.x= data_array
            self.nx = s[0]
        if len(s) == 2 :
            self.x = data_array[:, 0]
            self.y = data_array[:, 1]
            self.nx = s[0]
            self.ny = s[0] #one y value for each x value

    def WriteTableData(self,filename='test.txt'):
        f = open(filename,"w")
        if self.ny == 0:
            for i in range(0,self.nx):
                f.write('%8.4f\n' % self.x[i] )
        else:
            for i in range(0,self.nx):
                f.write('%8.4f  %8.4f\n' % (self.x[i],self.y[i]))
        f.close()

    def Quicklook(self):
        if (self.nx == 0):
            print("Whoops! No Data")
            return
        plt.cla()
        if self.ny == 0:
            plt.plot(self.x, c='black')
        else:
            plt.scatter(self.x, self.y, s=2, marker='o', c='black')
        plt.show()
        print("length of x list is ",len(self.x), "items")
        
    def ReadInteger16(self,filename,nxa=256,nya=256):
        self.filename = filename
        data = np.fromfile('m33.dat', dtype='i2')
        self.array = np.reshape(np.array(data),(nxa,nya))
        self.ndim = 2
        self.nxa = nxa
        self.nya = nya
        
    def WriteFloat64(self,filename="test.dat"):
        self.filename = filename
        f= open(self.filename,"w+")
        self.x.tofile(f)
        f.close()

    def ReadFloat64(self,filename="test.dat",nxa=256,nya=256):
        self.filename = filename
        f= open(self.filename,"r")
        self.y=np.fromfile(f,'f8')
        f.close()

    def ReadExcelColumn(self, filename, sheetname, columnname):
        self.filename = filename
        e = pd.ExcelFile(filename)
        ep = e.parse(sheetname)
        df=ep[columnname]
        self.x = df.values
        self.nx = len(self.x)
        self.ndim = 1
        
    def WriteExcelColumn(self, filename):
        df = pd.DataFrame(data=self.x)
        with pd.ExcelWriter(filename) as writer:
            df.to_excel(writer)
            
    def MyHistogram(self,bins=10):
        hi=np.histogram(self.x,bins=bins)
        hy=np.array(hi[0])
        hx=np.array(hi[1])
        hx=hx[1:]
        plt.cla()
        #plt.plot(hx,hy,linestyle='steps')
        plt.plot(hx,hy,linestyle='-')
        plt.show()

    def Slice(self, slc):
        """
        slices self.x and self.y according to slc
        """
        if self.nx == 0:
            raise ValueError('Data object has no data to slice')
        self.x = self.x[slc]
        self.nx = len(self.x)
        if self.ny != 0:
            self.y = self.y[slc]
            self.ny = len(self.y)


    #helper routine for smoothing
    def smoother(self, smooth_type='gaussian', smooth_param=1.0):

        if smooth_type != 'gaussian' and smooth_type != 'convolve':
            raise ValueError(f'Invalid smooth_type: {smooth_type}, valid smooth_types: gaussian and convolve')
        
        #prevent overflows
        if self.array.dtype == np.int16:
            data = self.array.astype(np.int32)
        else:
            data = self.array

        if smooth_type == 'gaussian':
            smoothed = gaussian_filter(data, smooth_param)
        elif smooth_type == 'convolve':
            filter = np.ones((smooth_param, smooth_param))
            smoothed = convolve(data, filter)/filter.sum() # retain orig scaling
        else:
            assert False # shouldn't get here

        return smoothed
            

    def MyImage(self,**kwargs):
        ax = kwargs.pop('ax', None)
        cmap = kwargs.pop('cmap', 'gray')
        title = kwargs.pop('title', self.filename)
        cb = kwargs.pop('cb', False)
        contours = kwargs.pop('contours', False)
        smooth_type = kwargs.pop('smooth_type', None)
        smooth_param = kwargs.pop('smooth_param', None)
        contours = kwargs.pop('contour_lines', False)
        levels = kwargs.pop('levels', None)

        fig = None
        if ax is None:
            fig, ax = plt.subplots()

        if smooth_type is None:
            data = self.array
        else:
            data = self.smoother(smooth_type, smooth_param)
        
        pcb = ax.imshow(data, origin='lower',  cmap=cmap)

        if contours:
            pcb = ax.contour(data, origin='lower', levels=levels, cmap='Reds')


        ax.set_title(title)

        #put the colorbar on if requested
        if cb:
            cbar = plt.colorbar(pcb, ax=ax, shrink=0.65, pad=0.05)
            cbar.set_label('Intensity', rotation=270)

        #since this is an image, ditch the axes ticks and labels
        ax.xaxis.set_visible(False); ax.yaxis.set_visible(False)

        return pcb

    def MyHistogram(self,**kwargs):
        ax = kwargs.pop('ax', None)
        xlim = kwargs.pop('xlim', (None, None))
        title = kwargs.pop('title', self.filename)
        density = kwargs.pop('density', False)
        grid = kwargs.pop('grid', True)
        which = kwargs.pop('which','x')

        data = getattr(self, which)


        fig = None
        if ax is None:
            fig, ax = plt.subplots()

        ax.hist(data, density=density, **kwargs)
        
        ylab = ('Density' if density else 'Count') + f' of {which}'
        ax.set_ylabel(ylab)
        ax.set_title(title)
        ax.set_xlim(xlim)
        if grid:
            ax.grid(axis='y')


    def SimData(self, npt=100, rand = 'Uniform',xbar=0.,sigma=1. ):
        if rand == 'Poisson':
            #xbar a vector or scalar of poisson expected values
            l = len(xbar) if hasattr(xbar, '__len__') else 1
            self.y = np.random.poisson(xbar, l)
        elif rand == 'Gauss':
            self.y = np.random.normal(size=npt,loc=xbar,scale=sigma)
        elif rand == 'Uniform':
            self.y = np.random.uniform(size=npt)
        else:
            raise ValueError(f'Invalid rand: {rand}, must be one of Poisson, Gauss or Uniform')

if __name__=="__main__":
    d = MyData()
    d.SimData(rand='Gauss', npt=50000, xbar=30, sigma=4)
    d.MyHistogram(which='y',bins=30, density=True, )
    plt.show()