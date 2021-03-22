import numpy as np
import matplotlib.pyplot as plt
import random
from scipy import signal
from OneDCalculation import array_factor, sparse_array_sidepeak, array_plot
from PSO import PSO


def fitness_func(xn_sparse):
    resolution = 10000
    wav = 1.55
    xn_sparse = np.asarray(xn_sparse)
    An_sparse = np.ones_like(xn_sparse)
    varphin_sparse = np.zeros_like(xn_sparse)
    phi_sparse, p_sparse = array_factor(xn_sparse, varphin_sparse, An_sparse, wav, resolution)
    max_peak_angle, max_peak_power = sparse_array_sidepeak(p_sparse, phi_sparse)
    return max_peak_power



if __name__ == '__main__':

    N_sparse = 32
    ArraySize = 256.0
    average_gap = ArraySize/N_sparse
    xn_sparse = np.zeros(N_sparse)
    min_gap = 4
    xn_sparse[-1] = ArraySize

    xn = np.linspace(0.0, ArraySize, N_sparse)
    initial = xn + np.random.rand(N_sparse)

    for i in range(int(N_sparse/2-1)):
        xn_sparse[i+1] = xn_sparse[i]+(min_gap + np.random.rand() * (average_gap-min_gap)*2.0)
    for i in range(int(N_sparse/2-1)):
        xn_sparse[N_sparse-i-2] = xn_sparse[N_sparse-i-1]-(min_gap + np.random.rand() * (average_gap-min_gap)*2.0)
    xn_sparse = np.around(xn_sparse, decimals=1)

    # initial = [x1,x2...]
    # bounds = [(x1_min,x1_max),(x2_min,x2_max)...]

    N_p = 50
    Maxiter = 200

    best_xn_sparse = np.asarray(PSO(fitness=fitness_func, x0=xn_sparse, bounds=min_gap, num_particles=N_p, maxiter=Maxiter).run_PSO())

    resolution = 10000
    wav = 1.55
    An_sparse = np.ones_like(best_xn_sparse)
    varphin_sparse = np.zeros_like(best_xn_sparse)
    best_phi_sparse, best_p_sparse = array_factor(best_xn_sparse, varphin_sparse, An_sparse, wav, resolution)
    best_p_sparse_log = 10 * np.log10(best_p_sparse)
    array_plot(best_phi_sparse, best_p_sparse_log)
    plt.ylim([-15, 0])
    plt.show()

