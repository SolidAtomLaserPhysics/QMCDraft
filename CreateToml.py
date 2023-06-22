import numpy as np
import os
import toml




def CreateConfigs(Beta, P, L, U, Ns, Mu, blueprintConfigPath, configTargetDirectory):


    for beta in Beta:
        for p in P:
            for l in L:
                for u in U:
                        for ns in Ns:
                                for mu in Mu:
                                    if not os.path.exists(configTargetDirectory + "/B{}_P{}_L{}_steps{}_Ns{}_Mu{}/".format(beta, p, l, steps, ns, mu)):                                  #make directory if not exists already
                                        os.makedirs(configTargetDirectory + "/B{}_P{}_L{}_steps{}_Ns{}_Mu{}/".format(beta, p, l, steps, ns, mu))
                                    startFile = toml.load(blueprintConfigPath)                             #opens and loads the toml file
                            

                                    #lines you want to change in the config.toml
                                    startFile['parameters']['beta'] = beta
                                    startFile['parameters']['U'] = u
                                    startFile['parameters']['mu'] = mu
                                    startFile['parameters']['p'] = p
                                    startFile['parameters']['L'] = l
                                    startFile['parameters']['Ksteps'] = 100                     #kSteps fixed to 100 as in ED
                                    startFile['parameters']['Ns'] = ns
                                    startFile['parameters']['Symm'] = "false"                     #symmetry fixed to false since tPrime
                                
                                    #lines we have to add as well to fit what the Wrapper wants
                                    startFile['ED']['ksteps'] = 100                             #kSteps fixed to 100 as in ED
                                    startFile['ED']['ns'] = ns
                                    startFile['ED']['symm'] = "false"                     #symmetry fixed to false since tPrime

                                    endFile = open(configTargetDirectory + "/B{}_P{}_L{}_steps{}_Ns{}_symm{}/config_U{}_Mu{}.toml".format(beta, p, l, steps, ns, symm, u, u/2),'w+')           #opens the toml file
                                    toml.dump(startFile, endFile)        #writes into toml file
                                    endFile.close()







