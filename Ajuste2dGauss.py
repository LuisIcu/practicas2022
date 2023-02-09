from astropy.convolution import convolve, Gaussian2DKernel
import numpy as np
import scipy, scipy.optimize
import matplotlib
from mpl_toolkits.mplot3d import  Axes3D
from matplotlib import cm # to colormap 3D surfaces from blue to red
import matplotlib.pyplot as plt

'''
Este programa sirve para recuperar el flujo y coordenadas de dos fuentes mediante un ajuste gaussiano
en dos dimensiones.
'''

graphWidth = 800 # units are pixels
graphHeight = 600 # units are pixels

# 3D contour plot lines
numberOfContourLines = 16

sigma = 6/2.355
gauss_2D_kernel = Gaussian2DKernel(sigma)

B=49
A = np.zeros((B,B))
A[20][20] = 700
A[31][31] = 1200

map = convolve(A,gauss_2D_kernel)

xData = np.array([])
yData = np.array([])
zData = np.array([])

for i in range(len(map)):
    for j in range(len(map[i])):
        yData= np.append(yData,i)
        xData= np.append(xData,j)
        zData= np.append(zData,map[j][i])

data = [xData, yData, zData]

def SurfacePlot(func, data, fittedParameters):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)

    matplotlib.pyplot.grid(True)
    axes = Axes3D(f)

    # extract data from the single list
    x_data = data[0]
    y_data = data[1]
    z_data = data[2]

    xModel = np.linspace(min(x_data), max(x_data), 200)
    yModel = np.linspace(min(y_data), max(y_data), 200)
    X, Y = np.meshgrid(xModel, yModel)

    Z = func(np.array([X, Y]), *fittedParameters)

    axes.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=1, antialiased=True)

    axes.scatter(x_data, y_data, z_data) # show data along with plotted surface

    axes.set_title('Surface Plot (click-drag with mouse)') # add a title for surface plot
    axes.set_xlabel('X Data') # X axis data label
    axes.set_ylabel('Y Data') # Y axis data label
    axes.set_zlabel('Flux') # Z axis data label

    plt.show()
    plt.close('all') # clean up after using pyplot or else there can be memory and process problems 

def func2(data, A, x1, y1, B, x2, y2):
    x = data[1]
    y = data[0]
    return A*np.exp(-((x-x1)**2+(y-y1)**2)/(2*sigma**2)) + B*np.exp(-((x-x2)**2+(y-y2)**2)/(2*sigma**2))

if __name__ == "__main__":    
    initialParameters = [15, 11, 17, 28,25,25] # these are the same as scipy default values in this example

    # here a non-linear surface fit is made with scipy's curve_fit()
    fittedParameters, pcov = scipy.optimize.curve_fit(func2, [xData, yData], zData, p0 = initialParameters)

    SurfacePlot(func2, data, fittedParameters)

    print('fitted parameters', fittedParameters)

    modelPredictions = func2(data, *fittedParameters) 

    absError = modelPredictions - zData

    SE = np.square(absError) # squared errors
    MSE = np.mean(SE) # mean squared errors
    RMSE = np.sqrt(MSE) # Root Mean Squared Error, RMSE
    Rsquared = 1.0 - (np.var(absError) / np.var(zData))
    print('RMSE:', RMSE)
    print('R-squared:', Rsquared)
    #print(map[15][18])
    #print(map[21][24])
    print('Volume1= ', 2*np.pi*fittedParameters[0]*sigma**2)
    print('Volume2= ', 2*np.pi*fittedParameters[3]*sigma**2)