import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


'''
calls a Julia script in the Draft folder,
that reads out the hdf5 file of each calculation and then prints out the self energies
'''
#TODO: ksteps implement
def extractSelfEnergy(QMCCalculationDirectory, QMCDraftDirectory, u,beta,q,mu,t,tPri,tPriPri, kSteps):
    os.chdir(QMCDraftDirectory)                  
    os.system('julia readQMCSelfEnergyResults.jl {} {} {} {} {} {} {} {} {}'.format(u, beta, q, mu, t, tPri, tPriPri, kSteps, QMCCalculationDirectory))
        
'''
calls a Julia script in the Draft folder,
that reads out the hdf5 file of each calculation and then prints out density
'''
def extractDensity(QMCCalculationDirectory, QMCDraftDirectory, u,beta,q,mu,t,tPri,tPriPri,kSteps):
    os.chdir(QMCDraftDirectory)                      
    os.system('julia readQMCDensityResults.jl {} {} {} {} {} {} {} {} {}'.format(u, beta, q, mu, t, tPri, tPriPri, kSteps, QMCCalculationDirectory))

