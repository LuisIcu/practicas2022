import random
import matplotlib.pyplot as plt
from astropy.convolution import convolve, AiryDisk2DKernel, Gaussian2DKernel
import numpy as np
from scipy.optimize import curve_fit

#----------Parámetros que vamos a usar-----------#
#1. Dimension de las matrices
B=150

#Matriz de ruido
Noise = np.random.normal(0,2,size=(B,B))


h = Noise[0]
for i in range(1,B):
    h = np.concatenate((h,Noise[i]),axis=None)

count, bins, ignored =  plt.hist(h,50,density=True,label='Histo ruido')
#Ajuste de la función
bin2 = np.delete(bins,len(bins)-1,0) + (bins[1]-bins[0])/2
def model(x,a,b):
    return (1/np.sqrt(2*np.pi*a**2))*np.exp(-(x-b)**2/(2*a**2))
parinc = [0.5,0.5]
popt, pconv = curve_fit(model,bin2,count,p0=parinc)
x_modelo  = np.linspace(bins[0], bins[len(bins)-1], 200)
plt.plot(x_modelo, model(x_modelo, *popt), 'r-')

plt.text(bin2[int(len(bin2)*0.85)],0.9*np.amax(count),r'Parámetros:' +'\n' +'$\sigma$ = ' + str(round(popt[0],4)) + '\n'+ r'$\mu$ = ' + str(round(popt[1],4)) )
#plt.text(-6,0.1,r'$\mu$ = ' + str(popt[1]))

#Guardar figura y ajuste
plt.xlabel('Valor del ruido')
plt.ylabel('Conteo')
plt.title('Histograma de ruido')
plt.savefig('./Imagenes/historuido.pdf',dpi=600,bbox_inches='tight')
#plt.show()
plt.close()
