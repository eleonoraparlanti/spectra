import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import os

class FitsReader():

    def __init__(self, filename):
        self.filename = filename

    def reader(self):
        with fits.open(self.filename) as hdul:  # open a FITS file
            data = hdul[0].data
        return data







