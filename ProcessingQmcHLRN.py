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
    Mu = [4.0]
    Beta = [50.0]
    Q = [3]
    T = [0.25]
    TPrime = [-0.05]                                                   
    TPrimePrime = [0.025]

    createDirectories = True
    preCalculation = True
    prepareForAndDoNextCalculation = False
    extractResults = False
    plotResults = False

    QMCCalculationDirectory = '/scratch/usr/hhpnhytt/finalQMC/QMCFindMu'
    QMCDraftDirectory = '/scratch/usr/hhpnhytt/finalQMC/QMCDraft'
    QMCHDF5BackupFolder = '/scratch/usr/hhpnhytt/finalQMC/HDF5BackupFolder'

    for u in U:
        for mu in Mu:
            for beta in Beta:
                for q in Q:
                    for t in T:
                        for tPri in TPrime:
                            for tPriPri in TPrimePrime: 
                                '''
                                all directories and files will be generated and put into its folder
                                after this, everything is ready to start the Calculation
                                '''          
                                if createDirectories:
                                    CreateDir.createDirectories(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}'.format(u,beta,q,mu,t,tPri,tPriPri))
                                    CreateDir.createParameters(u, mu, beta, q, t, tPri, tPriPri, QMCDraftDirectory, QMCCalculationDirectory)
                                    CreateDir.createHamiltonian(q, QMCDraftDirectory, QMCCalculationDirectory, beta, u, mu,t,tPri,tPriPri)
                                    CreateDir.createSubmit(QMCDraftDirectory, QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri)
                                    CreateDir.createRun(QMCDraftDirectory, QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri)

                                    #makes that run.sh runable
                                    #switches to that directory, since cd does not work with subprocess
                                    #also need os.system to be able to use the chmod command
                                    os.chdir(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}'.format(u,beta,q,mu,t,tPri,tPriPri))                      
                                    os.system('chmod +x run.sh')
                                    os.system('./run.sh')           #now have epsilonMatrix as .dat file




                                '''
                                start the first Calculation to get starting point of nCorr
                                '''
                                if preCalculation:
                                    os.chdir(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}'.format(u,beta,q,mu,t,tPri,tPriPri))
                                    os.system('sbatch submit_dmft_script' )




                                '''
                                prepare and do the next calculation
                                for that you rename the latest hdf5 file to an easy name
                                older hdf5 will we removed but also backuped in a folder
                                '''
                                if prepareForAndDoNextCalculation:
                                    os.chdir(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}'.format(u,beta,q,mu,t,tPri,tPriPri))
                                    #rename hdf5 from last calc to an easier name
                                    #before you remove the hdf5 file from last calculation and name the hdf5 from that calc to the easier name
                                    #NOTE: never do it twice, only with new calc
                                    hdf5Name = 'U{}_mu{}_B{}_L{}_t{}_tPri{}_tPriPri{}_DMFT.hdf5'.format(QMCHDF5BackupFolder, u,mu,beta,q,t,tPri,tPriPri)
                                    try:
                                        os.system('cp {}/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}'.format(u,beta,q,mu,t,tPri,tPriPri))
                                        os.system('rm {}'.format(hdf5Name))
                                    except:
                                        print("no hdf5 file with wanted name before == preCalculation")
                                    os.system('mv *.hdf5 {}'.format(hdf5Name))
                                    #write nCorr into Parameters.in so that it is ready for real calculation
                                    nCorr = subprocess.check_output(['julia /scratch/projects/hhp00048/codes/scripts/LadderDGA_utils/ncorr.jl {}'.format(hdf5Name)])
                                    changeToProd.createSubmit(QMCDraftDirectory, QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri)
                                    changeToProd.createParameters(u, mu, beta, q, t, tPri, tPriPri, QMCDraftDirectory, QMCCalculationDirectory, nCorr)
                                    



                                if extractResults:
                                    #TODO:  still need to implement to extract selfenergy with that julia script
                                    #       extract density (with julia script)
                                    pass

                                if plotResults:
                                    #TODO: plot self energy
                                    #       plot density
                                    pass







