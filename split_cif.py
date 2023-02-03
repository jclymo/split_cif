import argparse
import pathlib
import re
from collections import defaultdict
import os

def group_lines_by_element(lines):
    groups = defaultdict(list)
    for line in lines:
        i = re.search(r'[0-9]', line).start()
        el_symbol = line[:i]
        groups[el_symbol].append(line)
    return groups
    
def extract_section(file_path, section_heading="_atom_site_occupancy"):
    with file_path.open() as f:
        section = 0
        start_str, relevant_lines, end_str = '', [], ''
        while line := f.readline():
            if section == 1 and (line.startswith("_") or line.startswith("loop")) or line.startswith("#End"):
                # finished the relevant section on this line
                section = 2      

            if section == 0: start_str += line
            if section == 1: relevant_lines.append(line)
            if section == 2: end_str += line

            if line.startswith(section_heading):
                # start of the relevant section on next line
                section = 1

    return start_str, relevant_lines, end_str

def write_new_cif(start_str, el_lines, end_str, file_path):
    with file_path.open("w") as f_out:
        f_out.write(start_str)
        for line in el_lines:
            f_out.write(line)
        f_out.write(end_str)

def split_cif(file_path, out_folder):
    start_str, relevant_lines, end_str = extract_section(file)
    el_groups = group_lines_by_element(relevant_lines)
    for el, el_lines in el_groups.items():
        new_file_name = file_path.stem+'_'+el+'.cif'
        out_file = pathlib.Path(out_folder, new_file_name)
        write_new_cif(start_str, el_lines, end_str, out_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create single element cifs.')
    parser.add_argument('path', type=pathlib.Path)

    args = parser.parse_args()
    cif_path = args.path
    n = 0

    if cif_path.is_dir():
        i = 0
        for file in cif_path.iterdir():
            if not file.is_file(): continue
            
            if i % 500 == 0:
                n += 1
                out_folder = pathlib.Path(cif_path, f'extracted_cifs_{n}')
                if not os.path.exists(out_folder):
                    os.makedirs(out_folder)

            split_cif(file, out_folder)
            i += 1

    elif cif_path.is_file(): 
        out_folder = pathlib.Path(cif_path.parent, 'extracted_cifs')
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        file = cif_path
        split_cif(file, out_folder)
        
