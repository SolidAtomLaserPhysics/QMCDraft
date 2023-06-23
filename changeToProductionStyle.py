import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


'''
changes the submit script to 5 Nodes for the calculation
'''
def createSubmit(QMCDraftDirectory, QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri):
    with open(QMCDraftDirectory + '/submit_dmft_script', 'r', encoding='utf-8') as file:
        dataSubmit = file.readlines()
    
        dataSubmit[1] = "#SBATCH -t 4:00:00           \n"
        dataSubmit[2] = "#SBATCH -N 2   \n"
        dataSubmit[4] = "#SBATCH -p standard96     \n"                                            
        dataSubmit[16] = "mpirun -np 96 /home/hhpnhytt/w2dynamics/DMFT.py       \n"
    
    with open(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}/submit_dmft_script'.format(u,beta,q,mu,t,tPri,tPriPri), 'w', encoding='utf-8') as file:
        file.writelines(dataSubmit)



def createParameters(u, mu, beta, q, t, tPri, tPriPri, QMCDraftDirectory, QMCCalculationDirectory, nCorr):
    if q == 3:
        with open(QMCDraftDirectory + '/Parameters_Q3.in', 'r', encoding='utf-8') as file:
            data = file.readlines()
    
            data[2] = "NAt             = 3 #q des Magnetfeldes p/q      \n"
            data[5] = "beta            = {} #-> In Einheiten 1/t.     \n".format(beta)  
            data[7] = "mu              = {}         \n".format(mu) 
            data[10] = "#fileold         = U{}_mu{}_B{}_L{}_t{}_tPri{}_tPriPri{}_DMFT.hdf5 #-> Hier wird jede Iteration gespeichert. Von dort kann ich weiterrechnen.      \n".format(u, mu, beta, q, t, tPri, tPriPri)
            data[11] = "DMFTsteps       = 30 #-> Anzahl der DMFT loops     \n"
            data[14] = "FileNamePrefix  = U{}_mu{}_B{}_L{}_t{}_tPri{}_tPriPri{}_DMFT   \n".format(u, mu, beta, q, t, tPri, tPriPri)
            data[23] = "Udd             = {} #-> Hubbard U     \n".format(u)
            data[27] = "Udd             = {} #-> Hubbard U     \n".format(u)
            data[31] = "Udd             = {} #-> Hubbard U     \n".format(u)
            data[37] = "Nmeas           = 1e6   \n"
            data[38] = "NCorr           = {} #-> Wie viele Schritte zwischen zwei Messungen. \n".format(nCorr)
        with open(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}/Parameters.in'.format(u,beta,q,mu,t,tPri,tPriPri), 'w', encoding='utf-8') as file:
            file.writelines(data)
    
    if q == 4:
        with open(QMCDraftDirectory + '/Parameters_Q4.in', 'r', encoding='utf-8') as file:
            data = file.readlines()
    
            data[2] = "NAt             = 4 #q des Magnetfeldes p/q      \n"
            data[5] = "beta            = {} #-> In Einheiten 1/t.     \n".format(beta)  
            data[7] = "mu              = {}         \n".format(mu) 
            data[10] = "#fileold         = U{}_mu{}_B{}_L{}_t{}_tPri{}_tPriPri{}_DMFT.hdf5 #-> Hier wird jede Iteration gespeichert. Von dort kann ich weiterrechnen.      \n".format(u, mu, beta, q, t, tPri, tPriPri)
            data[11] = "DMFTsteps       = 30 #-> Anzahl der DMFT loops     \n"
            data[14] = "FileNamePrefix  = U{}_mu{}_B{}_L{}_t{}_tPri{}_tPriPri{}_DMFT   \n".format(u, mu, beta, q, t, tPri, tPriPri)
            data[23] = "Udd             = {} #-> Hubbard U     \n".format(u)
            data[27] = "Udd             = {} #-> Hubbard U     \n".format(u)
            data[31] = "Udd             = {} #-> Hubbard U     \n".format(u)
            data[35] = "Udd             = {} #-> Hubbard U     \n".format(u)
            data[41] = "Nmeas           = 1e6   \n"
            data[42] = "NCorr           = {} #-> Wie viele Schritte zwischen zwei Messungen. \n".format(nCorr)
    
        with open(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}/Parameters.in'.format(u,beta,q,mu,t,tPri,tPriPri), 'w', encoding='utf-8') as file:
            file.writelines(data)









