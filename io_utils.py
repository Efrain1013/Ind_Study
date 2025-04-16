import numpy as np


def read_nbands(filename):
    """
    Reads NBANDS from the BAND.dat file.
    """
    # print("We're in function")
    with open(filename, 'r') as f:
        for line in f:
            # print(line)
            if 'NBANDS' in line:
                parts = line.strip().split()
                nbands = int(parts[-1])
                # print(nbands)
                return nbands

    raise ValueError("Could not find NBANDS in file.")

def read_nkpts(filename):
    """
    Reads NKPTS from the BAND.dat file.
    """
    with open(filename, 'r') as f:
        for line in f:
            # print(line)
            if 'NKPTS' in line:
                parts = line.strip().split()
                # print(parts)
                nkpts = int(parts[-2])
                return nkpts

    raise ValueError("Could not find NKPTS in file.")


def find_ken_values(filename):
    """
    Reads BAND.dat file and extracts k-points and band energies.

    Parameters:
    filename (str): Path to BAND.dat

    Returns:
    tuple: (all_kpoints, all_energies, NKPTS, NBANDS)
    """

    with open(filename, "r") as file:
        data = np.loadtxt(file)

    NKPTS = read_nkpts(filename)
    NBANDS = read_nbands(filename)
    # print(f"NKPTS: {NKPTS} | NBANDS: {NBANDS}")
    all_kpoints = [float(value) for value in data[:, 0]]
    all_energies = [float(value) for value in data[:, 1]]

    return all_kpoints, all_energies, NKPTS, NBANDS

# Functino to split our kpoints and Energies
def split_kE(all_kpoints, all_energies, nkpts, nbands):
    k_values = []
    E_values = []

    for i in range(nbands):
        Es = all_energies[(i*nkpts):((i+1)*nkpts)]
        ks = all_kpoints[(i*nkpts):((i+1)*nkpts)]

        E_values.append(Es)
        k_values.append(ks)
        if k_values[i][0] != 0:
            k_values[i].reverse()
            E_values[i].reverse()

    return np.array(k_values), np.array(E_values)

# Function to get the labels of our symmetry points and their values
def get_kpoint_labels(filename):
    kpoint_value = []
    kpoint_name = []

    with open(filename, 'r') as file:
        for line in file:
            stripped = line.strip()
            # Skip empty lines or tips/comments
            if not stripped or stripped.startswith("*") or "Tip" in stripped:
                break

            # Skip header line
            if "Coordinate" in stripped:
                continue

            parts = stripped.split()
            if len(parts) < 2:
                continue

            label = parts[0]
            value_str = parts[-1]

            # Standardize the label
            if label.lower() == 'gamma':
                label = 'Γ'
            elif label[0] in ['m', 'n']:
                label = '-' + label[1:]

            try:
                value = float(value_str)
                kpoint_value.append(value)
                kpoint_name.append(label)
            except ValueError:
                continue  # skip if value isn't a float

    return kpoint_value, kpoint_name