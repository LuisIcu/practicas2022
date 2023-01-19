import random
import matplotlib.pyplot as plt
from astropy.convolution import convolve, Gaussian2DKernel
import numpy as np
import Funciones as L

figure,axes = plt.subplots()

'''
Este programa en específico crea un mapa cuadrado con cierto número de fuentes, las convoluciona
con un perfil gaussiano y les suma ruido instrumental.
Después, usamos fotometría de apertura para ver cómo se recupera el flujo de cada una de las 
fuentes
'''

#-------------Parámetros a usar-------------------
#1. Dimensión de las matrices
B = 150
#2. Número de fuentes
n = 15
#3. FWHM de la gaussiana
FWHM = 6
#4. Radio de sumado
R = round((3.5*(FWHM/2.355)))

#Nuestro kernel
GaussKernel = Gaussian2DKernel(FWHM/2.355)

'''----------------------------------'''
#Creamos la matriz de señales 
Fuentes= []

Map = np.zeros((B,B))
for i in range(n):
    x = random.randint(R+1,B-R-1)
    y = random.randint(R+1,B-R-1)
    f = random.randint(500,1500)
    Map[y][x] = f
    Fuentes.append([y,x,f])

#Matriz de ruido
Noise = np.random.normal(0,2,size=(B,B))

#Matriz final de señales
data = convolve(Map,GaussKernel)+Noise

plt.imshow(data,interpolation=None,origin='lower')
for i in range(len(Fuentes)):
    drawCircle = plt.Circle((Fuentes[i][1],Fuentes[i][0]),FWHM/2,fill=False,color='r')
    axes.add_artist(drawCircle)

plt.xlabel('x[pixels]')
plt.ylabel('y[pixels]')
plt.colorbar()
plt.savefig('./Imagenes/MapaCeleste.pdf',dpi=400,bbox_inches='tight')
#plt.show()
plt.close()


'''Plot comparando flujos iniciales e integrados'''
for i in range(len(Fuentes)):
    F = L.SumRadio(data,Fuentes[i][0],Fuentes[i][1],R)
    Fuentes[i].append(F)
    Fuentes[i].append(F/Fuentes[i][2])

#Arrays de flujo ingresado (Fo) y Flujo integrado (Fi)
Fo = L.ExtCol(Fuentes,2)
Fi = L.ExtCol(Fuentes,3)

#Ploteamos esto, y marcamos las que estén a ±1 y ±3 del sigma que va a ser 21
x = range(450,1550)
s = 21
plt.plot(x, [i for i in x])
plt.plot(x, [i+s for i in x], 'r--')
plt.plot(x, [i-s for i in x], 'r--')
plt.plot(x, [i+3*s for i in x], 'g--')
plt.plot(x, [i-3*s for i in x], 'g--')
color = ['c','r','g']
signo = ['o','^','*']

for i in range(len(Fo)):
    if Fi[i] < Fo[i] + s and Fi[i] > Fo[i] - s:
        tip=color[0]+signo[0]
    elif Fi[i] >= Fo[i] + s and Fi[i] < Fo[i] + 3*s:
        tip=color[2]+signo[2]
    elif Fi[i] <= Fo[i] - s and Fi[i] > Fo[i] - 3*s:
        tip=color[2]+signo[2]    
    else: 
        tip=color[1]+signo[1]
    plt.plot(Fo[i],Fi[i], tip)


plt.xlabel('Flujo ingresado')
plt.ylabel('Flujo obtenido')
plt.savefig('./Imagenes/comp.pdf',dpi=300,bbox_inches='tight')
#plt.show()
plt.close()

#--------------------------------------------------------------------------------------------------------------------------

#Escribiendo cosas en un txt 
file = open('./Imagenes/resultados.txt','w')

file.write(
    '---------------Datos de las fuentes--------------- \n'
    'y-crd: coordenada y\n'
    'x-crd: coordenada x\n'
    'f-in: flujo ingresado\n'
    'f-obt: flujo integrado\n'
    'f-obt/f-inc: la relación entre las dos cantidades anteriores\n'
    'f-conv: el flujo después de la convolución en las mismas coordenadas\n'
    'y-crd \t x-crd \t f-in \t f-obt \t f-obt/f-inc \t f-conv \n' 
)

for i in range(len(Fuentes)):
    file.write(
        str(Fuentes[i][0]) + '\t' + str(Fuentes[i][1]) + '\t' + str(Fuentes[i][2]) + '\t' + str(Fuentes[i][3]) + '\t' + str(Fuentes[i][4]) +'\n'
    )

file.write(
    '---------------Promedio de la razón de flujo obtenido/inicial--------------- \n'
)

fvar=0
for i in range(len(Fuentes)):
    fvar += Fuentes[i][4]
fprom = fvar/len(Fuentes)
file.write(
    str(fprom) + '\n'
)
