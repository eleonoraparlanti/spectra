import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import FitsReader
import os

class Dark_Flat():

    def __init__(self,filename_d,filename_b,filename_f, data):
        self.dark = filename_d
        self.flat = filename_f
        self.bias = filename_b
        self.data = data
        self.c = len(self.data)
        self.r = len(self.data[0])


    def open_Dark(self):
        a = FitsReader.FitsReader(self.dark)
        data = a.reader()
        return data


    def open_Flat(self):
        a = FitsReader.FitsReader(self.flat)
        data = a.reader()
        return data


    def open_Bias(self):
        a = FitsReader.FitsReader(self.bias)
        data = a.reader()
        return data


    def corrected_flat(self):
        d = self.open_Dark()
        b = self.open_Bias()
        f = self.open_Flat()
        image = np.zeros((self.c,self.r))
        for i in range(500,700):
            for j in range(0,self.r):
                image[i][j] = f[i][j] - b[i][j]

        return image

    def Flat(self):
        f = self.corrected_flat()
        g  = np.zeros((self.r))
        for i in range(500,700):
            for j in range(0,self.r):
               g[i] = g[i] + f[i][j]
        return g/self.r

    def Average_Flux(self):
        f = self.corrected_flat()
        k = 0
        for i in range(500,700):
            for j in range(0,self.r):
                k = k + f[i][j]

        average =  k / (self.c*self.r)

        return average


    def median_flux(self):
        f =  self.corrected_flat()
        med = np.median(f[600])
        return med


    def Correction(self):
        f = self.corrected_flat()
        d = self.open_Dark()
        b = self.open_Bias()
        av = self.Average_Flux()
        med = self.median_flux()
        a = self.Flat()
        image  = np.zeros((self.c,self.r),dtype=np.uint16)
        for i in range(500,700):
            for j in range(0,self.r):
                image[i][j] = (self.data[i][j]-(d[i][j]))*av / (f[i][j])
        return image