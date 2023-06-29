using HDF5
using DelimitedFiles



U = ARGS[1]
Beta = 3ARGS[2]
q = ARGS[3]
mu = ARGS[4]
t = ARGS[5]
tPrime = ARGS[6]
tPrimePrime = ARGS[7]
QMCCalculationDirectory = ARGS[8]


fileName = QMCCalculationDirectory * "/finalQMC_U$(U)_B_$(Beta)_q$(q)_mu$(mu)_t$(t)_tPri$(tPrime)_tPriPri$(tPrimePrime)/U$(U)_mu$(mu)_B$(Beta)_L$(q)_t$(t)_tPri$(tPrime)_tPriPri$(tPrimePrime).hdf5"


f = h5open(fileName, "r")
Values = read(f["dmft-last/ineq-001/siw/value"])
Frequencies = read(f[".axes/iw"])

siw = Values[:,1,1]

RealPart = [real(siw[800:1200])]                                #apparently Real Part is 2D array but only 1 element in that one direction. In reality vector
ImagPart = [imag(siw[800:1200])]
MatsubaraFreq = Frequencies[800:1200]

vv = [MatsubaraFreq RealPart[1] ImagPart[1]]

writedlm(QMCCalculationDirectory + "/finalQMC_U$(U)_B_$(Beta)_q$(q)_mu$(mu)_t$(t)_tPri$(tPrime)_tPriPri$(tPrimePrime)/self-en_wim_QMC-U$(U)_B$(Beta)_q$(q)_mu$(mu)_t$(t)_tPri$(tPrime)_tPriPri$(tPrimePrime).csv", vv)
