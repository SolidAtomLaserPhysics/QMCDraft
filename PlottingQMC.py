import numpy as np
import os
import math
import cmath
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D




def plotSigmaQMC(QMCCalculationDirectory, u,beta,q,mu,t,tPri,tPriPri):
    dataSelfEnergy = np.loadtxt(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}/self-en_wim_QMC-U{}_B{}_q{}_mu{}_t{}_tPri{}_tPriPri{}.csv'.format(u,beta,q,mu,t,tPri,tPriPri, u,beta,q,mu,t,tPri,tPriPri))
    MatsubaraFreq = dataSelfEnergy[:, 0]
    RealPart = dataSelfEnergy[:, 1]
    ImagPart = dataSelfEnergy[:, 2]
    halfArray = int((len(MatsubaraFreq)/2))

    plt.plot(MatsubaraFreq[halfArray:(halfArray+20)], ImagPart[halfArray:(halfArray+20)])                            #only plot until Matsubara frequency is the 20s value to see more structure
    plt.xlabel(r'$\nu$')
    plt.ylabel(r'Im($\Sigma$)')
    plt.savefig(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}/selfEnergyPlot_QMC-U{}_B{}_q{}_mu{}_t{}_tPri{}_tPriPri{}.png'.format(u,beta,q,mu,t,tPri,tPriPri, u,beta,q,mu,t,tPri,tPriPri))
    plt.clf()
 




def plotDensityQMC(QMCCalculationDirectory, u,beta,q,Mu,t,tPri,tPriPri):
    allDensities = np.zeros(len(Mu))
    for i_mu in range(len(Mu)):
        dataDensity = np.loadtxt(QMCCalculationDirectory + '/finalQMC_U{}_B_{}_q{}_mu{}_t{}_tPri{}_tPriPri{}/DensityQMC-U{}_B{}_q{}_mu{}_t{}_tPri{}_tPriPri{}.txt'.format(u,beta,q,Mu[i_mu],t,tPri,tPriPri, u,beta,q,Mu[i_mu],t,tPri,tPriPri))
        allDensities[i_mu] = dataDensity

    
    plt.plot(Mu, allDensities)                         
    plt.xlabel(r'$\mu$')
    plt.ylabel('n')
    plt.savefig(QMCCalculationDirectory + '/density_QMC-U{}_B{}_q{}_t{}_tPri{}_tPriPri{}.png'.format(u,beta,q,t,tPri,tPriPri))
    plt.clf()

