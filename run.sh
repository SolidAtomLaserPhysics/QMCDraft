#!/bin/bash



mpif90 hofstadter_hamiltonian.f90 -o hofstadter_hamiltonian.x -g -ffixed-line-length-0
mpirun --oversubscribe ./hofstadter_hamiltonian.x
