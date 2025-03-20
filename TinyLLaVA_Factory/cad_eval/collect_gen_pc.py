import os
import glob
import numpy as np
import multiprocessing as mp
import argparse
import sys
from OCC.Extend.DataExchange import read_step_file
from pythonocc_operator.lib.visualize import CADsolid2pc

parser = argparse.ArgumentParser()
parser.add_argument('--src', type=str, default=None, required=True)
parser.add_argument('--output', type=str, default=None, required=True)
parser.add_argument('--n_points', type=int, default=2000)
args = parser.parse_args()

SAVE_DIR = args.output
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def write_ply_custom(points, save_path):
    """
    Save point cloud data to a PLY file.
    
    Parameters:
        points (np.ndarray): A (N, 3) array of points.
        save_path (str): The file path where the PLY file will be saved.
    """
    num_points = points.shape[0]
    
    # Define the PLY header
    header = f"""ply
format ascii 1.0
element vertex {num_points}
property float x
property float y
property float z
end_header
"""
    
    # Write the PLY file
    with open(save_path, 'w') as f:
        f.write(header)
        np.savetxt(f, points, fmt='%f %f %f')

def process_one(path):
    data_id = os.path.basename(path).split('.')[0]

    save_path = os.path.join(SAVE_DIR, data_id + ".ply")
    if os.path.exists(save_path):
        return

    try:
        shape = read_step_file(path)
    except Exception as e:
        print(f'read step failed: {path} with error: {e}')
        return 

    try:
        out_pc = CADsolid2pc(shape, args.n_points, data_id)
    except Exception as e:
        print(f"convert pc failed for {data_id} with error: {e}")
        return 
    
    # Save the point cloud data directly to a PLY file
    write_ply_custom(out_pc, save_path)

all_paths = glob.glob(os.path.join(args.src, "*.step"))
mp.Pool(8).map(process_one, all_paths)
