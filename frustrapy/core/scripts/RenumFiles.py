import sys
import os

def renum_files(job_id, job_dir, mode):
    # Read equivalences from file
    equivalence_file_path = os.path.join(job_dir, f"{job_id}.pdb_equivalences.txt")
    with open(equivalence_file_path, "r") as file:
        equivalences = file.readlines()
    equivalences = [line.strip() for line in equivalences]

    # Use a list of tuples to store equivalences
    equiv_list = []

    # Process equivalences
    for line in equivalences:
        splitted = line.split()
        equiv_list.append(
            (splitted[1], splitted[0], splitted[2])
        )  # (chain_number, chain_letter, equiv_res)

    # Read tertiary frustration data
    tertiary_frustration_path = os.path.join(job_dir, "tertiary_frustration.dat")
    with open(tertiary_frustration_path, "r") as file:
        tertiary_frustration = file.readlines()

    # Open output files
    frust_file_path = os.path.join(job_dir, f"{job_id}.pdb_{mode}")
    frust_aux_file_path = os.path.join(job_dir, f"{job_id}_{mode}.pdb_auxiliar")
    frust_renum_file_path = os.path.join(job_dir, f"{job_id}_{mode}_renumbered")

    def find_equiv(chain_number):
        """Find and return the chain letter and equiv_res for a given chain number."""
        for item in equiv_list:
            if item[0] == chain_number:
                return item[1], item[2]  # Return chain_letter and equiv_res
        return None, None  # Return None if not found

    with open(frust_file_path, "w") as frust, open(
        frust_aux_file_path, "w"
    ) as frust_aux, open(frust_renum_file_path, "w") as frust_renum:
        if mode in ["configurational", "mutational"]:
            frust.write(
                "Res1 Res2 ChainRes1 ChainRes2 DensityRes1 DensityRes2 AA1 AA2 NativeEnergy DecoyEnergy SDEnergy FrstIndex Welltype FrstState\n"
            )

            for line in tertiary_frustration[2:]:
                splitted = line.split()
                res1, res2 = splitted[0], splitted[1]
                density1, density2 = splitted[11], splitted[12]
                aa1, aa2 = splitted[13], splitted[14]
                native_energy, decoy_energy, sd_energy = (
                    splitted[15],
                    splitted[16],
                    splitted[17],
                )
                frst_index = splitted[18]
                res_res_distance = ""
                frst_type = ""
                frst_type_aux = ""

                # Assign well-type
                if float(splitted[10]) < 6.5:
                    res_res_distance = "short"
                elif float(splitted[10]) >= 6.5:
                    if float(density1) < 2.6 and float(density2) < 2.6:
                        res_res_distance = "water-mediated"
                    else:
                        res_res_distance = "long"

                if float(frst_index) <= -1:
                    frst_type = "highly"
                    frst_type_aux = "red"
                elif -1 < float(frst_index) < 0.78:
                    frst_type = "neutral"
                    frst_type_aux = "gray"
                elif float(frst_index) >= 0.78:
                    frst_type = "minimally"
                    frst_type_aux = "green"

                chain_letter_res1, equiv_res1 = find_equiv(res1)
                chain_letter_res2, equiv_res2 = find_equiv(res2)

                frust.write(
                    f"{equiv_res1} {equiv_res2} {chain_letter_res1} {chain_letter_res2} {density1} {density2} {aa1} {aa2} {native_energy} {decoy_energy} {sd_energy} {frst_index} {res_res_distance} {frst_type}\n"
                )
                frust_renum.write(
                    f"{res1} {res2} {chain_letter_res1} {chain_letter_res2} {density1} {density2} {aa1} {aa2} {native_energy} {decoy_energy} {sd_energy} {frst_index} {res_res_distance} {frst_type}\n"
                )

                if frst_type_aux in ["green", "red"]:
                    frust_aux.write(
                        f"{equiv_res1} {equiv_res2} {chain_letter_res1} {chain_letter_res2} {res_res_distance} {frst_type_aux}\n"
                    )

        elif mode == "singleresidue":
            frust.write(
                "Res ChainRes DensityRes AA NativeEnergy DecoyEnergy SDEnergy FrstIndex\n"
            )

            for line in tertiary_frustration[2:]:
                splitted = line.split()
                res = splitted[0]
                density = splitted[5]
                aa = splitted[6]
                native_energy, decoy_energy, sd_energy = (
                    splitted[7],
                    splitted[8],
                    splitted[9],
                )
                frst_index = splitted[10]

                chain_letter, equiv_res = find_equiv(res)

                frust.write(
                    f"{equiv_res} {chain_letter} {density} {aa} {native_energy} {decoy_energy} {sd_energy} {frst_index}\n"
                )

    # Remove the renumbered file
    os.remove(frust_renum_file_path)

# Gather command line arguments
job_id = sys.argv[1]
job_dir = sys.argv[2]
mode = sys.argv[3]

# Read equivalences from file
equivalence_file_path = os.path.join(job_dir, f"{job_id}.pdb_equivalences.txt")
with open(equivalence_file_path, "r") as file:
    equivalences = file.readlines()
equivalences = [line.strip() for line in equivalences]

# Use a list of tuples to store equivalences
equiv_list = []

# Process equivalences
for line in equivalences:
    splitted = line.split()
    equiv_list.append(
        (splitted[1], splitted[0], splitted[2])
    )  # (chain_number, chain_letter, equiv_res)

# Read tertiary frustration data
tertiary_frustration_path = os.path.join(job_dir, "tertiary_frustration.dat")
with open(tertiary_frustration_path, "r") as file:
    tertiary_frustration = file.readlines()

# Open output files
frust_file_path = os.path.join(job_dir, f"{job_id}.pdb_{mode}")
frust_aux_file_path = os.path.join(job_dir, f"{job_id}_{mode}.pdb_auxiliar")
frust_renum_file_path = os.path.join(job_dir, f"{job_id}_{mode}_renumbered")


def find_equiv(chain_number):
    """Find and return the chain letter and equiv_res for a given chain number."""
    for item in equiv_list:
        if item[0] == chain_number:
            return item[1], item[2]  # Return chain_letter and equiv_res
    return None, None  # Return None if not found


with open(frust_file_path, "w") as frust, open(
    frust_aux_file_path, "w"
) as frust_aux, open(frust_renum_file_path, "w") as frust_renum:
    if mode in ["configurational", "mutational"]:
        frust.write(
            "Res1 Res2 ChainRes1 ChainRes2 DensityRes1 DensityRes2 AA1 AA2 NativeEnergy DecoyEnergy SDEnergy FrstIndex Welltype FrstState\n"
        )

        for line in tertiary_frustration[2:]:
            splitted = line.split()
            res1, res2 = splitted[0], splitted[1]
            density1, density2 = splitted[11], splitted[12]
            aa1, aa2 = splitted[13], splitted[14]
            native_energy, decoy_energy, sd_energy = (
                splitted[15],
                splitted[16],
                splitted[17],
            )
            frst_index = splitted[18]
            res_res_distance = ""
            frst_type = ""
            frst_type_aux = ""

            # Assign well-type
            if float(splitted[10]) < 6.5:
                res_res_distance = "short"
            elif float(splitted[10]) >= 6.5:
                if float(density1) < 2.6 and float(density2) < 2.6:
                    res_res_distance = "water-mediated"
                else:
                    res_res_distance = "long"

            if float(frst_index) <= -1:
                frst_type = "highly"
                frst_type_aux = "red"
            elif -1 < float(frst_index) < 0.78:
                frst_type = "neutral"
                frst_type_aux = "gray"
            elif float(frst_index) >= 0.78:
                frst_type = "minimally"
                frst_type_aux = "green"

            chain_letter_res1, equiv_res1 = find_equiv(res1)
            chain_letter_res2, equiv_res2 = find_equiv(res2)

            frust.write(
                f"{equiv_res1} {equiv_res2} {chain_letter_res1} {chain_letter_res2} {density1} {density2} {aa1} {aa2} {native_energy} {decoy_energy} {sd_energy} {frst_index} {res_res_distance} {frst_type}\n"
            )
            frust_renum.write(
                f"{res1} {res2} {chain_letter_res1} {chain_letter_res2} {density1} {density2} {aa1} {aa2} {native_energy} {decoy_energy} {sd_energy} {frst_index} {res_res_distance} {frst_type}\n"
            )

            if frst_type_aux in ["green", "red"]:
                frust_aux.write(
                    f"{equiv_res1} {equiv_res2} {chain_letter_res1} {chain_letter_res2} {res_res_distance} {frst_type_aux}\n"
                )

    elif mode == "singleresidue":
        frust.write(
            "Res ChainRes DensityRes AA NativeEnergy DecoyEnergy SDEnergy FrstIndex\n"
        )

        for line in tertiary_frustration[2:]:
            splitted = line.split()
            res = splitted[0]
            density = splitted[5]
            aa = splitted[6]
            native_energy, decoy_energy, sd_energy = (
                splitted[7],
                splitted[8],
                splitted[9],
            )
            frst_index = splitted[10]

            chain_letter, equiv_res = find_equiv(res)

            frust.write(
                f"{equiv_res} {chain_letter} {density} {aa} {native_energy} {decoy_energy} {sd_energy} {frst_index}\n"
            )

# Remove the renumbered file
os.remove(frust_renum_file_path)
