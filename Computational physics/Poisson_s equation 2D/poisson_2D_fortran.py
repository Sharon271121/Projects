# -*- coding: utf-8 -*-
"""poisson2D_sharon

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_aMrbGnPM7yErv0Js3T3GTsD5yLtRM-v

**Ecuación
 de Poisson aplicando el método pseudo-espectral**


 
 Sharon Navarro
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import lu_factor, lu_solve

#Numero de colocación
N = eval(input("Numero of colocations points:"  ))
Nx = eval(input("Numero of grid points x:"  ))
Ny = eval(input("Numero of grid points y:"))
#lamb = eval(input("lambda = 4.0 default:" ))


#FUNCIONES DE CHEBYSHEV
def cheby(m,r):
  cheby0 = 1
  cheby1 = r
  chebyn = 0
  if m == 0:
    cheby = cheby0
  elif m == 1:
    cheby = cheby1
  elif m >= 2:
    for i in range(2, m+1):
      chebyn = 2*r*cheby1 - cheby0
      cheby0 = cheby1
      cheby1 = chebyn
    cheby = chebyn
  return cheby 
#print(cheby(2,r))

#DERIVADAS DE CHEBYSHEV
def dcheby(m,r):
  dcheby0 = 0
  dcheby1 = 1
  dchebyn = 0
  if m == 0:
    dcheby = dcheby0
  elif m == 1:
    dcheby = dcheby1
  elif m >= 2:
    for i in range(2,m+1):
      dchebyn = 2*cheby(i-1,r) + 2*r*dcheby1 - dcheby0
      dcheby0 = dcheby1
      dcheby1 = dchebyn
    dcheby = dchebyn
  return dcheby 
#print(dcheby(2,r))


#SEGUNDAS DERIVADAS DE CHEBYSHEV
def ddcheby(m,r):
  ddcheby0 = 0
  ddcheby1 = 0
  ddchebyn = 0
  if m == 0:
    ddcheby = ddcheby0
  elif m == 1:
    ddcheby = ddcheby1
  elif m >= 2:
    for i in range(2,m+1):
      ddchebyn = 4*dcheby(i-1,r) + 2*r*ddcheby1 - ddcheby0
      ddcheby0 = ddcheby1
      ddcheby1 = ddchebyn
    ddcheby = ddchebyn
  return ddcheby 
#print(ddcheby(1,x))

x0 = 1
y0 = 1
#Fuente 
def f(x,y):
  f = (np.exp(x-x0)**2)*np.exp(x-y0)**2
  return f

#Puntos de colocación 
xmin = -1
xmax = 1
ymin= -1
ymax = 1

x = np.zeros((N+1))
y = np.zeros((N+1))

for i in range(0, N + 1):
  x[i]= np.cos(np.pi*i/N)
  y[i]= np.cos(np.pi*i/N)

A = np.zeros(((N+1)**2, (N+1)**2)) #MATRIZ
#A = [0,0 ]
#DEFINICIÓN DE LA MATRIZ A:

for i in range(0,N+1):
  for j in range(0,N+1):
    for l in range(0,N+1):
      for k in range(0,N+1):
        if i == 0 or i == N or j == 0 or j == N:
          A[i*(N+1) + j, l*(N+1) + k] = cheby(l, x[i])*cheby(k, y[j]) #Para las condiciones de frontera
        else:
          A[i*(N+1) + j, l*(N+1) + k] = ddcheby(l, x[i])*cheby(k, y[j]) + cheby(l, x[i])*ddcheby(k, y[j]) #Laplaciano

#DEFINICIÓN DEL VECTOR FUENTE: 

b = np.zeros((N+1)**2)
for i in range(0,N+1):
  for j in range(0, N+1):
    if i==0 or i ==N or j==0 or j==N:
      b[i*(N+1) + j]= 0
    else:
      b[i*(N+1) + j] = f(x[i], y[j])


#OPERAR PARA ENCONTRAR EL VECTOR SOLUCIÓN 
lu, piv = lu_factor(A)
X = lu_solve((lu, piv), b)

#GRAFICAR
x_ = np.linspace(-1, 1, Nx)
y_ = np.linspace(-1, 1, Ny)

r_x, r_y= np.meshgrid(x_, y_)

solution = np.zeros((N+1, N+1))

for i in range(0,N+1):
  for j in range(0,N+1):
    solution[i,j] = X[i*(N+1) + j]

sol=0
for i in range(0,N+1):
  for j in range(0,N+1):
    sol+= solution[i,j]*cheby(i, r_x)*cheby(j, r_y)

t = plt.axes(projection = '3d')
t.plot_surface(r_x, r_y, sol, cmap = 'viridis')
t.set_xlabel('x')
t.set_ylabel('y')
plt.show()