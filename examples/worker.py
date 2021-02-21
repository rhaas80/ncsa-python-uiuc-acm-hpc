#!/usr/bin/env python3

import mpi4py.MPI as MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
sz = comm.Get_size()

# fix seed so that the same numbers are used each time
np.random.seed(17)

def manager():
  numberstosend = np.random.rand(sz-1)
  for i in range(1,sz):
    comm.Send(numberstosend[i-1], i)

  result = np.array([0.])
  for i in range(1,sz):
    numbertoreceive = np.empty_like(result)
    status = MPI.Status()
    comm.Recv(numbertoreceive, status=status)
    print ("Received %f from PE %d" % (numbertoreceive[0], status.Get_source()))
    result = result + numbertoreceive
  print ("Total is %f" % result[0])

def worker():
  numbertoreceive = np.empty(shape=(1),dtype=float)
  comm.Recv(numbertoreceive, 0)

  result = numbertoreceive * rank

  print ("PE %d received %f and computed %f" % (rank, numbertoreceive[0], result[0]))

  comm.Send(result, 0)

if (rank == 0):
  manager()
else:
  worker()
