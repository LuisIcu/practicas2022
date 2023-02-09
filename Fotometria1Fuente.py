import random
import matplotlib.pyplot as plt
from astropy.convolution import convolve, AiryDisk2DKernel, Gaussian2DKernel
import numpy as np
from scipy.optimize import curve_fit

import Funciones as f

'''
Este programa muestra la fotometría de apertura para una fuente aislada sin ruido
'''

#----------Parámetros que vamos a usar-----------#
#1. Dimension de las matrices
B=31
#3.FWHM de la gaussiana
FWHM = 6


#-----Constantes a utilizar--------
#Sigma de la gaussiana
sigma = FWHM/2.355
#Radio de sumado
rsig = round(sigma)

#Nuestro kernel gaussiano
gauss_2D_kernel = Gaussian2DKernel(sigma) #Campana gaussiana

#Construimos la matriz que vamos a analizar
Signal = np.zeros((B,B))
medcord = int((B-1)/2)
Signal[medcord][medcord] = random.randint(500,1500)
RealFlux = Signal[medcord][medcord]

data = convolve(Signal,gauss_2D_kernel)

#SumMultRadio es una función que hice específicamente para ver cuánto flujo se recupera
#según el radio de integración
RelFlux = f.SumMultRadio(data,medcord,medcord,4*rsig,RealFlux)
Radio = np.array([i for i in range(1,4*rsig)])
plt.plot(Radio,RelFlux,'r--')



'''-----------------Esto ya es para el ploteo-----------------'''
plt.axhline(y = 0.9, color = 'c', linestyle = '--', linewidth = 0.5) 
plt.axhline(y = 1, color = 'c', linestyle = '--', linewidth = 0.5) 
for i in range(1,5):
    plt.axvline(x=i*sigma, ymin=0, ymax=1,linestyle = '--', linewidth = 0.5,color='m')
    plt.text(i*sigma+0.03,0.01,str(i)+r'$\sigma$',color='m')

plt.text(0.02,0.86,'90%',color='c')
plt.xlabel('Radio de integración')
plt.ylabel(r'$F(r)/F_{0}$')
plt.title(r'Relación entre el flujo integrado $F(r)$ sobre flujo ingresado $F_{0}$')
plt.xlim(0,12)
plt.ylim(0,1.05)
plt.savefig('./Imagenes/Fotometria1Fuente.pdf',dpi=400,bbox_inches='tight')
#plt.show()