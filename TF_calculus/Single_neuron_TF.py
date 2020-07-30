import numpy as np
import sys
sys.path.append('../')
from transfer_functions.tf_simulation import single_experiment_2,single_experiment
from transfer_functions.load_config import load_transfer_functions
from scipy.integrate import odeint
from single_cell_models.cell_library import get_neuron_params
from synapses_and_connectivity.syn_and_connec_library import get_connectivity_and_synapses_matrix
from transfer_functions.tf_simulation import reformat_syn_parameters
import matplotlib.pylab as plt

from scipy.optimize import fsolve
from scipy.optimize import minimize
import math


NTWK='CONFIG1'
NRN1B='HH_RS'







M = get_connectivity_and_synapses_matrix(NTWK, SI_units=True)

params = get_neuron_params(NRN1B, SI_units=True)
reformat_syn_parameters(params, M)


Qe, Te, Ee = params['Qe'], params['Te'], params['Ee']
Qi, Ti, Ei = params['Qi'], params['Ti'], params['Ei']
Gl, Cm , El = params['Gl'], params['Cm'] , params['El']
pconnec,Ntot,gei,ext_drive=params['pconnec'], params['Ntot'] , params['gei'],M[0,0]['ext_drive']





N = 8
freqs = np.linspace(3, 7, N)




frespEx=0*freqs
muVexcexp=0*freqs
stdexcexp=0*freqs

conta=0
seeds = np.arange(len(freqs))

ddt=5e-6

finhib=8.

t = np.arange(int(15./ddt))*ddt



for freq, seed in zip(freqs, seeds):
   
   
    fetrue=freqs[conta]


    finhib=0;
    fetrue=0;
    
                                

    
    frespEx[conta],muVexcexp[conta],stdexcexp[conta]= single_experiment_2(t,\
                                                fetrue*(1.-gei)*pconnec*Ntot,
                                                finhib*gei*pconnec*Ntot, params, seed=0)
                                                
                                                



    print("HERE: ",freqs[conta],frespEx[conta])




    conta+=1

np.save("TF_B_HHRS.npy",[freqs,frespEx,muVexcexp,stdexcexp])




