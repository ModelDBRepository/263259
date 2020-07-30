from __future__ import print_function

from brian2 import *
from time_varying_input import *
import numpy as np
import matplotlib.pylab as plt
import sys
sys.path.append('../')
from single_cell_models.cell_library import get_neuron_params
from single_cell_models.cell_construct import get_membrane_equation
from synapses_and_connectivity.syn_and_connec_library import get_connectivity_and_synapses_matrix
from synapses_and_connectivity.syn_and_connec_construct import build_up_recurrent_connections_for_2_pop,\
    build_up_recurrent_connections, build_up_poisson_group_to_pop


def run_simulation(NRN_exc='LIF', NRN_inh='LIF', NTWK='Vogels-Abbott', DT=0.1, tstop=300,\
                   kick_value=50., kick_duration=30., SEED=1, ext_drive=0., input_rate=None,\
                   afferent_exc_fraction=0.,
                   n_rec=3, full_recording=False, filename='data/example_data.npy'):

    seed(SEED%100)
    
    M = get_connectivity_and_synapses_matrix(NTWK, number=2)
    if afferent_exc_fraction<.5:
        afferent_exc_fraction = M[0,0]['afferent_exc_fraction']
        
    # number of neurons
    Ne, Ni= int(M[0,0]['Ntot']*(1-M[0,0]['gei'])), int(M[0,0]['Ntot']*M[0,0]['gei'])
    Ne=1
    Ni=1

    exc_neurons, eqs = get_membrane_equation(get_neuron_params(NRN_exc, number=Ne), M[:,0], return_equations=True)
    inh_neurons, eqs = get_membrane_equation(get_neuron_params(NRN_inh, number=Ni), M[:,1], return_equations=True)

    ## INITIAL CONDITIONS


    exc_neurons.Gee, exc_neurons.Gie, exc_neurons.V='0.*nS', '0.*nS', '(-90+30*rand())*mV'
    exc_neurons.p  = '.2'
    inh_neurons.Gei, inh_neurons.Gii, inh_neurons.V = '0.*nS', '0.*nS', '(-90+30*rand())*mV'

    group=exc_neurons
    group.V = -65.*mV
    #group.I = '0.7*nA * i / num_neurons'

    group.I0 = 1.7*nA

    monitor = SpikeMonitor(group)
    trace = StateMonitor(group, 'V', record=0)


    tstop=1000
    DT=DT
    time_array = np.arange(int(tstop/DT))*DT
    run(tstop* ms)
    V = trace[0].V[:]
    Varr=array(V/mV)
    
    plt.plot(time_array,Varr)
    plt.show()

if __name__=='__main__':


    import argparse
    # First a nice documentation 
    parser=argparse.ArgumentParser(description=
     """ 
     ----------------------------------------------------------------------
     Run the a network simulation using brian2

     Choose CELLULAR and NTWK PARAMETERS from the available libraries
     see  ../synapses_and_connectivity.syn_and_connec_library.py for the CELLS
     see ../synapses_and_connectivity.syn_and_connec_library.py for the NTWK

     Then construct the input as "NRN_exc--NRN_inh--NTWK"
     example: "LIF--LIF--Vogels-Abbott"
     ----------------------------------------------------------------------
     """
    ,formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--CONFIG",help="Cell and Network configuration !", default='RS-cell--FS-cell--CONFIG1')
    parser.add_argument("--DT",help="time steps in ms", type=float, default=0.1)
    parser.add_argument("--tstop",help="time of simulation in ms", type=float, default=1500)
    parser.add_argument("--kick_value",help=" stimulation (Hz) for the initial kick", type=float, default=0.)
    parser.add_argument("--kick_duration",help=" stimulation duration (ms) for the initial kick", type=float, default=100.)
    parser.add_argument("--ext_drive",help=" stimulation duration (ms) for the initial kick", type=float, default=4.)
    parser.add_argument("--SEED",help="SEED for the simulation", type=int, default=5)
    parser.add_argument("-f", "--file",help="filename for saving", default='data/example.npy')
    parser.add_argument("--n_rec",help="number of recorded neurons", type=int, default=1)

    args = parser.parse_args()
    
    run_simulation(\
                   NRN_exc=args.CONFIG.split('--')[0],\
                   NRN_inh=args.CONFIG.split('--')[1],\
                   NTWK=args.CONFIG.split('--')[2],
                   kick_value=args.kick_value, kick_duration=args.kick_duration,
                   DT=args.DT, tstop=args.tstop, SEED=args.SEED, ext_drive=args.ext_drive,\
                   full_recording=True, n_rec=args.n_rec, filename=args.file)

    
