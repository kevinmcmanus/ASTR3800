import os, sys
import numpy as np

if __name__ == "__main__":
    sys.path.insert(0, r'ASTR3800\src')

from Model.BlackBody import BlackBody

class Star():
    # required star properties the Star object keeps track of
    _starprops = ['ra','dec','distance','radius','mass','teff']
    # properties to coerce to floats
    _starpropfloats = ['distance','radius','mass','teff']
    
    def __init__(self, name, **kwargs):
        """
        Constructs a Star Object.

        Arguments:
            ra: string, right ascension (J2000) hh:mm:ss.ssss
            dec: string, declination (J2000) dd:mm:ss.sssss
            distance: float, pc
            radius: float, soloar radii
            mass: float, solar masses
            teff: float, effective temperature, K
        """      
        self.name = name # required
        
        #required properties; will bomb if property not supplied
        for prop in Star._starprops:
            setattr(self, prop, kwargs.pop(prop))

        #make sure the props that are supposed to be floats are floats
        for prop in Star._starpropfloats:
            setattr(self, prop, float(getattr(self, prop)))
       
    def __repr__(self):
        str = f'Star object: name: {self.name}'
        for prop in Star._starprops:
            v = getattr(self, prop, None)
            if v is not None:
                str += f', {prop}: {v}'            
        return str

    def radius_m(self):
        """
        Returns star radius in m.
        """
        sun_r_m = 6.957e+08 # m
        return self.radius*sun_r_m

    def distance_m(self):
        """
        Returns distance to star in m.
        """
        m_per_pc = 3.085677581491367e+16
        dist_m = self.distance*m_per_pc
        return dist_m
        
    def surface_area(self):
        """
        Returns surface area of star in m^2.
        """
        r = self.radius_m()
        return 4*np.pi*r**2
        
    def mass_g(self):
        """
        Returns star mass in kg.
        """
        sun_m_kg = 1.98841e+30 #kg
        return self.mass*sun_m_kg

    def Wien(self):
        """
        Computes and returns wavelength (in nm) of maximum flux given star's temperature
        """
        nm_per_meter = 1e9
        lmbda_max = BlackBody(name=None, temp=self.teff).Wien()
        return lmbda_max*nm_per_meter

    def surface_flux(self):
        """
        Computes flux on the surface of the star using StefanBoltzmann law
        Returns:
            flux: float, W m^-2
        """
        sb =  5.67037e-08 #stefan boltzmann const. W / (K4 m2)
        self.flux = flux = sb*np.power(self.teff,4)
        return flux

    def luminosity(self):
        """
        Computes and returns star's luminosity (in Watts) from its radius and temperature
        """
        sa = self.surface_area()
        flux = self.surface_flux()
        return flux*sa

    def luminosity_spectrum(self, lmbda=None):
        bb = BlackBody(name=None, temp=self.teff)
        spec = bb.flux(lmbda=lmbda)
        sa = self.surface_area()
        lum = spec*sa
        return lum

    def flux_spectrum(self, lmbda=None):
        lum = self.luminosity_spectrum(lmbda=lmbda)
        dist = self.distance_m()
        flux = lum/(4*np.pi*dist**2)
        return flux

    def to_dict(self):
        """
        Returns a dict of star properties.
        """
        d = dict([(prop,getattr(self,prop,None)) for prop in ['name']+Star._starprops])
        return d


        # #f_lambda need to be multiplied by surface area of star to get its luminosity
        # L_lambda = f_lambda*star.surface_area()
        # self.luminosity_lambda = L_lambda

        # #flux at the observer
        # f_obs_lambda = L_lambda/(4*np.pi*star.distance_m()**2)
        # self.f_obs_lambda = f_obs_lambda

        # #flux in the instrument bins
        # #multiply the spectrum by the bin width, bin area and obstime to get the energy in each instrument bin
        # dx = inst.binwidth_m()
        # inst_flux = f_obs_lambda*dx*inst.area*obstime

        # #update the model with the flux values
        # self.inst_flux_lambda = inst_flux

if __name__ == "__main__":
    mintaka = Star('Mintaka', ra='05:32:00.4009', dec='-00:17:56.7424',
            distance=380, mass= 24, teff=29500, radius=16.5)
    print(f'Mintaka lambda max: {mintaka.Wien()}')