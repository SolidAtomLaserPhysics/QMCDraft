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

fileName = string(QMCCalculationDirectory, "/finalQMC_U$(U)_B_$(Beta)_q$(q)_mu$(mu)_t$(t)_tPri$(tPrime)_tPriPri$(tPrimePrime)_kSteps$(kSteps)/U$(U)_mu$(mu)_B$(Beta)_q$(q)_t$(t)_tPri$(tPrime)_tPriPri$(tPrimePrime)_kSteps$(kSteps)_DMFT.hdf5")
#fileName = string(QMCCalculationDirectory, "/finalQMC_U$(U)_B_$(Beta)_q$(q)_mu$(mu)_t$(t)_tPri$(tPrime)_tPriPri$(tPrimePrime)_kSteps$(kSteps)_testSIW/DMFT_1.hdf5")


f = h5open(fileName, "r")
Values = read(f["dmft-last/ineq-001/siw/value"])
Frequencies = read(f[".axes/iw"])

siw = Values[:,1,1]

RealPart = [real(siw[800:1200])]                                #apparently Real Part is 2D array but only 1 element in that one direction. In reality vector
ImagPart = [imag(siw[800:1200])]
MatsubaraFreq = Frequencies[800:1200]




vv = [MatsubaraFreq RealPart[1] ImagPart[1]]

outputName = string(QMCCalculationDirectory, "/finalQMC_U$(U)_B_$(Beta)_q$(q)_mu$(mu)_t$(t)_tPri$(tPrime)_tPriPri$(tPrimePrime)_kSteps$(kSteps)/self-en_wim_QMC_1.csv")

writedlm(outputName, vv)
