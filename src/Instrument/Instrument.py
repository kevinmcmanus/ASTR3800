
import numpy as np
import sys

if __name__ == "__main__":
    sys.path.insert(0, r'ASTR3800\src')

from Star.Star import Star

class Instrument():
    def __init__(self,name='Unnamed', nlam = 100, lam_min = 100., lam_max = 1000.,
                 diameter = 1., efficiency=1.00):
        """
        Constructs an Instrument object.

        Arguments:
            name: str; name of the instrument
            nlam: int; number of wavelength bins
            lam_min, lam_max: float; wavelength minimum and maximum, NANOMETERS
            diameter: float, diameter of instrument in meters
            efficiency: float (0,1): efficiency of the instrument
        """
        self.name = name
        self.nlam = nlam
        self.lam_min = lam_min
        self.lam_max = lam_max
        self.lam = np.linspace(lam_min, lam_max, nlam )
        self.lambin = (lam_max-lam_min)/float(nlam) #binwidth in nm
        self.diameter = diameter # meters
        self.efficiency = efficiency
        self.area = (np.pi/4)*diameter**2 #in m^2
        self.eff_area = self.area*efficiency



    def __repr__(self):
        reprstr='Instrument Object; '+ ', '.join([f'{p} = {getattr(self,p)}' for p in \
             ['name', 'nlam', 'lam_min', 'lam_max', 'diameter', 'area', 'eff_area']])
        return reprstr

    def lam_meters(self):
        """
        Computes and returns the intruments wavelength property to meters
        """

        nm_per_meter = 1e9
        return self.lam/nm_per_meter

    def binwidth_m(self):
        """
        Return the width in meters of the instruments wavelength bins.
        """
        nm_per_meter = 1e9
        return self.lambin/nm_per_meter

    def simulate(self, star:Star, obstime:float, obstype:str='photon_counts'):
        """
        simulates observation of star for obstime seconds.

        Arguments:
            star: star object; the target of observation/simulation
            obstime: float; exposure time in seconds
            obstype: string {'photon_counts' 'flux'} specifies whether to comupte photon counts or flux

        Returns:
            dict of wavelength (key "lmbda") and photon count or flux (key: "photons" or "flux")
        """

        if obstype != 'flux' and obstype != 'photon_counts':
            raise ValueError(f'Invalid obstype: {obstype}, must be either \'photon_counts\' or \'flux\'')

        if obstype != 'photon_counts':
            raise ValueError('Only \'photon_counts\' implemeneted at this time.')

        lam_m = self.lam_meters()
        bin_width = self.binwidth_m()

        #get the star's flux spectrum (returned as Watts/labmda which is J/(second lambda))
        flux_spectrum = star.flux_spectrum(lmbda = lam_m)
        #bin-ify the spectrum
        # already done from above

        #get Joules
        joules_spectrum = obstime*flux_spectrum*self.area/self.nlam

        #convert to photons
        c = 2.99792e+08 # m s^-1
        h = 6.62607e-34  # J s
   

        expected_photon_counts = bin_width*joules_spectrum/(h*c/lam_m)

        #add poisson random component
        simulated_photon_counts = np.random.poisson(lam=expected_photon_counts,size=self.nlam)

        #return result
        return {'lmbda':self.lam, #note nanometers
                'expected': expected_photon_counts,
                'error': np.sqrt(expected_photon_counts),
                'simulated':simulated_photon_counts
                }

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    target = Star('G2 star in Andomeda', ra='0:42:44', dec='+41:16:9', distance=7e5, mass= 1, teff=5780, radius=1.0)

    print(target)

    #1 um = 1000 nm
    hubble = Instrument(name='Hubble Space Telescope',
    diameter=2.4, efficiency=0.6,
    nlam=100, lam_min=300, lam_max=2100)

    print(hubble)

    obstime=10e3 # seconds
    sim = hubble.simulate(target, obstime)

    plt.plot(sim['lmbda'], sim['expected'])
    plt.plot(sim['lmbda'], sim['simulated'])
    plt.show()