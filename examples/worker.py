#!/usr/bin/env python3

import mpi4py.MPI as MPI
import numpy as np

rank = MPI.COMM_WORLD.Get_rank()
sz = MPI.COMM_WORLD.Get_size()

# fix seed so that the same numbers are used each time
np.random.seed(17)

def manager():
  numberstosend = np.random.rand(sz-1)
  for i in range(1,sz):
    MPI.COMM_WORLD.Send(numberstosend[i-1], i)

  result = np.zeros(shape=(1), dtype=float)
  for i in range(1,sz):
    numbertoreceive = np.empty(shape=(1),dtype=float)
    status = MPI.Status()
    MPI.COMM_WORLD.Recv(numbertoreceive, status=status)
    print ("Received %f from PE %d" % (numbertoreceive[0], status.Get_source()))
    result = result + numbertoreceive
  print ("Total is %f" % result[0])

def worker():
  numbertoreceive = np.empty(shape=(1),dtype=float)
  MPI.COMM_WORLD.Recv(numbertoreceive, 0)

  result = numbertoreceive * rank

  print ("PE %d received %f and computed %f" % (rank, numbertoreceive[0], result[0]))

  MPI.COMM_WORLD.Send(result, 0)

if (rank == 0):
  manager()
else:
  worker()
