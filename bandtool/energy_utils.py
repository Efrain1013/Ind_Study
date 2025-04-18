import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Function to normalize energies to valence band maximum and to find valence and conduction band index
def norm_energies(all_energies):
    val_index = -1     # First iteration will go to index 0 (band no. 1)
    con_index = -1

    ndeg_val_bands = -1
    ndeg_con_bands = -1

    max_val_energy = -float('inf')
    
    for band in all_energies:
        max_of_band = max(band)
        
        if max_of_band < 0. or min(band) < 0:     # Stop when max bands > 0 i.e. val band has some +energy
            val_index += 1
            con_index = val_index + 1     # Conduction band would be the next highest band after the upmost valence band
            max_val_energy = max_of_band
    
    min_con_energy = min(all_energies[con_index])
    
    for i in range(con_index, min(con_index + 10, len(all_energies))):
        print(f"con_index = {con_index}, len(all_energies) = {len(all_energies)}")
        if -1.0E-17 < max(all_energies[i]) - max_val_energy < 1.0E-17:
            ndeg_val_bands += 1
        if -1.0E-17 < min(all_energies[i]) - min_con_energy < 1.0E-17:
            ndeg_con_bands += 1

    
    vert_shift = max_val_energy     # Get the shift from 0
    band_gap = min_con_energy - max_val_energy
    all_energies_norm = np.array(all_energies) - vert_shift     # If max(val) is > 0 we bring it down, min(val) < 0 bring up

    return all_energies_norm, val_index, ndeg_val_bands, con_index, ndeg_con_bands, band_gap

def parabola(x, a, b, c):
    return a * x ** 2 + b * x + c

def fit_check(fit_ks, fit_Es, con_ks, con_Es, kpoint_values, kpoint_labels, plot_name, index, ISCBM):
    mid_k = 0.

    if sum(fit_Es) > 0:
        ind = np.where(fit_Es == min(fit_Es))
        mid_k = fit_ks[ind]
    elif sum(fit_Es) < 0:
        ind = np.where(fit_Es == max(fit_Es))
        mid_k = fit_ks[ind]

    infinity = float('inf')
    fit_bounds = [[-infinity, -infinity, -infinity, -infinity], [infinity, infinity, infinity, infinity]]

    fig, ax = plt.subplots(figsize=(12, 8))
    plt.title(plot_name)
    plt.ylim(min(con_Es)-0.25, max(con_Es)+0.25)
    plt.xlim(min(con_ks), max(con_ks))
    plt.xlabel("k-points")
    plt.ylabel("E(k) (eV)")
    ax.tick_params(axis='both', which='both', labelsize=11)
    plt.xticks(kpoint_values, kpoint_labels)
    
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight('regular')
        label.set_fontsize(12)
        label.set_fontname('DejaVu Sans')  # Optional: pick a good bold font
        
    plt.plot(con_ks, con_Es, color='black')
    for sym_point in kpoint_values[1:-1]:
        plt.axvline(sym_point, alpha = 0.15, color='black', linestyle=':')
        
    plt.plot(fit_ks, fit_Es, color='red', linestyle='--')
    plt.axvline(mid_k, alpha = 0.4)
    if ISCBM:
        plt.savefig("Fit_Check_CBM" + str(index) + ".png")
    else:
        plt.savefig("Fit_Check_VBM" + str(index) + ".png")

def fit_parabola(kpoints, energies, min_kpoint_value, nkpts, kpoint_labels):
    min_kpoint_index = np.where(kpoints == min_kpoint_value)[0][0]
    num_of_paths = len(kpoint_labels) - 1
    kpoints_per_path = nkpts / num_of_paths
    num_of_points = int(kpoints_per_path // 20 - 1)
    upper = int(min_kpoint_index + num_of_points + 1)
    lower = int(min_kpoint_index - num_of_points)
    # print(upper, lower)
    fit_krange = kpoints[lower:upper]
    fit_Erange = energies[lower:upper]

    fit_params, fit_cov = curve_fit(parabola, fit_krange, fit_Erange)
    a_fit, b_fit, c_fit = fit_params
    fit_kpoints = np.linspace(kpoints[lower]-0.5, kpoints[upper]+0.5, 100)
    # print(fit_kpoints)
    fit_energies = parabola(fit_kpoints, a_fit, b_fit, c_fit)
    # print(fit_energies)
    
    return fit_kpoints, fit_energies, a_fit

def find_mass_eff(LC_Ek):
    d2Edk2 = 2. * LC_Ek * (1.602176634E-19) * ((1.0E-10)**2)   # Convert from LC (eVA^2) to Jm^2
    mass = (1.054571817E-34)**2 / d2Edk2
    mass_ratio = mass / (9.1093837E-31)
    return mass, mass_ratio

# hbar = 1.054571817E-34          hbar in Js
# m_elec = 9.1093837E-31          in kg
# eVtoJ = 1.602176634E-19         J/eV
# AngtoMet = 1.0E-10              m/A
