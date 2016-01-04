import numpy as np
import matplotlib.pyplot as plt
from ProbDist import ProbDist
from Spectrum import Spectrum

from astropy.io import fits



def build_spectrum(spectrum_filename):
    """
    Takes a spectrum filename in familiar format and produces a Spectrum
    """
    hdulist = fits.open(spectrum_filename)
    data = hdulist[1].data
    
    spec = Spectrum(data['wave'], data['flux'], data['error'])
    
    return spec
    
def build_probdist(prob_filename):
    """
    Takes a probability distribution filename in familiar format and produces a ProbDist
    """
    fits_file = fits.open(prob_filename)
    
    z_hdu = fits_file[1]
    p_hdu = fits_file[2]
    
    z_data = z_hdu.data
    p_data = np.exp(p_hdu.data)
    
    return ProbDist(z_data, p_data)
    
    
            
def plot_pz(pz_inst):
    """
    Plots the probability data versus redshift
    """
    plt.figure()
    
    plt.plot(pz_inst.z_data, pz_inst.p_data)
    
    plt.savefig("pz_figure.png")
    plt.close()

        
def plot_spectrum(spectrum):
    """
    Plots the spectrum in flux per wavelength
    """
    plt.figure()
    
    x = spectrum.wavelengths
    y = spectrum.fluxes
    y_err = spectrum.flux_errors
    
    plt.errorbar(x,y,yerr=y_err)
    
    plt.savefig("spec_figure.png")
    plt.close()


if __name__ == "__main__":
    spec_filename = "cosmos-01-G141_21477.1D.fits"
    spec = build_spectrum(spec_filename)
    plot_spectrum(spec)    
    
    pz_filename = "cosmos-01-G141_21477.new_zfit.pz.fits"
    prob = build_probdist(pz_filename)
    print prob.p(2.1,2.3)
    plot_pz(prob)
    

