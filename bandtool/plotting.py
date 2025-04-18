import matplotlib.pyplot as plt

def plot_bands(all_kpoints, all_energies, kpoint_values, kpoint_labels, nkpts):
    one_array = 0
    if len(all_energies) == nkpts:
        one_array = 1
        minimum_E = min(all_energies)/ 2. - 0.2
        maximum_k = max(all_kpoints)
    else:
        minimum_E = min([min(band) for band in all_energies]) / 2. - 0.2
        maximum_k = max([max(kline) for kline in all_kpoints])
    maximum_E = max(all_energies)
    
    fig1, ax1 = plt.subplots(figsize=(12, 8))
    plt.title("Band Structure", fontsize=20)
    ax1.tick_params(axis='both', which='both', labelsize=11)
    plt.ylim(minimum_E, min(6., maximum_E))
    plt.xlim(0., maximum_k)

    if one_array:
        plt.plot(all_kpoints, all_energies, color='black')
    else:
        for band in all_energies:
            plt.plot(all_kpoints[0], band, color='black')
            # print(all_kpoints[0][0])
            
    for sym_point in kpoint_values[1:-1]:
        plt.axvline(sym_point, alpha = 0.15, color='black', linestyle=':')
    
    for label in ax1.get_xticklabels() + ax1.get_yticklabels():
        label.set_fontweight('regular')
        label.set_fontsize(12)
        label.set_fontname('DejaVu Sans')  # Optional: pick a good bold font
        
    plt.xticks(kpoint_values, kpoint_labels)
    ax1.set_xlabel("k-points", fontsize=12, font='DejaVu Sans')  # X axis label
    ax1.set_ylabel("E(k) (eV)", fontsize=12)  # Y axis label
    plt.savefig('Band_Plot.png')
