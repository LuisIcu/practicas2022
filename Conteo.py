import matplotlib.pyplot as plt     
import numpy as np

n = 30

file = open('./cat1100.dat','r')
data = [line.replace('\n','').split(' ') for line in file]
file.close()

FluxPyBDSF = np.array([])
FluxCat = np.array([])

print(data[1][6],data[1][7])
for i in range(1,len(data)):
    FluxPyBDSF = np.append(FluxPyBDSF,float(data[i][7]))
    FluxCat = np.append(FluxCat,float(data[i][6]))


#------------Histogramas diferenciales

#--------Histograma Flujos PyBDSF
minP = min(FluxPyBDSF)
maxP = max(FluxPyBDSF)
dx = (maxP-minP)/n
intervalos1 = [minP + i*dx for i in range(n+1)]
count1, bins1, ignored1 =  plt.hist(x=FluxPyBDSF,bins=intervalos1,label='Histograma de flujos')
bins12 = np.array([])
for i in range(len(bins1)-1):
    bins12 = np.append(bins12,(bins1[i]+bins1[i+1])/2)
plt.close()

#--------Histograma Flujos catálogo
minC = min(FluxCat)
maxC = max(FluxCat)
dx = (maxC-minC)/n
intervalos2 = [minC + i*dx for i in range(n+1)]
count2, bins2, ignored2 =  plt.hist(x=FluxCat,bins=intervalos2,label='Histograma de flujos')
bins22 = np.array([])
for i in range(len(bins2)-1):
    bins22 = np.append(bins22,(bins2[i]+bins2[i+1])/2)
plt.close()




plt.plot(bins12,count1,'ro--',label='Conteo del PyBDSF')
plt.plot(bins22,count2,'bo--',label='Conteo del catálogo')

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Flux Density (mJy)')
plt.ylabel(r'$dN/dS$ (mJy$^{-1}$ deg$^{-2}$)')
plt.title('Conteo diferencial')
#plt.xtic(ks(intervalos2)
plt.legend()
plt.savefig('./Imagenes/ConteoDiferencial.pdf',dpi=600,bbox_inches='tight')
#plt.show()
plt.close()


#Conteo de fuentes para los dos catálogos anteriores
Ftot1 = sum(count1)
ConteoP = [Ftot1]
for i in range(len(count1)):
    Ftot1 = Ftot1 - count1[i]
    ConteoP.append(Ftot1)
plt.plot(bins1,ConteoP,'r--',label='Conteo de PyBDSF')


Ftot2 = sum(count2)
ConteoC = [Ftot2]
for i in range(len(count2)):
    Ftot2 = Ftot2 - count2[i]
    ConteoC.append(Ftot2)
plt.plot(bins2,ConteoC,'b--',label='Conteo del catálogo')


plt.yscale('log')
plt.xscale('log')
plt.title('Conteo acumulativo')
plt.legend()
plt.xlabel('Flux density (mJy)')
plt.ylabel(r'$N(>S)$ deg$^{-2}$')
plt.title('Histograma de fuentes')
plt.savefig('./Imagenes/ConteoAcumulativo.pdf',dpi=600,bbox_inches='tight')
#plt.show()