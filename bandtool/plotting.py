import matplotlib.pyplot as plt

def plot_limits(kpoints, energies, CUT, ISCBM, one_array, i):
    width = 12
    maximum_E = 0.
    maximum_k = 0.
    minimum_E = 0.
    minimum_k = 0.
    if one_array:
        if CUT == 'NO':
            maximum_k = max(kpoints)
            maximum_E = max(energies)
            minimum_E = min(energies)/ 2. - 0.2
        else:
            width = 3
            maximum_k = max(kpoints[:CUT])
            if i == 1:
                minimum_k = min(kpoints[CUT:])
                maximum_k = max(kpoints)
            maximum_E = 6.
            minimum_E = -6.
        if not ISCBM:
            maximum_E += 0.3
    else:
        if CUT == 'NO':
            maximum_k = max([max(kline) for kline in kpoints])
            maximum_E = max([max(band) for band in energies]) - 0.2
            minimum_E = min([min(band) for band in energies]) / 2. - 0.2
        else:
            width = 3
            maximum_k = max([max(kline[:CUT]) for kline in kpoints])
            if i == 1:
                minimum_k = min(kpoints[0][CUT:])
                maximum_k = max([max(kline) for kline in kpoints])
            maximum_E = 6.
            minimum_E = -6.
    
    return maximum_k, minimum_k, maximum_E, minimum_E, width


def plot_bands(all_kpoints, all_energies, kpoint_values, kpoint_labels, nkpts, CUT_SET, ISCBM):
    if len(CUT_SET) == 0 or CUT_SET == 'NO':
        CUT = 'NO'
    else:
        CUT = CUT_SET[0].extremum_k_index

    one_array = 0
    width = 12

    for i in range(0, 2):
        if len(all_energies) == nkpts:
            one_array = 1
            maximum_k, minimum_k, maximum_E, minimum_E, width = plot_limits(all_kpoints, all_energies, CUT, ISCBM, one_array, i)
        else:
            maximum_k, minimum_k, maximum_E, minimum_E, width = plot_limits(all_kpoints, all_energies, CUT, ISCBM, one_array, i)
            
        maximum_E = min(maximum_E, 5.1)
        minimum_E = max(minimum_E, -5.1)
        fig1, ax1 = plt.subplots(figsize=(width, 8))
        plt.title("Band Structure", fontsize=20)
        ax1.tick_params(axis='both', which='both', labelsize=11)
        plt.ylim(minimum_E, maximum_E)
        plt.xlim(minimum_k, maximum_k)

        if one_array:
            plt.plot(all_kpoints, all_energies, color='black')
        else:
            for band in all_energies:
                plt.plot(all_kpoints[0], band, color='black')
                # print(all_kpoints[0][0])
        
        skip = 0
        for sym_point in kpoint_values[1:-1]:
            if sym_point > maximum_k or sym_point < minimum_k:
                skip = 1
                break
            plt.axvline(sym_point, alpha = 0.15, color='black', linestyle=':')
        
        if not skip:
            for label in ax1.get_xticklabels() + ax1.get_yticklabels():
                label.set_fontweight('regular')
                label.set_fontsize(12)
                label.set_fontname('DejaVu Sans')  # Optional: pick a good bold font
                
            plt.xticks(kpoint_values, kpoint_labels)
            
    
        ax1.set_xlabel("k-points", fontsize=12, font='DejaVu Sans')  # X axis label
        ax1.set_ylabel("E(k) (eV)", fontsize=12)  # Y axis label

        if CUT == 'NO':
            plt.savefig('Band_Plot.png')
            break
        elif ISCBM:
            plt.savefig(f"Band_Plot_CUT_CBM{i}.png")
        else:
            plt.savefig(f"Band_Plot_CUT_VBM{i}.png")



