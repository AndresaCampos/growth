import os
import tarfile
from pathlib import Path
import numpy as np
import pandas as pd


def unzip_files(base_path):
    # loops over all folder in base_path
    for folder in os.listdir(base_path):
        tfile = str(folder)
        tf = tarfile.open(tfile)
        tf.extractall()


def write_dict(base_path, inside_path, inside_path_z, folder_template):
    growth_rows = []

    z_index = np.loadtxt(base_path / inside_path_z)
    for suffix in range(4500):
        try:
            folder = folder_template.format(suffix=suffix)
            path = base_path / folder / inside_path

            row_dict = {}

            with path.open('r') as fp:
                next(fp)
                for i, line in enumerate(fp):
                    value = float(line)
                    row_dict[z_index[i]] = value

            growth_rows.append(row_dict)

        except FileNotFoundError as e:
            print('FileNotFoundError at iteration', suffix)

    growth = pd.DataFrame(growth_rows)

    return growth


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    base_path = Path('/pylon5/asz3a2p/acampos/cosmosis/cosmosis-des-library/y3-3x2pt/code/growth',
                     resolve=True, absolute=True)
    folder_template = 'chain_1x2pt_wcdm_growth_{suffix}'
    inside_path_z = 'chain_1x2pt_wcdm_growth_1050/growth_parameters/z.txt'
    growth_path = 'growth_parameters/f_z.txt'
    sigma8_path = 'growth_parameters/sigma_8_z.txt'

    #growth = write_dict(base_path, growth_path, inside_path_z, folder_template)
    sigma8 = write_dict(base_path, sigma8_path, inside_path_z, folder_template)

    np.savetxt('sigma_8_052.txt', sigma8[0.52])