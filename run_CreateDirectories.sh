#!/bin/bash

#creates all directories
python3 createDirectories.py
#submits first calcs to find Ncorr
for U in 1.0 2.0 3.0
do
   for beta in 30.0 50.0 70.0 100.0
   do 
      for q in 3 4
      do
         for tPrime 0.25
            cd /home/hhpnhytt/QMC/QMC_U($U)_B($beta)_P1_L($q)_tPrime($tPrime)
            #last step is to submit it
            sbatch submit_dmft_script 
         done
      done
   done
done

