# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 11:28:16 2023

@author: Elida
"""


import numpy as np
import random as rn
import generate_splines as sp
from generate_tubular_model import getRandomVect
import os


import random as rn

def generate_radio_list(r1_range, r2_range, r3_range, r4_range, r5_range):
    # Validar que los rangos sean válidos
    for r_range in [r1_range, r2_range, r3_range, r4_range, r5_range]:
        if len(r_range) != 2 or r_range[0] >= r_range[1]:
            raise ValueError("Invalid range format. Each range must be in the format [min, max] with min < max.")

    # Validar que los máximos de los radios estén en el orden correcto
    if r1_range[1] <= r2_range[1] or r2_range[1] <= r3_range[1] or r4_range[1] <= r3_range[1] or r5_range[1] <= r4_range[1]:

        raise ValueError("Maximum value of each range must be in increasing order: r1 > r2 > r3 < r4 < r5.")

    while True:
        # Generar radios aleatorios dentro de los rangos especificados
        r1 = rn.randint(*r1_range)
        r2 = rn.randint(*r2_range)
        r3 = rn.randint(*r3_range)
        r4 = rn.randint(*r4_range)
        r5 = rn.randint(*r5_range)
        
        if r1 > r2 and r2 > r3 and r3 < r4 and r4 < r5:
            return [r1, r2, r3, r4, r5]

def generate_fiber_parameters(final_centroid_to_simu, r1_range, r2_range, r3_range, r4_range, r5_range, numb_fib_total_range):
    simulated_tractography = []
    par_list = []

    for centroide in final_centroid_to_simu:
        numb_fib_total = rn.randint(*numb_fib_total_range)
        radio_list = generate_radio_list(r1_range, r2_range, r3_range, r4_range, r5_range)
        par_list.append((numb_fib_total, radio_list))

        fiber_points = [0, 3, 10, 17, 20]
        spline_all, _, _ = sp.splines_simulator(fiber_points, radio_list, centroide, numb_fib_total)
        lista_unica = sum(spline_all, [])

        simulated_tractography.append(lista_unica)
      
    for idx, _ in enumerate(final_centroid_to_simu):
        print('Terminado Fascículo', idx)

    return simulated_tractography, par_list

def generate_noise(simulated_tractography,mu,sigma_range):
   sigma_list = np.linspace(sigma_range[0], sigma_range[1], len(simulated_tractography))
   numb_point=5
   simulated_tractography_random2=[]
   c=0
   for d in simulated_tractography:  
       aplastada=[]
       sigma=sigma_list[c]
       c+=1
       for d1 in d: 
            vect=getRandomVect(mu, sigma)
         
            random_numbers=np.linspace(-1, 0,5)
         
            resultado = np.array([i * vect for i in random_numbers])
            d1_copy = d1.copy()
            d1_copy[0:numb_point] += resultado
            d1_copy = d1_copy[::-1]
            d1_copy[0:numb_point] += resultado
            d1_copy = d1_copy[::-1]
            
            aplastada.append(d1_copy)
    
                    
    
       simulated_tractography_random2.append(aplastada)
   return simulated_tractography_random2  


def generate_labels(simulated_tractography):
    n = 0
    index_sim_tractography = []

    for i in simulated_tractography:
        index_list = np.arange(n, n + len(i))
        n = index_list[-1] + 1
        index_sim_tractography.append(index_list)
        
        


    with open('resultados/labels.txt', 'w') as f:
        for index_list in index_sim_tractography:
            f.write(' '.join(map(str, index_list)) + '\n')




