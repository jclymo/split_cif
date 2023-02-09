import split_cif as sc
import argparse
import pathlib

parser = argparse.ArgumentParser(description='Create single element cifs.')
parser.add_argument('path', type=pathlib.Path)
parser.add_argument('-v', '--v', action='store_true')

args = parser.parse_args()
cif_path = args.path

# check path exists and is either a cif file or directory. 
if not cif_path.exists():
    raise Exception(f'Path {cif_path} does not exist.')
if not cif_path.is_dir():
    if not cif_path.suffix == '.cif':
        raise Exception(f'Path {cif_path} must be either a cif file or directory of cif files.')

verbose = args.v
sc.main(cif_path, verbose)
