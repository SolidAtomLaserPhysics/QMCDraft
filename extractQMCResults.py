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




def extractSelfEnergy(QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri):
    with open(QMCDraftDirectory + '/submit_dmft_script', 'r', encoding='utf-8') as file:
        


