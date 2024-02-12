# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 11:28:03 2022

@author: Elida
"""
import numpy as np
import math
from math import cos,sin
import random as rn
from scipy.interpolate import splprep, splev


#%%Generate a 3x3 random vector

def getRandomVect(mu, sigma):
         vect = np.zeros([3], dtype = 'float32')
         vect[0] = rn.gauss(mu, sigma)
         vect[1] = rn.gauss(mu, sigma)
         vect[2] = rn.gauss(mu, sigma)
         
         return vect
#%% Finding the point to rotate around the centroid

def find_point_to_rotate(radio,point,p1,vd):
    
    D=-(vd[0]*p1[0]+ vd[1]*p1[1]+ vd[2]*p1[2]) #valor D del plado
    
    r=0
    c=0
    h=[]   
    while True:
        vect = getRandomVect(0,radio)
        point_to_rotate=vect+point
        
        #comprobar si el punto pertenece al plano
        D_comp=-(point_to_rotate[0]*vd[0]+ point_to_rotate[1]*vd[1]+ point_to_rotate[2]*vd[2])
                
        if round(D_comp,2)==round(D,2):
      
            r=math.sqrt((point_to_rotate[0]-point[0])**2 + (point_to_rotate[1]-point[1])**2 + (point_to_rotate[2]-point[2])**2)
            vd1=[(point_to_rotate[0]-p1[0]),(point_to_rotate[1]-p1[1]),(point_to_rotate[2]-p1[2])]
            g=vd[0]*vd1[0]+ vd[1]*vd1[1] +vd[2]*vd1[2]
            h.append(g)
                      
            if  round(r)==radio and abs(round(g,3))==0.0:  #
                                                         
                   break
                                                      
        c+=1
    return point_to_rotate, r,c,g,vd,vd1,D 

#%%

def PointRotate3D(punto, punto_de_rotacion, eje_rotacion, angulo_rotacion):
    # Restar el punto de rotación al punto original para obtener el vector relativo
    vector_rel = punto - punto_de_rotacion
    
    # Convertir el ángulo de rotación a radianes
    angulo_rad = angulo_rotacion
    
    # Calcular la matriz de rotación
    cos_ang = np.cos(angulo_rad)
    sin_ang = np.sin(angulo_rad)
    ux, uy, uz = eje_rotacion / np.linalg.norm(eje_rotacion)
    
    matriz_rot = np.array([[cos_ang + ux**2*(1 - cos_ang), ux*uy*(1 - cos_ang) - uz*sin_ang, ux*uz*(1 - cos_ang) + uy*sin_ang],
                           [uy*ux*(1 - cos_ang) + uz*sin_ang, cos_ang + uy**2*(1 - cos_ang), uy*uz*(1 - cos_ang) - ux*sin_ang],
                           [uz*ux*(1 - cos_ang) - uy*sin_ang, uz*uy*(1 - cos_ang) + ux*sin_ang, cos_ang + uz**2*(1 - cos_ang)]])
    
    # Aplicar la matriz de rotación al vector relativo
    vector_rot = np.dot(matriz_rot, vector_rel)
    
    # Sumar el vector rotado al punto de rotación para obtener el punto rotado final
    punto_rotado = punto_de_rotacion + vector_rot
    
    return punto_rotado
#%%

def find_perpendicular_vector(point, vector):
    # Punto
    x1, y1, z1 = point
    
    # Vector
    a, b, c = vector
    
    # Resolver ecuación para obtener una variable desconocida
    y = 10  # Puedes elegir cualquier valor arbitrario
    
    # Calcular el valor correspondiente de la variable desconocida
    x = (-b*y - c*z1) / a
    z = (-a*x1 - b*y) / c
    
    # Construir el vector perpendicular
    perpendicular_vector = np.array([x, y, z])
    
    return perpendicular_vector   
#%%Find the tangent vector to the centroid point corresponding to the rotation axis.
def tangent_function (centroide,point):
    x=centroide[:,0]
    y=centroide[:,1]
    z=centroide[:,2]
    
    # Combine the coordinates into a single array
    points = np.array([x, y, z])
    
    # Fit a B-spline curve to the points
    tck, u = splprep(points, s=0)
    
    # Define the point (x, y, z) at which to find the tangent
    point =centroide[0] #np.array([2, 4, 1])  # Example: [2, 4, 1]
    
    # Find the parameter 't' that corresponds to the closest point on the curve to the given point
    distances = np.linalg.norm(points - point[:, np.newaxis], axis=0)
    u_closest = distances.argmin()
    t_closest = u[u_closest]
    
    # Calculate the derivatives of the curve at the closest point
    derivative_order = 1  # Order of the derivative (1 for tangent)
    curve_derivatives = splev(t_closest, tck, der=derivative_order)
    
    # Calculate the tangent vector
    tangent_vector = np.array(curve_derivatives)
    
    # Normalize the tangent vector to get the unit tangent vector
    tangent_unit_vector = tangent_vector / np.linalg.norm(tangent_vector)
    

    return tangent_unit_vector 
#%%Generate the 8 points that form the circles of each section.
def allpoints_generator(radio_list, centroide, point_list):
    d_list = []
    dist1_list_list = []

    for i in range(len(point_list)):
        p1 = point_list[i]

        if i == 0:
            point_to_rotate,r,c,g,vd,vd1,D= find_point_to_rotate(radio_list[i], point_list[i], point_list[i], tangent_function(centroide, point_list[i]))
        else:
            alfa = radio_list[i] / radio_list[0]
            point_recta = [(alfa * vd1[0] + p1[0]), (alfa * vd1[1] + p1[1]), (alfa * vd1[2] + p1[2])]
            point_to_rotate = point_recta
            r = math.sqrt((point_to_rotate[0] - p1[0]) ** 2 + (point_to_rotate[1] - p1[1]) ** 2 + (point_to_rotate[2] - p1[2]) ** 2)

  
        d = []
        theta_list = np.radians(np.arange(0, 360, 45))
        for theta in theta_list:
            result = PointRotate3D(point_to_rotate, p1, tangent_function(centroide, p1), theta)

            d.append(result)

        d_list.append(d)


    points_all_spline = []

    for i in range(len(d_list[0])):
        points_spline = []
        for j in range(len(d_list)):
            points_spline.append(d_list[j][i])
        points_all_spline.append(np.array(points_spline))

    return points_all_spline, d_list

