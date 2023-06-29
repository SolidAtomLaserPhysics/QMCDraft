import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


'''
calls a Julia script in the Draft folder,
that reads out the hdf5 file of each calculation and then prints out the self energies
'''
def extractSelfEnergy(QMCCalculationDirectory, QMCDraftDirectory, u,beta,q,mu,t,tPri,tPriPri):
    os.chdir(QMCDraftDirectory)    
    print(1)                  
    os.system('julia readQMCSelfEnergyResults.jl {} {} {} {} {} {} {} {}'.format(u, beta, q, mu, t, tPri, tPriPri, QMCCalculationDirectory))
    print(2)
        
'''
calls a Julia script in the Draft folder,
that reads out the hdf5 file of each calculation and then prints out density
'''
def extractDensity(QMCCalculationDirectory, QMCDraftDirectory, u,beta,q,mu,t,tPri,tPriPri):
    os.chdir(QMCDraftDirectory)                      
    os.system('julia readQMCDensityResults.jl {} {} {} {} {} {} {} {}'.format(u, beta, q, mu, t, tPri, tPriPri, QMCCalculationDirectory))

