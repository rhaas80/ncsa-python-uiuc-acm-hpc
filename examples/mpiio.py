#!/usr/bin/env python3

import mpi4py.MPI as MPI
import h5py
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
sz = comm.Get_size()

fh = h5py.File('data.h5', 'w', driver='mpio', comm=comm)

dset = fh.create_dataset('alldata', shape=(sz+1, 3), dtype=float)

if rank == sz-1: # last rank
  dset[rank:rank+2] = 10.*rank + np.arange(0.,6.).reshape((2,3))
else:
  dset[rank] = 10.*rank + np.arange(0.,3.).reshape((1,3))

fh.close()

# show output
if rank == 0:
  with h5py.File('data.h5', 'r') as fh:
    print("alldata:\n", fh["alldata"][:])
