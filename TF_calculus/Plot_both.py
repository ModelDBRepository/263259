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




freqsexp,frespEx,muVexcexp,stdexcexp=np.load("TF_B_HHRS.npy")
freqsexp_in,frespinh,muVexcexp,stdexcexp=np.load("TF_B_HHFS.npy")
print("eee",frespinh)

freqsexp_th,frespEx_th=np.load("TF_B_HHRS_th.npy")
freqsexp_th,frespinh_th=np.load("TF_B_HHFS_th.npy")



plt.plot(freqsexp,frespEx,'go',freqsexp_th,frespEx_th,'g-',freqsexp_in,frespinh,'ro',freqsexp_th,frespinh_th,'r-')
plt.show()


