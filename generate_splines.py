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

def ControlPoints_funtion(centroide_points,rotated_points,numb_fibxcluster):# paso:numero de fibras entre a fib lejana y el centroide
    general_point=[]
    rotated_points=list(rotated_points.copy())
    rotated_points.append(rotated_points[0])
    for i in range(len (rotated_points)-1):
        point1=centroide_points
        point2=rotated_points[i]
        point3=rotated_points[i+1]
                        
        x=[point1[0],point2[0],point3[0]]
        y=[point1[1],point2[1],point3[1]]
        z=[point1[2],point2[2],point3[2]]
        
        
        
        max_x=max(point1[0], point2[0],point3[0])
        max_y=max(point1[1], point2[1],point3[1])
        max_z=max(point1[2], point2[2],point3[2])
        
        min_x=min(point1[0], point2[0],point3[0])
        min_y=min(point1[1], point2[1],point3[1])
        min_z=min(point1[2], point2[2],point3[2])
        
        mode_x=sum(x)-max_x-min_x
        mode_y=sum(y)-max_y-min_y
        mode_z=sum(z)-max_z-min_z
            
 
        # v1=np.random.triangular(min_x,mode_x,max_x, size=int(numb_fibxcluster[i]))
        # v2=np.random.triangular(min_y,mode_y,max_y, size=int(numb_fibxcluster[i]))
        # v3=np.random.triangular(min_z,mode_z,max_z, size=int(numb_fibxcluster[i]))
        v1=np.random.uniform(min_x,max_x, size=int(numb_fibxcluster[i]))
        v2=np.random.uniform(min_y,max_y, size=int(numb_fibxcluster[i]))
        v3=np.random.uniform(min_z,max_z, size=int(numb_fibxcluster[i]))
        

        
        point_list=[]
        for k in range(int(numb_fibxcluster[i])):
        
            point=[v1[k],v2[k],v3[k]]
        
        
            point_list.append(point)
        general_point.append(point_list)

    
    return general_point
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



