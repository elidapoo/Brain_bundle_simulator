# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 10:03:34 2023

@author: Elida
"""

import numpy as np
import random as rn
import math
from geomdl import fitting
import generate_tubular_model as gtm


#%%Generate fourth-order splines with 21 points
def Approximate_funtion(points):
    
    degree =4# cubic curve
    
    
    # Do global curve approximation
    curve = fitting.approximate_curve(points, degree,ctrlpts_size=5)
    
 
    curve.delta = 0.048

    curve_points = curve.evalpts
    return curve_points

#%%Generate the points inside the circles of each section.These points are the control points of the splines.

def ControlPoints_funtion(centroide_point, rotated_points, numb_fibxcluster):
    general_point = []
    rotated_points = list(rotated_points.copy())
    rotated_points.append(rotated_points[0])
    punto_central=centroide_point
    radio_maximo = np.max(np.linalg.norm(rotated_points - punto_central, axis=1))
    
    for i in range(len(rotated_points) - 1):
        point1 = centroide_point
        point2 = rotated_points[i]
        point3 = rotated_points[i+1]
        
        # Coordenadas de los puntos del triángulo
        x = [point1[0], point2[0], point3[0]]
        y = [point1[1], point2[1], point3[1]]
        z = [point1[2], point2[2], point3[2]]
        
        # Coordenadas máximas y mínimas del triángulo
        max_x = max(x)
        max_y = max(y)
        max_z = max(z)
        
        min_x = min(x)
        min_y = min(y)
        min_z = min(z)
        
        # Puntos medios del triángulo
        mode_x = sum(x) - max_x - min_x
        mode_y = sum(y) - max_y - min_y
        mode_z = sum(z) - max_z - min_z
        
        # Generamos puntos aleatorios dentro del triángulo
        v1 = np.random.uniform(min_x, max_x, size=int(numb_fibxcluster[i]))
        v2 = np.random.uniform(min_y, max_y, size=int(numb_fibxcluster[i]))
        v3 = np.random.uniform(min_z, max_z, size=int(numb_fibxcluster[i]))
        
        # Proyectamos los puntos aleatorios sobre el plano del triángulo
        v1, v2, v3 = project_points_on_plane(v1, v2, v3, point1, point2, point3)
        
        # Calculamos la distancia de cada punto al centro y aplicamos la restricción del radio
        distancia_al_centro = np.linalg.norm(np.column_stack((v1, v2, v3)) - punto_central, axis=1)
        
        v1 = v1[distancia_al_centro <= radio_maximo]
        v2 = v2[distancia_al_centro <= radio_maximo]
        v3 = v3[distancia_al_centro <= radio_maximo]
        
        # Si no se generaron suficientes puntos, generamos más
        faltantes = int(numb_fibxcluster[i] - len(v1))
        while faltantes > 0:
            # Generamos puntos adicionales solo en la cantidad necesaria para alcanzar la meta
            nuevos_v1 = np.random.uniform(min_x, max_x, size=faltantes)
            nuevos_v2 = np.random.uniform(min_y, max_y, size=faltantes)
            nuevos_v3 = np.random.uniform(min_z, max_z, size=faltantes)
            
            # Filtramos los puntos adicionales
            distancia_al_centro = np.linalg.norm(np.column_stack((nuevos_v1, nuevos_v2, nuevos_v3)) - punto_central, axis=1)
            nuevos_v1 = nuevos_v1[distancia_al_centro <= radio_maximo]
            nuevos_v2 = nuevos_v2[distancia_al_centro <= radio_maximo]
            nuevos_v3 = nuevos_v3[distancia_al_centro <= radio_maximo]
            
            # Agregamos los puntos adicionales
            v1 = np.concatenate((v1, nuevos_v1))
            v2 = np.concatenate((v2, nuevos_v2))
            v3 = np.concatenate((v3, nuevos_v3))
            
            faltantes = int(numb_fibxcluster[i] - len(v1))
        
        # Agregamos los puntos generados a la lista
        general_point.append(np.column_stack((v1, v2, v3)))
    
    return general_point

def project_points_on_plane(x, y, z, point1, point2, point3):
    # Calculamos el vector normal al plano del triángulo
    v1 = np.array(point2) - np.array(point1)
    v2 = np.array(point3) - np.array(point1)
    normal = np.cross(v1, v2)
    
    # Normalizamos el vector normal
    normal = normal / np.linalg.norm(normal)
    
    # Calculamos la ecuación del plano Ax + By + Cz + D = 0
    A, B, C = normal
    D = -np.dot(normal, point1)
    
    # Proyectamos los puntos sobre el plano
    t = (-D - A * x - B * y - C * z) / (A**2 + B**2 + C**2)
    v1 = x + A * t
    v2 = y + B * t
    v3 = z + C * t
    
    return v1, v2, v3


#%%Spline generation by circular sector
def splines_simulator(fiber_points,radio_list,centroide,numb_fib_total):
    point_list=centroide[fiber_points] #centroide[[0,5,10,15,20]]

    points_all_spline,d_list=gtm.allpoints_generator(radio_list,centroide, point_list)  ###quitar_p2_list                   
    numb_points=len(points_all_spline)
    paso=round(numb_fib_total/numb_points)
    number_fiber_per_cluster=paso*np.ones(numb_points)
    result=sum(number_fiber_per_cluster)
    if result<numb_fib_total:
        number_fiber_per_cluster[0]=number_fiber_per_cluster[0]+(numb_fib_total-result)
    else:
        number_fiber_per_cluster[0]=number_fiber_per_cluster[0]-(result-numb_fib_total)   
    general_general_point=[]
    for ik in range(len(d_list)):
        general_point=ControlPoints_funtion(centroide[fiber_points[ik]],d_list[ik],number_fiber_per_cluster)
        general_general_point.append(general_point)
    spline_all=[]    
    for i in range(len(general_general_point[0])):
        splinexsector=[]    
        for j in range (len(general_general_point[0][i])) :
        
            points_spline=[]
            for k in range (len(general_general_point)):
                points_spline.append(general_general_point[k][i][j])
                
            
            spline= Approximate_funtion(points_spline)
            splinexsector.append(np.array(spline).astype('float32'))
        spline_all.append(splinexsector)
        
    return spline_all, points_all_spline,d_list

