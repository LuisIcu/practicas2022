import random
import matplotlib.pyplot as plt
from astropy.convolution import convolve, AiryDisk2DKernel, Gaussian2DKernel
import numpy as np

#----------Parámetros que vamos a usar-----------#
#1. Dimension de las matrices
B=150
#3. Cuantas fuentes queremos
n = 15
#3.FWHM de la gaussiana
FWHM = 6
#4. Flag para ver si sumamos el ruido
#0 si no lo sumamos, 1 si sí lo sumamos, 2 si usamos el modo de prueba
F = 0


#Kernels que podemos usar
airydisk_2D_kernel = AiryDisk2DKernel(4)
gauss_2D_kernel = Gaussian2DKernel(FWHM/2.355)


sigma4 = round((3.5)*(FWHM/2.355))
#Matriz de señales obtenidas
Fuentes=[]
Signal = np.zeros((B,B))
for i in range(n):
    x = random.randint(sigma4,B-sigma4)
    y = random.randint(sigma4,B-sigma4)
    f = random.randint(10,1500)
    Signal[x][y]=f
    Fuentes.append([x,y,f])


#Matriz de ruido
Noise = np.random.normal(0,1,size=(B,B))

#Matriz observada + matriz de ruido
Obs = Signal+Noise

if F==1:
    conv= convolve(Signal,gauss_2D_kernel)
    data = conv + Noise
elif F==0:
    data = convolve(Signal,gauss_2D_kernel)



for k in range(len(Fuentes)):
    Tot = 0
    x = Fuentes[k][0]
    y = Fuentes[k][1]
    for i in range(-sigma4,sigma4):
        for j in range(-sigma4,sigma4):
            if np.sqrt((i)**2+(j)**2)<=sigma4:
                Tot += data[x+i][y+j]
    Fuentes[k].append(Tot)
    Fuentes[k].append(Tot/Fuentes[k][2])

for i in range(len(Fuentes)):
    print(Fuentes[i][0], Fuentes[i][1], Fuentes[i][2], Fuentes[i][3], Fuentes[i][4])
    
#plt.imshow(airydisk_2D_kernel, interpolation='none', origin='lower')
plt.imshow(data, interpolation='none', origin='lower')
plt.xlabel('x [pixels]')
plt.ylabel('y [pixels]')
plt.colorbar()
plt.savefig('Mapa-celeste.pdf',dpi=300,bbox_inches='tight')
plt.close()
#plt.show()

h = []
for i in range(len(Noise)):
    for j in range(len(Noise[i])):
        h.append(Noise[i][j])
count, bins, ignored =  plt.hist(h,50,density=True)
plt.savefig('historuido.pdf',dpi=300,bbox_inches='tight')
plt.close()

Cambio = []
for i in Fuentes:
    Cambio.append(i[4])
print(Cambio)
count, bins, ignored =  plt.hist(Cambio,5,density=True)
plt.savefig('cambio.pdf',dpi=300,bbox_inches='tight')
plt.close()
