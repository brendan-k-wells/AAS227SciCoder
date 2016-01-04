

class Spectrum(object):
    def __init__(self, wavelengths, fluxes, flux_errors = None):
        """ 
        A spectrum class which holds wavelengths and fluxes for the moment
        """
        self.wavelengths = wavelengths
        self.fluxes = fluxes
        self.flux_errors = flux_errors
    