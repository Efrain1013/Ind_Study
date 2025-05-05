from bandtool.io_utils import find_ken_values, split_kE, get_kpoint_labels
from bandtool.energy_utils import norm_energies
from bandtool.plotting import plot_bands
from bandtool.output_utils import build_band_extrema_list, build_total_results, write_summary_to_file, create_output_folder, get_band_results

def main():
    print("Running main script...")
    all_kpoints, all_energies, NKPTS, NBANDS = find_ken_values("BAND.dat")
    all_kpoints_norm, all_energies_split = split_kE(all_kpoints, all_energies, NKPTS, NBANDS)
    kpoint_values, kpoint_labels = get_kpoint_labels("KLABELS")
    all_energies_norm, val_index, NDEG_VAL, con_index, NDEG_CON, BAND_GAP = norm_energies(all_energies_split)
    plot_bands(all_kpoints_norm, all_energies_norm, kpoint_values, kpoint_labels, NKPTS, CUT_SET = 'NO', ISCBM=1)
    cbm_results, vbm_results = get_band_results(all_kpoints_norm, all_energies_norm, kpoint_values, kpoint_labels, con_index, val_index, NDEG_CON+1, NDEG_VAL+1, NKPTS)
    all_cbms = build_band_extrema_list(cbm_results)
    all_vbms = build_band_extrema_list(vbm_results)
    plot_bands(all_kpoints_norm, all_energies_norm, kpoint_values, kpoint_labels, NKPTS, CUT_SET=all_cbms, ISCBM=1)
    plot_bands(all_kpoints_norm, all_energies_norm, kpoint_values, kpoint_labels, NKPTS, CUT_SET=all_vbms, ISCBM=0)
    total_results = build_total_results(NKPTS, NBANDS, BAND_GAP, NDEG_CON, NDEG_VAL, all_cbms, all_vbms)
    write_summary_to_file(total_results, "MY_REPORT.txt")
    create_output_folder()

if __name__ == "__main__":
    main()
