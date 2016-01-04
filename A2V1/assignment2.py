import numpy as np
import matplotlib.pyplot as plt
from FITSFileHandler import FITSFileHandler as Ffh
from ProbabilityDistribution import ProbabilityDistribution as Pz
from Spectrum import Spectrum as Spec

            
def plot_pz(pz_inst):
    plt.figure()
    
    plt.plot(pz_inst.z_data, pz_inst.p_data)
    
    plt.show()


        
def plot_spectrum(spectrum):
    plt.figure()
    
    x = spectrum.wavelengths
    y = spectrum.fluxes
    y_err = spectrum.flux_errors
    
    plt.errorbar(x,y,yerr=y_err)
    
    plt.show()    


if __name__ == "__main__":
    spec_filename = "../cosmos-01-G141_21477.1D.fits"
    pz_filename = "../cosmos-01-G141_21477.new_zfit.pz.fits"
    
    prob = Pz(Ffh(pz_filename))
    print prob.p(2.1,2.3)
    plot_pz(prob)
    
    spec = Spec(Ffh(spec_filename))
    plot_spectrum(spec)
