import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

import createDirectories.py as CreateDir
import changeToProductionStyle.py as changeToProd







if __name__ == "__main__":
    U = [1.5, 3.0]
    Mu = [1.0]
    Beta = [30.0, 70.0]
    Q = [3]
    T = [0.25]
    TPrime = [0.025]
    TPrimePrime = [0.0]

    QMCCalculationDirectory = '/scratch/usr/hhpnhytt/finalEDResults/finalQMC'
    

    preCalculation = True
    calculation = False

    for u in U:
        for mu in Mu:
            for beta in Beta:
                for q in Q:
                    for t in T:
                        for tPri in TPrime:
                            for tPriPri in TPrimePrime:
                                if preCalculation:
                                    CreateDir.createDirectories(QMCCalculationDirectory + "/U{}_mu{}_B{}_L{}_t{}_tPri{}_tPriPri{}".format(u, mu, beta, q, t, tPri, tPriPri))
                                    CreateDir.createFilesInDirectories(u, mu, beta, q, t, tPri, tPriPri, QMCCalculationDirectory)
                                if calculation:







