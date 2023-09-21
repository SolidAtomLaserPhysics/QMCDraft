import numpy as np
import os
import math
import cmath
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D




def plotSigmaQMC(QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri, kSteps):
    dataSelfEnergy = np.loadtxt(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}_kSteps{}/self-en_wim_QMC-U{}_mu{}_B{}_q{}_t{}_tPri{}_tPriPri{}_kSteps{}.csv'.format(u,beta,q,mu,t,tPri,tPriPri,kSteps, u,mu,beta,q,t,tPri,tPriPri,kSteps))
    MatsubaraFreq = dataSelfEnergy[:, 0]
    RealPart = dataSelfEnergy[:, 1]
    ImagPart = dataSelfEnergy[:, 2]
    halfArray = int((len(MatsubaraFreq)/2))

    plt.plot(MatsubaraFreq[halfArray:(halfArray+20)], ImagPart[halfArray:(halfArray+20)])                            #only plot until Matsubara frequency is the 20s value to see more structure
    plt.xlabel(r'$\nu$')
    plt.ylabel(r'Im($\Sigma$)')
    plt.savefig(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}_kSteps{}/selfEnergyPlot_QMC-U{}_B{}_q{}_mu{}_t{}_tPri{}_tPriPri{}_kSteps{}.png'.format(u,beta,q,mu,t,tPri,tPriPri,kSteps, u,beta,q,mu,t,tPri,tPriPri,kSteps))
    plt.clf()
 




def plotDensityQMC(QMCCalculationDirectory, u,beta,q,Mu,t,tPri,tPriPri, kSteps):
    allDensities = np.zeros(len(Mu))
    for i_mu in range(len(Mu)):
        dataDensity = np.loadtxt(QMCCalculationDirectory + '''/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}_kSteps{}/densityValues-U{}_mu{}_B{}_q{}_t{}_tPri{}_tPriPri{}_kSteps{}.csv'''.format(u,beta,q,Mu[i_mu],t,tPri,tPriPri,kSteps, u,Mu[i_mu],beta,q,t,tPri,tPriPri,kSteps), dtype=float)
        allDensities[i_mu] = (dataDensity[0] + dataDensity[3])/2

    
    plt.plot(Mu, allDensities, marker = 'x')                         
    plt.xlabel(r'$\mu$')
    plt.ylabel('n')
    plt.savefig(QMCCalculationDirectory + '/density_QMC-U{}_B{}_q{}_t{}_tPri{}_tPriPri{}_kSteps{}.png'.format(u,beta,q,t,tPri,tPriPri,kSteps))
    plt.clf()

