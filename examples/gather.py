#/usr/bin/env python3

import mpi4py.MPI as MPI
import numpy

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
sz = comm.Get_size()

myvals = numpy.empty(2)

# sest up an array of values 0...2*sz
if(rank == 0):
  values = numpy.arange(2.*sz)
  comm.Scatter(values, myvals, root=0)
else:
  comm.Scatter(None, myvals, root=0)

# have each rank square its data
myvals = myvals**2

# gather results back to root rank
if(rank == 0):
  values = numpy.empty(2*sz)
  comm.Gather(myvals, values, root=0)
  print("Got squares: "+str(values))
else:
  comm.Gather(myvals, None, root=0)
