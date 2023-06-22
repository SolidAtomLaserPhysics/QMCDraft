import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


'''
changes the submit script to 5 Nodes for the calculation
'''
def changeSubmit():
    with open('submit_dmft_script', 'r', encoding='utf-8') as file:
        data = file.readlines()
  
    data[2] = "#SBATCH -N 5 \n"
    data[16] = "mpirun -np 480 /home/hhpnhytt/w2dynamics/DMFT.py \n"
  
    with open('submit_dmft_script', 'w', encoding='utf-8') as file:
        file.writelines(data)


def changeParametersIn():
    with open('Parameters.in', 'r', encoding='utf-8') as file:
        data = file.readlines()
  
    data[11] = "DMFTsteps       = 10 #-> Anzahl der DMFT loops       \n"                     #set amount of DMFT loops to 10
    #data[37] = "Nmeas           = 1e6   \n"
  
    with open('Parameters.in', 'w', encoding='utf-8') as file:
        file.writelines(data)






if __name__ == "__main__":
    changeSubmit()
    changeParametersIn()







