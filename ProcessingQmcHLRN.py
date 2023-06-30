import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import subprocess

import createDirectories as CreateDir
import changeToProductionStyle as changeToProd
import extractQMCResults as extract
import PlottingQMC as plot






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
    #Mu = [-2.0, -1.8, -1.6, -1.4, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0]
    Mu = [-1.5, 0.5, 1.5, 2.5]
    Beta = [50.0]
    Q = [3]
    T = [0.25]
    TPrime = [-0.05]                                                   
    TPrimePrime = [0.025]
    KSteps = [100, 200, 300, 400, 500]

    createDirectories = True
    preCalculation = True
    prepareForAndDoNextCalculation = False
    extractResults = False
    plotResults = False

    QMCCalculationDirectory = '/scratch/usr/hhpnhytt/finalQMC/QMCFindMu'
    QMCDraftDirectory = '/scratch/usr/hhpnhytt/finalQMC/QMCDraft'
    QMCHDF5BackupFolder = '/scratch/usr/hhpnhytt/finalQMC/HDF5BackupFolder'

    for u in U:
        for beta in Beta:
            for q in Q:
                for t in T:
                    for tPri in TPrime:
                        for tPriPri in TPrimePrime: 
                            for kSteps in KSteps:
                                for mu in Mu:
                                    '''
                                    all directories and files will be generated and put into its folder
                                    after this, everything is ready to start the Calculation
                                    '''          
                                    if createDirectories:
                                        CreateDir.createDirectories(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}_kSteps{}'.format(u,beta,q,mu,t,tPri,tPriPri, kSteps))
                                        print("dir created")
                                        CreateDir.createParameters(u, mu, beta, q, t, tPri, tPriPri, kSteps, QMCDraftDirectory, QMCCalculationDirectory)
                                        print("parameters.in created")
                                        CreateDir.createHamiltonian(q, QMCDraftDirectory, QMCCalculationDirectory, beta, u, mu,t,tPri,tPriPri, kSteps)
                                        print("epsilon Matrix created")
                                        CreateDir.createSubmit(QMCDraftDirectory, QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri, kSteps)
                                        print("submit created")
                                        CreateDir.createRun(QMCDraftDirectory, QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri, kSteps)
                                        print("run.sh created")

                                        #makes that run.sh runable
                                        #switches to that directory, since cd does not work with subprocess
                                        #also need os.system to be able to use the chmod command
                                        os.chdir(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}_kSteps{}'.format(u,beta,q,mu,t,tPri,tPriPri, kSteps))                      
                                        os.system('chmod +x run.sh')
                                        os.system('./run.sh')           #now have epsilonMatrix as .dat file

                                        print("epsilon Matrix calculated")




                                    '''
                                    start the first Calculation to get starting point of nCorr
                                    '''
                                    if preCalculation:
                                        os.chdir(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}_kSteps{}'.format(u,beta,q,mu,t,tPri,tPriPri, kSteps))
                                        os.system('sbatch submit_dmft_script' )


                                    #TODO: path to get nCorr seems incorrect?



                                    #TODO: kSteps in paths below einbinden


                                    '''
                                    prepare and do the next calculation
                                    for that you rename the latest hdf5 file to an easy name
                                    older hdf5 will we removed but also backuped in a folder
                                    '''
                                    if prepareForAndDoNextCalculation:
                                        os.chdir(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}_kSteps{}'.format(u,beta,q,mu,t,tPri,tPriPri, kSteps))
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
                                    #TODO:  extract density (with julia script)
                                    #       
                                    extract.extractSelfEnergy(QMCCalculationDirectory, QMCDraftDirectory, u,beta,q,mu,t,tPri,tPriPri)
                                    extract.extractDensity(QMCCalculationDirectory, QMCDraftDirectory, u,beta,q,mu,t,tPri,tPriPri)


                            if plotResults:
                                #TODO: plot self energy
                                #       plot density
                                for mu in Mu:
                                    plot.plotSigmaQMC(QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri)
                                plot.plotDensityQMC(QMCCalculationDirectory, u,beta,q,Mu,t,tPri,tPriPri)







