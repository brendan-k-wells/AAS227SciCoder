import numpy as np
from .errors import *


class ProbDist(object):
    def __init__(self, z_data, p_data):
        """
        A probability distribution takes the binned redshift data (z_data)
        and probability data (p_data)
        """
        self.z_data = z_data
        if z_data is None:
            raise RedshiftDataIsNone("The redshift data is None")
        self.p_data = p_data
        if p_data is None:
            raise ProbabilityDataIsNone("The probability data is None")
            
        if len(p_data) != len(z_data):
            raise DataLengthNotEqual("The probability and redshift data must be the same length")
    
    def _identify_bin_range(self, low, high):
        """
        This method finds the range of z_data corresponding to low and high.
        
        The return value is low_bin, high_bin, where:
                z_data[low_bin] is the first value > low
                z_data[high_bin] is the first value > high
        """
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
        """
        Integrates the probability data from low to high
        
        If interpolate is false, this method returns the integral using only
        whole bins. If interpolate is true, it determines the fractional area
        above and below the regular bin area. This is included for compatability
        with example code
        """
        
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
        """
        Returns the integrated normalized probability from low to high
        """
        numerator = self._integrate(low,high)
        denominator = self._integrate(0,6)
        
        return numerator/denominator