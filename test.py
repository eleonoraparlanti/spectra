import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import os
import fitsreader
import Dark_Flat



fits_image_filename = ('/home/eleonoraparlanti/Desktop/UNI/ASTROFISICAOSSERVATIVA/Spectrum/RRLyr_lamp.fit')





a = FitsReader.FitsReader(fits_image_filename)
x = a.reader()

plt.imshow(x)
plt.show()
