import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import os
import FitsReader
import Dark_Flat
from scipy.optimize import curve_fit


fits_image_filename = ('/home/eleonoraparlanti/Desktop/UNI/ASTROFISICAOSSERVATIVA/Spectrum/M42_lamp.fit')
fits_dark_filename = ('/home/eleonoraparlanti/Desktop/UNI/ASTROFISICAOSSERVATIVA/Spectrum/cal-005__dark.fit')
fits_flat_filename = ('/home/eleonoraparlanti/Desktop/UNI/ASTROFISICAOSSERVATIVA/Spectrum/cal-002__flat.fit')
fits_bias_filename = ('/home/eleonoraparlanti/Desktop/UNI/ASTROFISICAOSSERVATIVA/Spectrum/cal-005_bias.fit')




plt.figure(1)
a = FitsReader.FitsReader(fits_image_filename)
data = a.reader()
plt.imshow(data)
plt.gray()
plt.show()


plt.figure(2)
spec = data[800]
plt.plot(spec)
plt.show()

"""
c = FitsReader.FitsReader(fits_flat_filename)
data = c.reader()
plt.imshow(data)
plt.gray()
plt.show()
"""

b = Dark_Flat.Dark_Flat(fits_dark_filename,fits_bias_filename, fits_flat_filename,data)
x = b.corrected_flat()




plt.figure(3)
y = b.Correction()
plt.imshow(y)
plt.gray()
plt.savefig("lamp-ne-ar.png")
plt.show()
print(b.Average_Flux())



plt.figure(4)
f = b.corrected_flat()
plt.imshow(f)
plt.gray()
plt.show()


c = len(data)
r = len(data[0])

plt.figure(5)
spec = y[605]
plt.plot(spec)
plt.show()


for i in range (0, r):
    if (spec[i]> 3000):
        print ("Int = %f; Pixel= %f" % (spec[i], i))

#for i in range (1000, 1080):
    #if (spec[i]> 5000):
#    print ("Int = %f; Pixel= %f" % (spec[i], i))



"""FIT"""

pix = np.array([133, 895, 1029, 1148,  1275])
err = np.array([3,2,1,1,2])
lam = np.array([4200.67, 5852.49, 6143.06, 6402.25,  6677.28])

w = 1/err**2

init = (0.5, 1, 1)


# DEFINIZIONE DELLA FUNZIONE QUADRATICA
def ff(x, a, b, c):
    return a * x**2 + b * x + c


pars, covm = curve_fit(ff, pix, lam, init, err, absolute_sigma=False)

# CALCOLO DEL CHI QUADRO PER IL BEST FIT
chi2 = (( w*(lam - ff(pix, pars[0], pars[1],pars[2])) ** 2)).sum()

# CALCOLO DEI GRADI DI LIBERTA
ndof = len(pix) - len(init)

# STAMPA DEI RISULTATI OTTENUTI
print('Chi quadro = %.3f ,' % chi2, 'Gradi di liberta = %d ' % ndof)
print('\n')

# STAMPA DEI RISULTATI
print('a = ', pars[1], '+/-', (np.sqrt(covm[0, 0])))
print('\n')
print('b = ', pars[0], '+/-', np.sqrt(covm[1, 1]))
print('\n')
print('c = ', pars[2], '+/-', np.sqrt(covm[2, 2]))
print('\n')

# prepare a dummy xx array (with 1000 linearly spaced points)
xx = np.linspace(min(pix), max(pix), 1000)

# TRACCIARE LA CURVA
plt.plot(xx, ff(xx, pars[0], pars[1],pars[2]), color='red')
plt.errorbar(pix,lam,yerr = 0, xerr = err,linestyle='', color='black', marker='+')

# IMPOSTARE LA FINESTRA DEI RESIDUI


# CREAZIONE ARRAY PER I RESIDUI NORMALIZZATI

r = (lam - ff(pix, pars[0], pars[1],pars[2])) / err

# GRAFICA(RESIDUI)


plt.figure(6)
plt.title('Residui')
plt.rc('font', size=16)
plt.grid(color='gray')
plt.ylabel('Res norm', size=18)
plt.minorticks_on()

# RANGE DI VALORI DA VISUALIZZARE
plt.ylim((-10, 10))

# TRACCIARE LA CURVA DEI RESIDUI
plt.plot(pix, r, linestyle="--", color='blue', marker='o')
plt.show()





print(c)
print (r)