import random
import matplotlib.pyplot as plt
from astropy.convolution import convolve, AiryDisk2DKernel, Gaussian2DKernel
import numpy as np
from scipy.optimize import curve_fit

import Funciones as FL

'''
Este programa hace fotometría de apertura para una fuente que está a cierta distancia de
otra fuente. Vamos variando esta distancia para ver cómo cambia el flujo integrado según esta
distancia.
'''


fig, ax=plt.subplots()


#-----Constantes a utilizar--------
#Sigma de la gaussiana
FWHM = 6
sig = FWHM/2.355
#Radio de sumado
rsig = round(sig)
rmax = 8*rsig

#Kernel gaussiano
gauss_2D_kernel = Gaussian2DKernel(sig) #Campana gaussiana

Radio = np.array([i for i in range(1,rmax)])
colores=['#8D21FC','#219CFC','#21FCA5','#61FC21','#FCF821','#FCAB21','#E16140']

ytot = 2*rmax+1
xtot = 3*rmax+2
mc = round((ytot-1)/2)

fuentes = np.zeros((ytot,xtot))
fneto = 1000

fuentes[mc][rmax+1] = 1000
fuentes[mc][rmax+4] = fneto

data = convolve(fuentes,gauss_2D_kernel)

#Hay que hacer la fotometría para el primer caso afuera del for y de ahí iteramos
Finc = FL.SumMultRadio(data,mc,rmax+4,rmax,fneto)
Comp = Finc

ax.plot(Radio,Finc,'--',color=colores[0],label=r'$d$ = '+str(round(3/sig,2))+r'$\sigma$')
plt.axvline(x=3, ymin=0, ymax=1,linestyle = '--', linewidth = 0.5,color=colores[0],alpha = 1)

#El for lo que hace es borrar la fuente anterior y "moverla" unos cuantos pixeles al lado
#Hace esto cierta cantidad de veces
for m in range(6,8*rsig,3):
    fuentes[mc][rmax-2+m] = 0
    fuentes[mc][rmax+1+m] = fneto
    data = convolve(fuentes,gauss_2D_kernel)
    Finc = FL.SumMultRadio(data,mc,rmax+1+m,rmax,fneto)
    #Comp = np.concatenate([Comp,Finc])
    ax.plot(Radio,Finc,'--',color=colores[int(m/3 - 1)],label=r'$d$ = '+str(round(m/sig,2))+r'$\sigma$')
    plt.axvline(x=m, ymin=0, ymax=1,linestyle = '--', linewidth = 0.5,color=colores[int(m/3 - 1)],alpha = 1)


#Este for lo que hace es poner las líneas verticales
for i in range(1,10):
    plt.axvline(x=i*sig, ymin=0, ymax=1,linestyle = '--', linewidth = 0.5,color='gray',alpha = 0.6)
    plt.text(i*sig+0.03,0.01,str(i)+r'$\sigma$',color='gray',alpha = 0.75)

#POnemos líneas horizontales
plt.axhline(y = 0.9, color = 'c', linestyle = '--', linewidth = 0.8) 
plt.axhline(y = 1, color = 'c', linestyle = '--', linewidth = 0.8) 
plt.text(1.02,0.80,'90%',color='c',alpha=0.5)



#---------------------- FORMATO DEL PLOT ---------------------------#
plt.xlabel('Radio de integración')
plt.ylabel(r'$F_{f}/F_{0}$')
#plt.title(r'Flujo integrado $F_{f}$ sobre flujo intrínseco $F_{0}$ en función de la distancia $d$ de separación entre las fuentes')
plt.title(r'Relación $F_{f}/F_{0}$ según la distancia $d$ entre las fuentes')
plt.xlim(1,rmax)
plt.ylim(0,)
leg = ax.legend()
plt.savefig('./Imagenes/Fotometria2Fuentes.pdf',dpi=400,bbox_inches='tight')
#plt.show()