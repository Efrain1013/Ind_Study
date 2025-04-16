import numpy as np

# Calculates the position of the minimum 
def kpath_position(kpoints, energies, kpoint_value, kpoint_name):

    max_index = np.where(energies == max(energies))[0]
    min_index = np.where(energies == min(energies))[0]
    if len(max_index) >= 1:
        max_index = max_index[0]
    if len(min_index) >= 1:
        min_index = min_index[0]

    # print(f"The minimum index is at {min_index}")
    min_energy = energies[min_index]

    max_kpoint = kpoints[max_index]
    min_kpoint = kpoints[min_index]

    band_is_cbm = 0
    if min_energy > 0:
        band_is_cbm = 1

    min_k_path_name = []

    if band_is_cbm:
        for i in range(len(kpoint_value)):
            if kpoint_value[i] <= min_kpoint <= kpoint_value[i+1]:
                min_k_path_name = [kpoint_name[i], kpoint_name[i+1]]
                path_amount = (min_kpoint - kpoint_value[i]) / (kpoint_value[i+1] - kpoint_value[i])
                return min_kpoint, min_k_path_name, path_amount
            
    elif not band_is_cbm:
        for i in range(len(kpoint_value)):
            if kpoint_value[i] <= max_kpoint <= kpoint_value[i+1]:
                max_k_path_name = [kpoint_name[i], kpoint_name[i+1]]
                path_amount = (max_kpoint - kpoint_value[i]) / (kpoint_value[i+1] - kpoint_value[i])
                return max_kpoint, max_k_path_name, path_amount
    else:
        raise ValueError('min_k_path_name is undefined')