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


NRN1='HH_RS'
NRN2='HH_RS'


TF1, TF2 = load_transfer_functions(NRN1, NRN2, NTWK)




M = get_connectivity_and_synapses_matrix(NTWK, SI_units=True)
params = get_neuron_params(NRN1, SI_units=True)
reformat_syn_parameters(params, M)
paramsinh = get_neuron_params(NRN2, SI_units=True)
reformat_syn_parameters(paramsinh, M)

Qe, Te, Ee = params['Qe'], params['Te'], params['Ee']
Qi, Ti, Ei = params['Qi'], params['Ti'], params['Ei']
Gl, Cm , El = params['Gl'], params['Cm'] , params['El']
pconnec,Ntot,gei,ext_drive=params['pconnec'], params['Ntot'] , params['gei'],M[0,0]['ext_drive']






N = 100
freqs = np.linspace(3, 7, N)




frespthEx=0*freqs
muVexcth=0*freqs
stdexcth=0*freqs




conta=0
seeds = np.arange(len(freqs))

ddt=5e-6

finhib=8.

t = np.arange(int(10./ddt))*ddt



for freq, seed in zip(freqs, seeds):
   
   
    fetrue=freqs[conta]

                                                
    
    
    
    
    
    frespthEx[conta]=TF1(fetrue, finhib)
    




    muGe, muGi = Qe*Te*fetrue*(1.-gei)*pconnec*Ntot, Qi*Ti*finhib*gei*pconnec*Ntot
    muG = Gl+muGe+muGi
    muVV=(muGe*Ee+muGi*Ei+Gl*El)/muG
    
    
    muGn, Tm = muG/Gl, Cm/muG

    Ue, Ui = Qe/muG*(Ee-muVV), Qi/muG*(Ei-muVV)

    sV = np.sqrt(\
             (1.-gei)*pconnec*Ntot*fetrue*(Ue*Te)**2/2./(Te+Tm)+\
             gei*pconnec*Ntot*finhib*(Ti*Ui)**2/2./(Ti+Tm))
    

    muVexcth[conta]=muVV
    stdexcth[conta]=sV




    conta+=1



np.save("TF_B_HHRS_th.npy",[freqs,frespthEx])
freqsexp,frespEx,muVexcexp,stdexcexp=np.load("TF_B_HHRS.npy")

plt.plot(freqsexp,frespEx,'go',freqs,frespthEx,'g-')
plt.show()


plt.plot(freqsexp,muVexcexp,'go',freqs,muVexcth,'g-')
plt.show()

plt.plot(freqsexp,stdexcexp,'go',freqs,stdexcth,'g-')
plt.show()




