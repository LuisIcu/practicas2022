import random
import matplotlib.pyplot as plt
from astropy.convolution import convolve, AiryDisk2DKernel, Gaussian2DKernel
import numpy as np
from scipy.optimize import curve_fit

import Funciones as f

'''
Este programa lo hice para ver cuánto de flujo se aporta por el ruido gaussiano

Lo que hace es crear una matriz y en esa matriz mira cúanto ruido se ha sumado alrededor de
cierta cantidad de puntos. Esto lo repetimos para muchas matrices con muchos puntos cada una
para tener un valor estadístico significativo.
'''

#----------Parámetros que vamos a usar-----------#
#1. Dimension de las matrices
B=100
#3.FWHM de la gaussiana
FWHM = 6
#4 Cantidad de mapas creados
Nmap = 100
#Cantidad de círculos por mapa
Ncirc = 20


#-----Constantes a utilizar--------
#Sigma de la gaussiana
sigma = FWHM/2.355
#Radio de sumado
rsig = round(sigma)

#Kernels que podemos usar
airydisk_2D_kernel = AiryDisk2DKernel(4) #Disco de Airy
gauss_2D_kernel = Gaussian2DKernel(sigma) #Campana gaussiana

Limit = np.array([])

r=round(2.5*rsig)
for m in range(Nmap):
    Ruido=np.random.normal(0,2,(B,B))
    for n in range(Ncirc):
        Tot=0
        x = random.randint(r+1,B-r-1)
        y = random.randint(r+1,B-r-1)
        Tot=f.SumRadio(Ruido,x,y,r)
        Limit = np.append(Limit,Tot)

#Media y Desviación del ruido
mean = f.media(Limit)
stdv = f.stdv(Limit)

#Media y Desviación del ruido con valores absolutos
absmean = f.mediaabs(Limit)
absstdv = f.stdvabs(Limit)

#--------------------------------------------------------------------------------------------------------------------------

#Escribiendo cosas en un txt 
file = open('./datosruido.txt','w')

file.write(
    'Se crearon ' + str(Nmap) + ' mapas donde se tomaron ' + str(Ncirc) + ' puntos por mapa.\n'
    'Se sumó el ruido en un radio de sumado de ' + r'2$\sigma\approx$ 6.5' + ' pixeles. \n'
    'A partir de estos datos tenemos los siguientes datos: \n'
    '\n'
    'Cantidad de datos: ' + str(Nmap*Ncirc) + '\n'
    'Media del ruido en cada círculo: ' + str(mean) + '\n'
    'Desviación del ruido: ' + str(stdv) + '\n'
    'Media del ruido en cada círculo (con valor absoluto): ' + str(absmean) + '\n'
    'Desviación del ruido (con valor absoluto): ' + str(absstdv) + '\n'
    '\n'
    '\n'
    'Ruido en cada círculo:\n'
    '\n'
)

for i in range(len(Limit)):
    file.write(
        str(i) + '\t' + str(Limit[i]) + '\n'
    )
