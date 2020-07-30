"""
This script connects the different synapses to a target neuron
"""
from __future__ import print_function
from brian2 import *


def build_up_recurrent_connections_for_2_pop(Pops, syn_conn_matrix, SEED=1):

    seed(SEED)
    
    exc_neurons, inh_neurons = Pops
    P = syn_conn_matrix
    # exc_exc
    exc_exc = Synapses(exc_neurons, exc_neurons, model='w:siemens', on_pre='Gee_post += w')
    exc_exc.connect('i!=j', p=P[0,0]['p_conn'])
    exc_exc.w = P[0,0]['Q']*nS
    # exc_inh
    exc_inh = Synapses(exc_neurons, inh_neurons, model='w:siemens' ,on_pre='Gei_post += w')
    exc_inh.connect('i!=j', p=P[0,1]['p_conn'])
    exc_inh.w = P[0,1]['Q']*nS
    # inh_exc
    inh_exc = Synapses(inh_neurons, exc_neurons, model='w:siemens' ,on_pre='Gie_post += w')
    inh_exc.connect('i!=j', p=P[1,0]['p_conn'])
    inh_exc.w = P[1,0]['Q']*nS
    # inh_inh
    inh_inh = Synapses(inh_neurons, inh_neurons, model='w:siemens', on_pre='Gii_post += w')
    inh_inh.connect('i!=j', p=P[1,1]['p_conn'])
    inh_inh.w = P[1,1]['Q']*nS
    return exc_exc, exc_inh, inh_exc, inh_inh


def build_up_recurrent_connections(NeuronGroups, syn_conn_matrix):

    CONNECTIONS = np.empty((len(NeuronGroups), len(NeuronGroups)))
    
    if len(NeuronGroups)!=syn_conn_matrix.shape[0]:
        print('problem the matrix of connectivity and synapses does not')
        print('match the number of populations')

    for jj in range(len(NeuronGroups)):
        # loop over post-synaptic neurons
        for ii in range(len(NeuronGroups)):
            # loop over presynaptic neurons
            CONNECTIONS[ii,jj] = Synapses(NeuronGroups[ii], NeuronGroups[jj],\
                                          model='w:siemens',\
                                          name=syn_conn_matrix[ii,jj]['name'],
                                          on_pre='G'+syn_conn_matrix[ii,jj]['name']+'_post +=w')
            CONNECTIONS[ii,jj].connect('i != j', p=syn_conn_matrix[ii,jj]['p_conn'])  # exclude self-connections
            CONNECTIONS[ii,jj].w = syn_conn_matrix[ii,jj]['Q']*nS
    return CONNECTIONS

def build_up_poisson_group_to_pop(list_of_freqs, list_of_synapses, target_group):

    CONNECTIONS = np.empty(len(NeuronGroups), dtype=object)

    return CONNECTIONS

 
