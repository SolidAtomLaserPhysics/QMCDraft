import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import subprocess

import createDirectories as CreateDir
import changeToProductionStyle as changeToProd






if __name__ == "__main__":
    #U = [1.5, 2.5]
    #Mu = [1.0]
    #Beta = [50.0]
    #Q = [3]
    #T = [0.25]
    #TPrime = [-0.05, 0.0375]                                                    #tPri = -0.2 t
    #TPrimePrime = [0.025]                                               #tPriPri = 0.1 t

#little testing values
    U = [1.5]
    Mu = [1.0]
    Beta = [50.0]
    Q = [3]
    T = [0.25]
    TPrime = [-0.05]                                                   
    TPrimePrime = [0.025]

    createDirectories = True
    preCalculation = True
    prepareForCalculation = False

    QMCCalculationDirectory = '/scratch/usr/hhpnhytt/finalQMCResults'
    QMCDraftDirectory = '/scratch/usr/hhpnhytt/finalQMCResults/QMCDraft'

    for u in U:
        for mu in Mu:
            for beta in Beta:
                for q in Q:
                    for t in T:
                        for tPri in TPrime:
                            for tPriPri in TPrimePrime:           
                                if createDirectories:
                                    CreateDir.createDirectories(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}'.format(u,beta,q,mu,t,tPri,tPriPri))
                                    CreateDir.createParameters(u, mu, beta, q, t, tPri, tPriPri, QMCDraftDirectory, QMCCalculationDirectory)
                                    CreateDir.createHamiltonian(q, QMCDraftDirectory, QMCCalculationDirectory, beta, u, mu,t,tPri,tPriPri)
                                    CreateDir.createSubmit(QMCDraftDirectory, QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri)
                                    CreateDir.createRun(QMCDraftDirectory, QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri)
                                    #CreateDir.createProduction(QMCDraftDirectory, QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri)


                                    #makes that run.sh runable
                                    #switches to that directory, since cd does not work with subprocess
                                    #also need os.system to be able to use the chmod command
                                    os.chdir(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}'.format(u,beta,q,mu,t,tPri,tPriPri))                      
                                    os.system('chmod +x run.sh')
                                    os.system('./run.sh')           #now have epsilonMatrix as .dat file


                                if preCalculation:
                                    os.chdir(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}'.format(u,beta,q,mu,t,tPri,tPriPri))
                                    os.system('sbatch submit_dmft_script' )


                                if prepareForCalculation:
                                    #have to find the correct slurm file name for each folder
                                    slurmName = 'a'
                                    #get Ncorr
                                    os.chdir(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}'.format(u,beta,q,mu,t,tPri,tPriPri))
                                    x = subprocess.check_output(['julia /scratch/projects/hhp00048/codes/scripts/LadderDGA_utils/ncorr.jl {}'.format(slurmName)])
                                    os.system('julia /scratch/projects/hhp00048/codes/scripts/LadderDGA_utils/ncorr.jl U2.0_mu1.0_beta30.0_DMFT-2023-03-15-Wed-14-41-21.hdf5')








