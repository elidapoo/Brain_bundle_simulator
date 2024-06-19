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
def find_point_to_rotate(radio, point, p1, vd):
    D = -(vd[0]*p1[0] + vd[1]*p1[1] + vd[2]*p1[2])  # valor D del plano
    
    while True:
        vect = getRandomVect(0, radio)
        point_to_rotate = vect + point
        
        # comprobar si el punto pertenece al plano
        D_comp = -(point_to_rotate[0]*vd[0] + point_to_rotate[1]*vd[1] + point_to_rotate[2]*vd[2])
        
        if round(D_comp, 2) == round(D, 2):
            r = np.linalg.norm(point_to_rotate - point)
            vd1 = point_to_rotate - p1
            g = np.dot(vd, vd1)
            
            if round(r) == radio and abs(round(g, 3)) == 0.0:
                break
                
    return point_to_rotate, vd1
#%%

def PointRotate3D(punto, punto_de_rotacion, eje_rotacion, angulo_rotacion):
   
    vector_rel = punto - punto_de_rotacion
    

    angulo_rad = angulo_rotacion
    

    cos_ang = np.cos(angulo_rad)
    sin_ang = np.sin(angulo_rad)
    ux, uy, uz = eje_rotacion / np.linalg.norm(eje_rotacion)
    
    matriz_rot = np.array([[cos_ang + ux**2*(1 - cos_ang), ux*uy*(1 - cos_ang) - uz*sin_ang, ux*uz*(1 - cos_ang) + uy*sin_ang],
                            [uy*ux*(1 - cos_ang) + uz*sin_ang, cos_ang + uy**2*(1 - cos_ang), uy*uz*(1 - cos_ang) - ux*sin_ang],
                            [uz*ux*(1 - cos_ang) - uy*sin_ang, uz*uy*(1 - cos_ang) + ux*sin_ang, cos_ang + uz**2*(1 - cos_ang)]])
 
    vector_rot = np.dot(matriz_rot, vector_rel)
    

    punto_rotado = punto_de_rotacion + vector_rot
    
    return punto_rotado


#%%

def find_perpendicular_vector(point, vector):
  
    x1, y1, z1 = point
    

    a, b, c = vector
    
   
    y = 10  
    
  
    x = (-b*y - c*z1) / a
    z = (-a*x1 - b*y) / c
    

    perpendicular_vector = np.array([x, y, z])
    
    return perpendicular_vector 
#%%
def tangent_function1(centroide,point):
    x=centroide[:,0]
    y=centroide[:,1]
    z=centroide[:,2]
    
    points = np.array([x, y, z])
    
    tck, u = splprep(points, s=0)
    
   
    point =centroide[0] 

    distances = np.linalg.norm(points - point[:, np.newaxis], axis=0)
    u_closest = distances.argmin()
    t_closest = u[u_closest]
    
    
    derivative_order = 1 
    curve_derivatives = splev(t_closest, tck, der=derivative_order)
    
 
    tangent_vector = np.array(curve_derivatives)

    tangent_unit_vector = tangent_vector / np.linalg.norm(tangent_vector)
    

    return tangent_unit_vector  

def tangent_function(points, index):
    if index == 0:
        tangent = points[1] - points[0]
    elif index == len(points) - 1:
        tangent = points[-1] - points[-2]
    else:
        tangent = points[index + 1] - points[index - 1]
    return tangent / np.linalg.norm(tangent)





#%%Generate the 8 points that form the circles of each section.
def allpoints_generator(radio_list, centroide, point_list):
    d_list = []
    idx = [0, 3, 10, 17, 20]
    d_list = []
 

    for i in range(len(point_list)):
        p1 = point_list[i]
    
     
            
        V = tangent_function(centroide,idx[i])
    
        W = np.cross(V, [0, 0, 1])
        W_norm = W / np.linalg.norm(W)
        point_recta = p1 + radio_list[i] * W_norm
        point_to_rotate = point_recta
        d = []
        theta_list = np.radians(np.arange(0, 360, 45))
        for theta in theta_list:
            result = PointRotate3D(point_to_rotate, p1, V, theta)
    
            d.append(result)
    
        d_list.append(d)
    
    points_all_spline = []
    for i in range(len(d_list[0])):
        points_spline = []
        for j in range(len(d_list)):
            points_spline.append(d_list[j][i])
        points_all_spline.append(np.array(points_spline))

    return points_all_spline, d_list