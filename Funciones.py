import random
import matplotlib.pyplot as plt
from astropy.convolution import convolve, AiryDisk2DKernel, Gaussian2DKernel
import numpy as np
from scipy.optimize import curve_fit

#Funciones propias
#Me sirven para cosas en específico que uso para simplificar mis códigos


#Función para sacar la media de un array
def media(A):
    return np.sum(A)/len(A)

#Función para sacar la desviación estándar de un array
def stdv(A):
    mean = media(A)
    sum = np.sum((A-mean)**2)
    return np.sqrt(sum/(len(A)-1))

#Función para sacar la media de un array con valores absolutos
def mediaabs(A):
    return np.sum(np.abs(A))/len(A)

#Función para sacar la desviación estándar de un array con valores absolutos
def stdvabs(A):
    mean = mediaabs(A)
    sum = np.sum((np.abs(A)-mean)**2)
    return np.sqrt(sum/(len(A)-1))

#Función para sumar el flujo centrado en un punto con coordenadas (x,y) hasta un radio r
def SumRadio(A,x,y,r):
    Flux = 0
    for i in range(-r,r+1):
        for j in range(-r,r+1):
            if np.sqrt(i**2+j**2)<=r:
                Flux += A[x+i][y+j]
    return Flux

#Función para sumar el flujo centrado en un punto con coordenadas (x,y) desde un radio 1 hasta un radio r
def SumMultRadio(A,x,y,rmax,Freal):
    Fluxes = np.array([])
    for r in range(1,rmax):
        Flux = SumRadio(A,x,y,r)
        Fluxes = np.append(Fluxes,Flux)
    return Fluxes/Freal

#Extraer la columna de una matriz como un array aparte
def ExtCol(A,j):
    col = np.array([A[0][j]])
    for i in range(1,len(A)):
        col = np.append(col,A[i][j])
    return col

#Hallar máximo de un sector
def FindMax(A):
    max = np.max(A)
    xcord = np.where(A==max)[0][0]
    ycord = np.where(A==max)[1][0]
    return xcord, ycord

#Contar cuántas veces aparece algún arreglo de 2d (?) (hay que corregir esta descripción xd)
def Contar2d(A):
    x = np.array([A[0][0]])
    y = np.array([A[0][1]])
    z = np.array([1])

    for i in range(1,len(A)):
        f = 0
        for j in range(len(x)):
            if A[i][0] == x[j] and A[i][1]==y[j]:
                z[j]+=1
                f=1
                break
        if f == 0:
            x = np.append(x,A[i][0])
            y = np.append(y,A[i][1])
            z = np.append(z,1)
    return x, y, z


