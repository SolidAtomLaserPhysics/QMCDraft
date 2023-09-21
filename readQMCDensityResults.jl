using HDF5
using DelimitedFiles



U = ARGS[1]
Beta = ARGS[2]
q = ARGS[3]
mu = ARGS[4]
t = ARGS[5]
tPrime = ARGS[6]
tPrimePrime = ARGS[7]
kSteps = ARGS[8]
QMCCalculationDirectory = ARGS[9]



fileName = string(QMCCalculationDirectory, "/finalQMC_U$(U)_B_$(Beta)_q$(q)_mu$(mu)_t$(t)_tPri$(tPrime)_tPriPri$(tPrimePrime)_kSteps$(kSteps)/U$(U)_mu$(mu)_B$(Beta)_q$(q)_t$(t)_tPri$(tPrime)_tPriPri$(tPrimePrime)_kSteps$(kSteps)DMFT.hdf5")
f = h5open(fileName, "r")
Values = read(f["dmft-last/ineq-001/occ/value"])    
Error = read(f["dmft-last/ineq-001/occ/error"])            







occupation1 = Values[:,:,1,1]
error1 = Error[:,:,1,1]


outputNameValues = string(QMCCalculationDirectory, "/finalQMC_U$(U)_B_$(Beta)_q$(q)_mu$(mu)_t$(t)_tPri$(tPrime)_tPriPri$(tPrimePrime)_kSteps$(kSteps)//densityValues-U$(U)_mu$(mu)_B$(Beta)_q$(q)_t$(t)_tPri$(tPrime)_tPriPri$(tPrimePrime)_kSteps$(kSteps).csv")
outputNameErrors = string(QMCCalculationDirectory, "/finalQMC_U$(U)_B_$(Beta)_q$(q)_mu$(mu)_t$(t)_tPri$(tPrime)_tPriPri$(tPrimePrime)_kSteps$(kSteps)//densityErrors-U$(U)_mu$(mu)_B$(Beta)_q$(q)_t$(t)_tPri$(tPrime)_tPriPri$(tPrimePrime)_kSteps$(kSteps).csv")
writedlm(outputNameValues, Values)
writedlm(outputNameErrors, Error)

