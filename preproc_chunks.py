"""
This script preprocess the snapshot of N-body simulation into 3D image with 6 channels,
output is in shape of (Nc,Ng,Ng,Ng), giving the normalized {displacement + velocity} field arranged by the original grid of the tracer particles
"""

import numpy as np
from bigfile import File
import argparse
import os, sys
from map2map.norms import cosmology

def pos2dis(pos, boxsize, Ng):
    """Assume `pos` is ordered in `pid` that aligns with the Lagrangian lattice,
    and all displacement must not exceed half box size.
    """
    cellsize = boxsize / Ng
    lattice = np.arange(Ng) * cellsize + 0.5 * cellsize

    pos[..., 0] -= lattice.reshape(-1, 1, 1)
    pos[..., 1] -= lattice.reshape(-1, 1)
    pos[..., 2] -= lattice

    pos -= np.rint(pos / boxsize) * boxsize

    return pos

def get_nonlin_fields(inpath, outpath):#, Nchunks):
    """
    inpath is LR simulation snapshot in bigfile format (from MP-Gadget)
    outpath is numpy array in shape (Nc,Ng/2,Ng/2,Ng/2)
    """
    bigf = File(inpath)
    header = bigf.open('Header')
    boxsize = header.attrs['BoxSize'][0]
    scale_factor = header.attrs['Time'][0]
    redshift = 1./scale_factor - 1

    Ng = header.attrs['TotNumPart'][1] ** (1/3)
    Ng = int(np.rint(Ng))

    cellsize = boxsize / Ng

    pid_ = bigf.open('1/ID')[:] - 1   # so that particle id starts from 0
    pos_ = bigf.open('1/Position')[:]
    pos = np.empty_like(pos_)
    pos[pid_] = pos_
    pos = pos.reshape(Ng, Ng, Ng, 3)

    vel_ = bigf.open('1/Velocity')[:]
    vel = np.empty_like(vel_)
    vel[pid_] = vel_
    vel = vel.reshape(Ng, Ng, Ng, 3)
    del pid_, pos_, vel_

    dis = pos2dis(pos, boxsize, Ng)
    del pos

    dis = dis.astype('f4')
    vel = vel.astype('f4')

    dis = np.moveaxis(dis,-1,0)
    vel = np.moveaxis(vel,-1,0)

    disp = cosmology.disnorm(dis,z=redshift)
    velocity = cosmology.velnorm(vel,z=redshift)
    #catnorm = np.copy(disp) ###np.concatenate([disp,velocity],axis=0)
    #Ncells_per_chunk = int(Ng/2)
    cell_index_chunk = [0,int(Ng/2),Ng]
    for i in range(2):
        for j in range(2):
            for k in range(2): 
                  disp_chunk = disp[:,cell_index_chunk[i]:cell_index_chunk[i+1],
                                      cell_index_chunk[j]:cell_index_chunk[j+1],
                                      cell_index_chunk[k]:cell_index_chunk[k+1]]
                  velocity_chunk = velocity[:,cell_index_chunk[i]:cell_index_chunk[i+1],
                                              cell_index_chunk[j]:cell_index_chunk[j+1],
                                              cell_index_chunk[k]:cell_index_chunk[k+1]]
                  chunk_tag = f"{i}{j}{k}"
                  np.save(outpath+"/disp_a%.6f_chunk%s" % (scale_factor,chunk_tag),disp_chunk)
                  np.save(outpath+"/vel_a%.6f_chunk%s" % (scale_factor,chunk_tag),velocity_chunk)
"""
	for i in range(Nchunks):
        chunk_idx = Ncells_per_chunk*i,Ncells_per_chunk*(i+1)
        disp_chunk = disp[:,chunk_idx[0]:chunk_idx[1],
			    chunk_idx[0]:chunk_idx[1],
			    chunk_idx[0]:chunk_idx[1]]
        velocity_chunk = velocity[:,chunk_idx[0]:chunk_idx[1],
				    chunk_idx[0]:chunk_idx[1],
				    chunk_idx[0]:chunk_idx[1]]
        np.save(outpath+"/disp_a%.6f_chunk%d" % (scale_factor,i),disp_chunk)
        np.save(outpath+"/vel_a%.6f_chunk%d" % (scale_factor,i),velocity_chunk)
        #np.save("disp_"+outpath,disp_chunk)
        #np.save("vel_"+outpath,velocity_chunk)
"""
    
#-------------------------------------------------------------------    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='preprocess')
    parser.add_argument('--inpath',required=True,type=str,help='path of the input snapshot')
    parser.add_argument('--outpath',required=True,type=str,help='path of the output')
    #parser.add_argument('--Nchunks',required=True,type=int,help='number of chunks to split the data files')
    
    args = parser.parse_args()
    get_nonlin_fields(args.inpath, args.outpath)
    #get_nonlin_fields(args.inpath, args.outpath, args.Nchunks)
    
    
    
    
    
    
