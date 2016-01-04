import astropy
import numpy as np
import matplotlib.pyplot as plt

spec_filename = "cosmos-01-G141_20062.1D.fits"
pz_filename = "cosmos-01-G141_20062.new_zfit.pz.fits"

from astropy.io import fits

class ProbabilityHandler:
    
    def __init__(self, filename):
        self.hdulist = fits.open(filename)
        self.z_hdu = self.hdulist[1]
        self.p_hdu = self.hdulist[2]
        
        self.z_data = self.z_hdu.data
        self.p_data = self.p_hdu.data
    
    def _identify_bin_range(self, low, high):
        low_bin = 0
        high_bin = None
        in_range = False
        for i, value in enumerate(self.z_data):
            if value >= low and not in_range:
                low_bin = i
                in_range = True
            if in_range and value > high:
                high_bin = i
                break
            
        else:
            high_bin = len(self.z_data)
                    
        return low_bin, high_bin
            
            
    def _integrate_probs(self,bins):
        sum = 0
        for i in xrange(*bins):
            sum += np.exp(self.p_data[i])
            
        return sum
        
    def p(self,low, high):
        numerator = self._integrate_probs(self._identify_bin_range( low,high))
        denominator = self._integrate_probs(self._identify_bin_range(0,6))
        
        return numerator/denominator
            
    def plot(self):
        plt.figure()
        
        plt.plot(self.z_data, np.exp(self.p_data))
        
        plt.show()

class SpectrumHandler:
    def __init__(self, filename):
        self.hdulist = fits.open(filename)
        
        self.data = self.hdulist[1].data
        
    def plot(self):
        plt.figure()
        
        x = self.data['wave']
        y = self.data['flux']
        y_err = self.data['error']
        
        plt.errorbar(x,y,yerr=y_err)
        
        plt.show()    


if __name__ == "__main__":
    if False:
        prob = ProbabilityHandler(pz_filename)
        print prob.p(2.1,2.3)
        prob.plot()
    
    spec = SpectrumHandler(spec_filename)
    spec.plot()
