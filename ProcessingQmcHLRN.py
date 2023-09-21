import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import subprocess

import createDirectories as CreateDir
import changeToProductionStyle as changeToProd
import extractQMCResults as extract
import PlottingQMC as plot
import createMatrix as createMat





if __name__ == "__main__":
    #U = [1.5, 2.5]
    #Mu = [1.0]
    #Beta = [50.0]
    #Q = [3]
    #T = [0.25]
    #TPrime = [-0.05, 0.0375]                                                    #tPri = -0.2 t
    #TPrimePrime = [0.025]                                               #tPriPri = 0.1 t

#little testing values
    U = [1.0]
    Mu = [1.2]   
    #Mu = [-2.0, -1.8, -1.6, -1.4, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0]  
    Beta = [50.0]
    Q = [3]
    T = [0.25]
    #TPrime = [0.0, float(np.format_float_positional(-1e-10)), float(np.format_float_positional(-1e-9)), float(np.format_float_positional(-1e-8)), float(np.format_float_positional(-1e-7)), float(np.format_float_positional(-1e-6)), 
    #              float(np.format_float_positional(-1e-5)), float(np.format_float_positional(-1e-4)), -0.001, -0.01, -0.02, -0.05]  
    TPrime = [-0.05]
    TPrimePrime = [0.025]                                                 
    KSteps = [240]
    numberOfCores = 96

#True or False dependent on what to do
    createDirectories = False
    preCalculation = True
    renameHDF5 = False
    backUp = False
    Version = 0                                         #Version number which I put behind the backup hdf5 (precalc = 0)
    prepareForAndDoNextCalculation = False
    extractResults = False
    plotResults = False

    QMCCalculationDirectory = '/scratch/usr/hhpnhytt/finalQMC/QMCMaxentTestHighAccuracy/21-9-23'
    QMCDraftDirectory = '/scratch/usr/hhpnhytt/finalQMC/QMCDraft'
    #QMCHDF5BackupFolder = '/scratch/usr/hhpnhytt/finalQMC/HDF5BackupFolder'




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
                                        CreateDir.createSubmit(QMCDraftDirectory, QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri, kSteps, numberOfCores)
                                        print("submit created")
                                        createMat.writeHKFile(1, q, t, tPri, tPriPri, kSteps, QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}_kSteps{}/Hk_Hofstadter.dat'.format(u,beta,q,mu,t,tPri,tPriPri, kSteps))
                                        print("epsilon Matrix calculated")



                                    '''
                                    start the first Calculation to get starting point of nCorr
                                    '''
                                    if preCalculation:
                                        os.chdir(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}_kSteps{}'.format(u,beta,q,mu,t,tPri,tPriPri, kSteps))
                                        os.system('sbatch submit_dmft_script' )




                                    '''
                                    for that you rename the latest hdf5 file to an easy name
                                    '''
                                    if renameHDF5:
                                        os.chdir(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}_kSteps{}'.format(u,beta,q,mu,t,tPri,tPriPri,kSteps))
                                        #rename hdf5 from last calc to an easier name
                                        hdf5Name = 'U{}_mu{}_B{}_q{}_t{}_tPri{}_tPriPri{}_kSteps{}_DMFT.hdf5'.format(u,mu,beta,q,t,tPri,tPriPri,kSteps)
                                        #renaming itself
                                        try:
                                            os.system('mv U{}_mu{}_B{}_L* {}'.format(u,mu,beta, hdf5Name))
                                        except:
                                            print("no new hdf5 file")





                                    '''
                                    Here I manually backup 
                                    I backup after the calculation of Version n and after renaming the hdf5
                                    I save hdf5, parameters.in and submit with its Version into the backup Folder. 
                                    With this I can resolve all calculations
                                    '''
                                    if backUp:
                                        os.chdir(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}_kSteps{}'.format(u,beta,q,mu,t,tPri,tPriPri,kSteps))
                                        hdf5Name = 'U{}_mu{}_B{}_q{}_t{}_tPri{}_tPriPri{}_kSteps{}_DMFT.hdf5'.format(u,mu,beta,q,t,tPri,tPriPri,kSteps)
                                        #copy old/renamed hdf5 to a safe place and remove the old version then
                                        try:
                                            os.system('cp {} hdf5BackupFolder/U{}_mu{}_B{}_q{}_t{}_tPri{}_tPriPri{}_kSteps{}_DMFT_Version{}.hdf5'.format(hdf5Name, u,mu,beta,q,t,tPri,tPriPri,kSteps, Version))         
                                        except:
                                            print("no hdf5 file to backup")
                                        #move the Parameters.in which belongs to that Version into the Backup Folder
                                        try:
                                            os.system('mv Parameters.in hdf5BackupFolder/Parameters_Version{}.in'.format(Version))         
                                        except:
                                            print("no Parameters.in file to backup")
                                        #move the submit_dmft_script which belongs to that Version into the Backup Folder
                                        try:
                                            os.system('mv submit_dmft_script hdf5BackupFolder/submit_dmft_script_Version{}'.format(Version))         
                                        except:
                                            print("no hdf5 file to backup")
                                        #move the slurm which belongs to that Version into the Backup Folder
                                        try:
                                            os.system('mv slurm* hdf5BackupFolder/slurm_Version{}'.format(Version))         
                                        except:
                                            print("no hdf5 file to backup")


                                    '''
                                    prepare and do the next calculation
                                    '''
                                    if prepareForAndDoNextCalculation:
                                        hdf5Name = 'U{}_mu{}_B{}_q{}_t{}_tPri{}_tPriPri{}_kSteps{}_DMFT.hdf5'.format(u,mu,beta,q,t,tPri,tPriPri,kSteps)
                                        #write nCorr into Parameters.in so that it is ready for real calculation
                                        process = subprocess.run(['julia  /scratch/projects/hhp00048/codes/scripts/LadderDGA_utils/ncorr.jl ' + QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}_kSteps{}/{}'.format(u,beta,q,mu,t,tPri,tPriPri,kSteps, hdf5Name)]
                                                               ,capture_output = True, shell = True)
                                        nCorr = int(process.stdout.decode("utf-8"))
                                        print(nCorr)
                                        changeToProd.createSubmit(QMCDraftDirectory, QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri,kSteps)
                                        changeToProd.createParameters(u, mu, beta, q, t, tPri, tPriPri, kSteps, QMCDraftDirectory, QMCCalculationDirectory, nCorr)
                                        os.chdir(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}_kSteps{}'.format(u,beta,q,mu,t,tPri,tPriPri, kSteps))
                                        os.system('sbatch submit_dmft_script' )
                                    
                                    #TODO: BACKup Ordner in demselben directory, kein globaler









                                    '''
                                    will extract results(density and self energy) out of the hdf5 file
                                    NOTE: before it will rename the hdf5 file to a good name(and will safe it to a backup folder)
                                    '''
                                    if extractResults:
                                        #extract.extractSelfEnergy(QMCCalculationDirectory, QMCDraftDirectory, u,beta,q,mu,t,tPri,tPriPri,kSteps)
                                        extract.extractDensity(QMCCalculationDirectory, QMCDraftDirectory, u,beta,q,mu,t,tPri,tPriPri,kSteps)





                                if plotResults:
                                    #TODO: plot self energy
                                    #       plot density
                                    #for mu in Mu:
                                    #    plot.plotSigmaQMC(QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri,kSteps)
                                    plot.plotDensityQMC(QMCCalculationDirectory, u,beta,q,Mu,t,tPri,tPriPri,kSteps)







