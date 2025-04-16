from energy_utils import fit_parabola, fit_check, find_mass_eff
from kpath_utils import kpath_position
import os, shutil, sys

def get_band_results(kpoints, energies, kpoint_values, kpoint_labels, con_index, val_index, ndeg_con, ndeg_val, nkpts):
    cbm_results = []
    vbm_results = []

    for i in range(ndeg_con):
        band_index = con_index+i
        extremum_kpoint_value, extremum_kpath_name, extremum_kpath_amount = kpath_position(kpoints[band_index], energies[band_index], kpoint_values, kpoint_labels)
        fit_kpoints, fit_energies, lead_coeff = fit_parabola(kpoints[band_index], energies[band_index], extremum_kpoint_value, nkpts, kpoint_labels)
        fit_check(fit_kpoints, fit_energies, kpoints[band_index], energies[band_index], kpoint_values, kpoint_labels, f"Fit Check for Con Band: {i+1}", i, ISCBM=1)
        mass_eff, mass_ratio = find_mass_eff(lead_coeff)
        results = [band_index, mass_eff, mass_ratio, lead_coeff, extremum_kpoint_value, extremum_kpath_name, extremum_kpath_amount]
        cbm_results.append(results)

    for i in range(ndeg_val):
        band_index = val_index-i
        extremum_kpoint_value, extremum_kpath_name, extremum_kpath_amount = kpath_position(kpoints[band_index], energies[band_index], kpoint_values, kpoint_labels)
        fit_kpoints, fit_energies, lead_coeff = fit_parabola(kpoints[band_index], energies[band_index], extremum_kpoint_value, nkpts, kpoint_labels)
        fit_check(fit_kpoints, fit_energies, kpoints[band_index], energies[band_index], kpoint_values, kpoint_labels, f"Fit Check for Val Band: {i+1}", i, ISCBM=0)
        mass_eff, mass_ratio = find_mass_eff(lead_coeff)
        results = [band_index, mass_eff, mass_ratio, lead_coeff, extremum_kpoint_value, extremum_kpath_name, extremum_kpath_amount]
        vbm_results.append(results)

    return cbm_results, vbm_results

class BandResults:
    def __init__(self, band_index, mass_eff, mass_ratio, lead_coeff, extremum_kpoint_value, extremum_kpath_name, extremum_kpath_amount):
        self.band_index = band_index
        self.mass_eff = mass_eff
        self.mass_ratio = mass_ratio
        self.lead_coeff = lead_coeff
        self.extremum_kpoint_value = extremum_kpoint_value
        self.extremum_kpath_name = extremum_kpath_name
        self.extremum_kpath_amount = extremum_kpath_amount

def build_band_extrema_list(data_list):
    """
    Converts raw ordered band extrema data into BandExtrema objects.
    Assumes each row is [energy, k_point (tuple), band_index, effective_mass].
    """
    return [BandResults(
                band_index = row[0], 
                mass_eff = row[1], 
                mass_ratio = row[2], 
                lead_coeff = row[3], 
                extremum_kpoint_value = row[4], 
                extremum_kpath_name = row[5], 
                extremum_kpath_amount = row[6],
                ) for row in data_list]

class TotalResults:
    def __init__(self, nkpts=None, nbands=None, band_gap=None, ndeg_con=None,
                 ndeg_val=None, cbm_list=None, vbm_list=None):
        self.nkpts = nkpts
        self.nbands = nbands
        self.band_gap = band_gap
        self.ndeg_con = ndeg_con
        self.ndeg_val = ndeg_val
        self.cbm_list = cbm_list  # list of BandExtrema
        self.vbm_list = vbm_list

def build_total_results(nkpts, nbands, band_gap, ndeg_con, ndeg_val, cbm_values, val_values):
    return TotalResults(
        nkpts = nkpts,
        nbands = nbands,
        band_gap = band_gap,
        ndeg_con = ndeg_con,
        ndeg_val = ndeg_val,
        cbm_list = cbm_values,
        vbm_list = val_values
    )

def create_output_folder():

    output_filenames = ["MY_REPORT.txt", "Band_Plot.png", "Fit_Check*"]
    output_dir = "./Output_Files/"

    dir_exists = os.path.exists(output_dir)
    if not dir_exists:
        print(f"Creating output directory '{output_dir}'...")
        os.makedirs(output_dir)
        if not os.path.exists(output_dir):
            raise FileNotFoundError(f"Could not create output directory {output_dir}")
    elif dir_exists:
        overwrite_prompt = True
        while overwrite_prompt:
            overwrite = input(f"Directory '{output_dir}' already exists. Overwrite the files in '{output_dir}'? [y/n]")
            if overwrite == 'y':
                print(f"We will overwrite the files in {output_dir}")
                overwrite_prompt = False
            elif overwrite == 'n':
                print("We will not overwrite files. Exiting the program ...")
                sys.exit()
            else:
                print("Please type either a 'y' or an 'n' (without single quotes)")

    for name in output_filenames:
        file_exists = os.path.exists(name)
        if file_exists:
            if os.path.exists(output_dir+name):
                os.remove(output_dir+name)
            shutil.move(name, output_dir)
        else:
            print(os.listdir())
            raise FileNotFoundError(f"The file '{name}' was not created and so cannot be moved :(")

def write_summary_to_file(results, output_path):
    with open(output_path, 'w') as f:
        f.write(f"Band Gap: {results.band_gap:.7f} eV\n\n")

        f.write("Conduction Band Minima (CBMs):\n")
        for i, cbm in enumerate(results.cbm_list):
            f.write(f"CBM #{i+1}:\n"
                    f"   Band Index = {cbm.band_index}\n"
                    f"   Effective Mass = {cbm.mass_eff:.7e} kg = {cbm.mass_ratio:.7f} m_e\n"
                    f"   Leading Coefficient (in parabola equation) = {cbm.lead_coeff}\n"
                    f"   k-point Value at CBM = {cbm.extremum_kpoint_value}\n"
                    f"   CBM Location = {cbm.extremum_kpath_amount} on path {cbm.extremum_kpath_name[0]}->{cbm.extremum_kpath_name[1]}\n\n"
                    )


        f.write("Valence Band Minima (VBMs):\n")
        for i, vbm in enumerate(results.vbm_list):
            f.write(f"vBM #{i+1}:\n"
                    f"   Band Index = {vbm.band_index}\n"
                    f"   Effective Mass = {vbm.mass_eff:.7e} kg = {vbm.mass_ratio:.7f} m_e\n"
                    f"   Leading Coefficient (in parabola equation) = {vbm.lead_coeff}\n"
                    f"   k-point Value at VBM = {vbm.extremum_kpoint_value}\n"
                    f"   VBM Location = {vbm.extremum_kpath_amount} on path {vbm.extremum_kpath_name[0]}->{vbm.extremum_kpath_name[1]}\n\n"
                    )


