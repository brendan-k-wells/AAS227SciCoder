import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import sys

class FITSFileHandler(object):
    def __init__(self,filename):
        self.hdulist = fits.open(filename)

class ProbabilityHandler(FITSFileHandler):
    def __init__(self, filename):
        super(ProbabilityHandler,self).__init__(filename)
        self.z_hdu = self.hdulist[1]
        self.p_hdu = self.hdulist[2]
        
        self.z_data = self.z_hdu.data
        self.p_data = np.exp(self.p_hdu.data)
    
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
            
        
    def _integrate(self, low,high, interpolate=True):
        # Get the intermediate data
        low_bin, high_bin = self._identify_bin_range(low,high)
        
        new_data = zip(self.z_data, self.p_data)[low_bin:high_bin]
        
        # Get the interp points
        
        if interpolate:
            low_p, high_p = np.interp([low,high], self.z_data, self.p_data)
        
            # Sub in as needed
            if new_data[0][0] > low:
                new_data.insert(0, (low,low_p))
                
            if new_data[-1][0] < high:
                new_data.append((high,high_p))
                    
        # Integrate
        x,y = zip(*new_data)
        integral = np.trapz(y,x)
        
        
        return integral
        
        
        
    def p(self,low, high):
        numerator = self._integrate(low,high)
        denominator = self._integrate(0,6)
        
        return numerator/denominator
            
    def plot(self):
        plt.figure()
        
        plt.plot(self.z_data, np.exp(self.p_data))
        
        plt.show()

class SpectrumHandler(FITSFileHandler):
    def __init__(self, filename):
        super(SpectrumHandler,self).__init__(filename)
        
        self.data = self.hdulist[1].data
        
    def plot(self):
        plt.figure()
        
        x = self.data['wave']
        y = self.data['flux']
        y_err = self.data['error']
        
        plt.errorbar(x,y,yerr=y_err)
        
        plt.show()    


if __name__ == "__main__":
    spec_filename = "cosmos-01-G141_21477.1D.fits"
    pz_filename = "cosmos-01-G141_21477.new_zfit.pz.fits"
    
    prob = ProbabilityHandler(pz_filename)
    print prob.p(2.1,2.3)
    prob.plot()
    
    spec = SpectrumHandler(spec_filename)
    spec.plot()
