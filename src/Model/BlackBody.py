import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import non_negative_factorization

# import sys
# sys.path.append(r'C:\Users\Kevin\repos\ASTR3800\src')

if __name__ == "__main__":
    from Model import Model
else:
    from Model.Model import Model

class BlackBody(Model):
    def __init__(self, name, temp, lmbda=None):
        self.temp = temp
        self.lmbda = lmbda
        self._intensity = None
        super().__init__(name)

        if self.lmbda is None:
            #set default wavelengh array
            nm_per_meter = 1e9
            lam_min = 100.; lam_max = 1000.; nlam=100
            lam = np.linspace(lam_min, lam_max, nlam )/nm_per_meter
            self.lmbda = lam

    def _lmbda(self, lmbda):
        mylmbda = lmbda if lmbda is not None else self.lmbda
        if mylmbda is None:
            raise ValueError('Missing wavelength array')
        return mylmbda

    def intensity(self, lmbda=None):
        """
        Computes and returns Planck Function
        Arguments:
            lmdba: array(n,) float; wavelength in meters
        returns:
            intensity: array(n,): float, intensity (brightness) at each lambda, watt m^-2 m^-1 steradian^-1
        """
        #some constants(mks units)
        c = 2.99792e+08 #m s^-1; speed of light
        h = 6.62607e-34 #J s; Planck's constant
        k = 1.38065e-23 #J k^1- ; Boltzmann's constant

        mylmbda = self._lmbda(lmbda=lmbda)
        temp = self.temp

        #construct the intensity (B_lambda) as product of two terms
        #first term:
        first_term = (2*h*c**2)/np.power(mylmbda, 5)

        #second term:
        expnt = h*c/(mylmbda*k*temp)
        second_term = 1/(np.exp(expnt)-1)

        B_lambda = first_term*second_term #units: J s^-1 m^-2 m^-1 steradian^-1

        return B_lambda

    def flux(self, lmbda=None):

        #self._ intensity is an infintesimally small area on body's surface radiating isotropically
        #Intergrate over surface of the area that is facing outward
        #this integration gets rid of the steradian term above
        #See Maoz, p12, eq 2.5

        mylmbda = self._lmbda(lmbda=lmbda)
        B_lambda = self.intensity(mylmbda)

        f_lmbda = np.pi*B_lambda #See Maoz, p12, eq 2.5

        return f_lmbda


    def integrate_spectrum(self, lmbda=None):
        """
        Approximates definite integral of flux over frequency range. Returns result.

        """
        mylmbda = self._lmbda(lmbda=lmbda)
        flux = self.flux(lmbda=mylmbda)

        bolo_flux = np.trapz(flux, self.lmbda)
        return bolo_flux

    def Wien(self):
        """
        Computes and returns wavelength (in m) of maximum flux given star's temperature
        """

        lmbda_max = 0.0029/self.temp #meters
        return lmbda_max

    def plot_spectrum(self, **kwargs):
        ax = kwargs.pop('ax', None)
        title = kwargs.pop('title', self.name)
        label = kwargs.pop('label', f'Planck teff={self.temp}')
        lmbda = kwargs.pop('lmbda', None)

        mylmbda = self._lmbda(lmbda=lmbda)
        obsval = self.flux(lmbda=mylmbda)

        fig = None
        if ax is None:
            fig, ax = plt.subplots()


        nm_per_m = 1e9 #x-axis to be plotted in nanometers
        lmbda_nm = self.lmbda*nm_per_m
        lmbda_max_nm = self.Wien()*nm_per_m

        ln, = ax.plot(lmbda_nm, obsval, label=label, **kwargs)
        zz = f'{lmbda_max_nm:.3e}'
        lbl = r'$\lambda_{max}: '+zz+r'\ nm$'
        ax.axvline(lmbda_max_nm,  color=ln.get_color(), ls=':', label=lbl)

        ax.set_xlabel(r'$Wavelength (nm)$')
        ax.set_ylabel(r'$Joule\ m^{-2}\ s^{-1}\ m^{-1}$')
        ax.set_title(title)

if __name__ == "__main__":


    b_sun = BlackBody('sun', 5780)
    lam_min = 100.; lam_max = 1000.; nlam=100
    lam = np.linspace(lam_min, lam_max, nlam )
    #convert to meters
    nm_per_meter = 1e9
    lam /= nm_per_meter

    print('++++++++*****')
    print(b_sun.flux(lam))

    hotter_sun = BlackBody('hotter sun', 7000.0)
    hotter_sun.flux(lam)

    fig,ax = plt.subplots(figsize=(6,6))
    b_sun.plot_spectrum(ax=ax)
    hotter_sun.plot_spectrum(ax=ax)
    ax.legend()
    plt.show()

