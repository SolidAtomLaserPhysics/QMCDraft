import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


'''
changes the submit script to 5 Nodes for the calculation
'''
def createDirectories(path):
    if not os.path.exists(path):                                  #make directory if not exists already
        os.mkdir(path)


def createParameters(u, mu, beta, q, t, tPri, tPriPri, QMCDraftDirectory, QMCCalculationDirectory):
    if q == 3:
        with open(QMCDraftDirectory + '/Parameters_Q3.in', 'r', encoding='utf-8') as file:
            data = file.readlines()
    
            data[2] = "NAt             = 3 #q des Magnetfeldes p/q      \n"
            data[5] = "beta            = {} #-> In Einheiten 1/t.     \n".format(beta)  
            data[7] = "mu              = {}         \n".format(mu) 
            data[10] = "#fileold         = U{}_mu{}_B{}_L{}_t{}_tPri{}_tPriPri{}_DMFT.hdf5 #-> Hier wird jede Iteration gespeichert. Von dort kann ich weiterrechnen.      \n".format(u, mu, beta, q, t, tPri, tPriPri)
            data[11] = "DMFTsteps       = 3 #-> Anzahl der DMFT loops     \n"
            data[14] = "FileNamePrefix  = U{}_mu{}_B{}_L{}_t{}_tPri{}_tPriPri{}_DMFT   \n".format(u, mu, beta, q, t, tPri, tPriPri)
            data[23] = "Udd             = {} #-> Hubbard U     \n".format(u)
            data[27] = "Udd             = {} #-> Hubbard U     \n".format(u)
            data[31] = "Udd             = {} #-> Hubbard U     \n".format(u)
            data[37] = "Nmeas           = 1e5   \n"
            data[38] = "NCorr           = 20 #-> Wie viele Schritte zwischen zwei Messungen. \n"
    with open(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}/Parameters_Q3.in'.format(u,beta,q,mu,t,tPri,tPriPri), 'w', encoding='utf-8') as file:
        file.writelines(data)
    
    if q == 4:
        with open(QMCDraftDirectory + '/Parameters_Q4.in', 'r', encoding='utf-8') as file:
            data = file.readlines()
    
            data[2] = "NAt             = 4 #q des Magnetfeldes p/q      \n"
            data[5] = "beta            = {} #-> In Einheiten 1/t.     \n".format(beta)  
            data[7] = "mu              = {}         \n".format(mu) 
            data[10] = "#fileold         = U{}_mu{}_B{}_L{}_t{}_tPri{}_tPriPri{}_DMFT.hdf5 #-> Hier wird jede Iteration gespeichert. Von dort kann ich weiterrechnen.      \n".format(u, mu, beta, q, t, tPri, tPriPri)
            data[11] = "DMFTsteps       = 3 #-> Anzahl der DMFT loops     \n"
            data[14] = "FileNamePrefix  = U{}_mu{}_B{}_L{}_t{}_tPri{}_tPriPri{}_DMFT   \n".format(u, mu, beta, q, t, tPri, tPriPri)
            data[23] = "Udd             = {} #-> Hubbard U     \n".format(u)
            data[27] = "Udd             = {} #-> Hubbard U     \n".format(u)
            data[31] = "Udd             = {} #-> Hubbard U     \n".format(u)
            data[35] = "Udd             = {} #-> Hubbard U     \n".format(u)
            data[41] = "Nmeas           = 1e5   \n"
            data[42] = "NCorr           = 20 #-> Wie viele Schritte zwischen zwei Messungen. \n"
    
    with open(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}/Parameters_Q4.in'.format(u,beta,q,mu,t,tPri,tPriPri), 'w', encoding='utf-8') as file:
        file.writelines(data)





    #now copy the FortranCode and change what to change
def createHamiltonian(q, QMCDraftDirectory, QMCCalculationDirectory,
                      beta, u, mu,t,tPri,tPriPri):
    with open(QMCDraftDirectory + '/hofstadter_hamiltonian.f90', 'r', encoding='utf-8') as file:           #calculate ED results on /scratch
        dataFortran = file.readlines()

        dataFortran[5] = "  integer, parameter :: q={}   \n".format(q)

        dataFortran[8] = "  real(kind=8), parameter :: t={}d0   \n".format(t)
        dataFortran[9] = "  real(kind=8), parameter :: t={}d0  \n".format(tPri)
        dataFortran[10] = "  real(kind=8), parameter :: t={}d0  \n".format(tPriPri)
        
    with open(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}/hofstadter_hamiltonian.f90'.format(u,beta,q,mu,t,tPri,tPriPri), 'w', encoding='utf-8') as file:
        file.writelines(dataFortran)




# can change running time and number of cores here
def createSubmit(QMCDraftDirectory, QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri):
    with open(QMCDraftDirectory + '/submit_dmft_script', 'r', encoding='utf-8') as file:
        dataSubmit = file.readlines()
    
        dataSubmit[1] = "#SBATCH -t 4:00:00           \n"
        dataSubmit[2] = "#SBATCH -N 1   \n"
        dataSubmit[16] = "mpirun -np 96 /home/hhpnhytt/w2dynamics/DMFT.py       \n"
    
    with open(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}/submit_dmft_script'.format(u,beta,q,mu,t,tPri,tPriPri), 'w', encoding='utf-8') as file:
        file.writelines(dataSubmit)




#just copy the run.sh
def createRun(QMCDraftDirectory, QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri):
    with open(QMCDraftDirectory + '/run.sh', 'r', encoding='utf-8') as file:
        dataRun = file.readlines()
    
    with open(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}/run.sh'.format(u,beta,q,mu,t,tPri,tPriPri), 'w', encoding='utf-8') as file:
        file.writelines(dataRun)

#NOTE: copy production but better should write it into ProcessingQmcHLRN itself
def createProduction(QMCDraftDirectory, QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri):
    with open(QMCDraftDirectory + '/changeToProductionStyle.py', 'r', encoding='utf-8') as file:
        dataProd = file.readlines()
    
    with open(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}/changeToProductionStyle.py'.format(u,beta,q,mu,t,tPri,tPriPri), 'w', encoding='utf-8') as file:
        file.writelines(dataProd)
    







