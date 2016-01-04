from astropy.io import fits

class FITSFileHandler(object):
    def __init__(self,filename):
        self.hdulist = fits.open(filename)
