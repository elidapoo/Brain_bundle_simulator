# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 14:52:57 2023

@author: Elida
"""

import os
import BTools as bt
import numpy as np
import generate_parameters as gp  
import time
inicio = time.time()


def main():
    # Input Parameters (default settings change them for your application)
    ######################################
    r1_range = [8, 10]
    r2_range = [6, 8]
    r3_range = [5, 7]
    r4_range = [6, 8]
    r5_range = [8, 10]
    numb_fib_total_range = [50, 300]
    mu = 0
    sigma_range = [2.5,3.5]
    centroids, _ = bt.read_bundle('Example/100centroides.bundles')
    centroids=centroids[0:2]
    ######################################
  
    if not os.path.exists("resultados"):
        os.makedirs("resultados")

    if sigma_range == 0 or sigma_range == [0]:
        simulated_tractography, par_list = gp.generate_fiber_parameters(centroids, r1_range, r2_range, r3_range, r4_range, r5_range, numb_fib_total_range)
        gp.generate_labels(simulated_tractography)
        with open('resultados/parametros.txt', 'w') as f:
            f.write('radios: ' + ', '.join(map(str, par_list)))
        bt.write_bundle_severalbundles('resultados/simulated_tractography.bundles', simulated_tractography)
    else:
        simulated_tractography, par_list = gp.generate_fiber_parameters(centroids, r1_range, r2_range, r3_range, r4_range, r5_range, numb_fib_total_range)

        with open('resultados/parametros.txt', 'w') as f:
            f.write('radios: ' + ', '.join(map(str, par_list)))

        simulated_tractography_disperse = gp.generate_noise(simulated_tractography, mu, sigma_range)
        gp.generate_labels(simulated_tractography_disperse)
        bt.write_bundle_severalbundles('resultados/simulated_tractography.bundles', simulated_tractography)

if __name__ == "__main__":
    main()



fin = time.time()
print(fin-inicio)    
import visual_tools as vs

simulated_tractography, _ = bt.read_bundle_severalbundles('resultados/simulated_tractography.bundles')

vs.visual_allpoints(simulated_tractography[0:2])


