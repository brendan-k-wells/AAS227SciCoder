from .errors import *

class Spectrum(object):
    def __init__(self, wavelengths, fluxes, flux_errors = None):
        """ 
        A spectrum class which holds wavelengths and fluxes for the moment
        """
        self.wavelengths = wavelengths
        if wavelengths is None:
            raise WavelengthDataIsNone("The wavelength data is None")
            
        self.fluxes = fluxes
        if fluxes is None:
            raise FluxDataIsNone("The flux data is None")
            
        self.flux_errors = flux_errors
    
