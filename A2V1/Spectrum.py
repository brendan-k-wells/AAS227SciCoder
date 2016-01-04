

class Spectrum(object):
    def __init__(self, fits_file):
        self._fits_file = fits_file
        
        self._data = fits_file.hdulist[1].data
        
        self.wavelengths = self._data['wave']
        self.fluxes = self._data['flux']
        self.flux_errors = self._data['error']