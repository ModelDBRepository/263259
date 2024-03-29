import numpy as np
import numba # with NUMBA to make it faster !!!
import argparse
import matplotlib.pylab as plt
### ================================================
### ========== Reformat parameters  ================
### ======= for single cell simulation =============
### ================================================


def reformat_syn_parameters(params, M):
    """
    valid only of no synaptic differences between excitation and inhibition
    """

    params['Qe'], params['Te'], params['Ee'] = M[0,0]['Q'], M[0,0]['Tsyn'], M[0,0]['Erev']
    params['Qi'], params['Ti'], params['Ei'] = M[1,1]['Q'], M[1,1]['Tsyn'], M[1,1]['Erev']
    params['pconnec'] = M[0,0]['p_conn']
    params['Ntot'], params['gei'] = M[0,0]['Ntot'], M[0,0]['gei']
    

### ================================================
### ======== Conductance Time Trace ================
### ====== Poisson + Exponential synapses ==========
### ================================================

def generate_conductance_shotnoise(freq, t, N, Q, Tsyn, g0=0, seed=0):
    """
    generates a shotnoise convoluted with a waveform
    frequency of the shotnoise is freq,
    K is the number of synapses that multiplies freq
    g0 is the starting value of the shotnoise
    """
    if freq==0:
        freq=1e-9
    upper_number_of_events = max([int(3*freq*t[-1]*N),1]) # at least 1 event
    np.random.seed(seed=seed)
    spike_events = np.cumsum(np.random.exponential(1./(N*freq),\
                             upper_number_of_events))
    g = np.ones(t.size)*g0 # init to first value
    dt, t = t[1]-t[0], t-t[0] # we need to have t starting at 0
    # stupid implementation of a shotnoise
    event = 0 # index for the spiking events
    for i in range(1,t.size):
        g[i] = g[i-1]*np.exp(-dt/Tsyn)
        while spike_events[event]<=t[i]:
            g[i]+=Q
            event+=1
    return g

### ================================================
### ======== AdExp model (with IaF) ================
### ================================================




def pseq_hh(cell_params):
    """ function to extract all parameters to put in the simulation
        (just because you can't pass a dict() in Numba )"""
    
    # those parameters have to be set
    El, Gl,GNa,GK,GM,ENa,EK  = cell_params['El'], cell_params['Gl'],cell_params['GNa'], cell_params['GK'],cell_params['GM'], cell_params['ENa'],cell_params['EK']
    Ee, Ei = cell_params['Ee'], cell_params['Ei']
    Cm = cell_params['Cm']
    VT=cell_params['VT']# then those can be optional

    return Gl,GNa,GK,GM, Cm , El,ENa,EK, Ee, Ei,VT





def hh_sim(t, I, Ge, Gi,
              Gl,GNa,GK,GM, Cm , El,ENa,EK, Ee, Ei,VT):
    """ functions that solve the membrane equations for the
        adexp model for 2 time varying excitatory and inhibitory
        conductances as well as a current input
        returns : v, spikes
    """

    
    last_spike = -np.inf # time of the last spike, for the refractory period
    V, spikes = El*np.ones(len(t), dtype=np.float), []
    dt = t[1]-t[0]
    
    
    
    
    w, i_exp,m,n,h,p = 0., 0.,0.,0.,0.,0. # w and i_exp are the exponential and adaptation currents

    #print("params",GM,VT,Cm)
    
    shifth=20*0.001
    
    shifth=0*0.001
    
    refrh=0.1
    
    for i in range(len(t)-1):

        
        m = m + 1000*dt*((0.32*(13.-1000.*V[i]+1000.*VT)/(np.exp((13.-1000.*V[i]+1000.*VT)/(4.))-1.))*(1-m)-(0.28*(1000.*V[i]-1000.*VT-40.)/(np.exp((1000.*V[i]-1000.*VT-40.)/(5.))-1.))*m)
        
        
        n = n + 1000*dt*(0.032*(15.-1000.*V[i]+1000.*VT)/(np.exp((15.-1000.*V[i]+1000.*VT)/(5.))-1.)*(1.-n)-.5*np.exp((10.-1000.*V[i]+1000.*VT)/(40.))*n)
        
        alphah=0.128*np.exp((17.-1000.*(V[i]-shifth)+1000.*VT)/(18.))
        betah=4./(1+np.exp((40.-1000.*(V[i]-shifth)+1000.*VT)/(5.)))
        
        '''
        alphah=alphah/100
        betah=betah/100
        '''
        h = h + 1000*dt*(alphah*(1.-h)-betah*h)
        
        p = p + 1000*dt*(((1./(np.exp(-(35.+1000.*V[i])/(10.))+1.))-p)/((4000.)/(3.3*( np.exp((35.+1000.*V[i])/(20.)) )+1.*(np.exp(-(35.+1000.*V[i])/(20.))) )))

        
        V[i+1] = V[i] + dt/Cm*(I[i] +\
                               Gl*(El-V[i]) + Ge[i]*(Ee-V[i]) + Gi[i]*(Ei-V[i])+\
                               GNa*(m*m*m)*h*(ENa-V[i]) +\
                               GK*(n*n*n*n)*(EK-V[i])  +\
                               GM*p*(EK-V[i]))
            
            
            
        #if ((V[i+1] > -0.04) & (t[i+1]-last_spike>0.005)):
        #if ((V[i+1] > 0.01) & (t[i+1]-last_spike>0.002)):

        if((V[i+1] > 0.01) & (V[i]<0.01) &(t[i+1]-last_spike>0.0002)):
            
                                   
            last_spike = t[i+1]
            
                                       
            if t[i+1] > 5.:
                spikes.append(t[i+1])
    
    '''
    plt.plot(1000*t,V)
    plt.show()
    '''
    return V, np.array(spikes)



### ================================================
### ========== Single trace experiment  ============
### ================================================

def single_experiment(t, fe, fi, params, seed=0):
    ## fe and fi total synaptic activities, they include the synaptic number
    ge = generate_conductance_shotnoise(fe, t, 1, params['Qe'], params['Te'], g0=0, seed=seed)
    gi = generate_conductance_shotnoise(fi, t, 1, params['Qi'], params['Ti'], g0=0, seed=seed)
    I = np.zeros(len(t))
    v, spikes = adexp_sim(t, I, ge, gi, *pseq_adexp(params))
    return len(spikes)/t.max() # finally we get the output frequency



def single_experiment_2(t, fe, fi, params, seed=0):
    ## fe and fi total synaptic activities, they include the synaptic number
    ge = generate_conductance_shotnoise(fe, t, 1, params['Qe'], params['Te'], g0=0, seed=seed)
    gi = generate_conductance_shotnoise(fi, t, 1, params['Qi'], params['Ti'], g0=0, seed=seed)
    

    
    a, b, tauw = params['a'],\
        params['b'], params['tauw']
    Qe, Te, Ee = params['Qe'], params['Te'], params['Ee']
    Qi, Ti, Ei = params['Qi'], params['Ti'], params['Ei']
    Gl,GNa,GK,GM, Cm , El,ENa,EK = params['Gl'],params['GNa'],params['GK'],params['GM'], params['Cm'] , params['El'],params['ENa'],params['EK']
    VT=params['VT']
    I = 0.*np.ones(len(t))
    #I = 2*1.e-9*np.ones(len(t))
    
    v, spikes= hh_sim(t, I, ge, gi, *pseq_hh(params))


    
    
    
    froutput=len(spikes)/(t.max()-5.)
    

   
   #print("DATA",froutput,v[(v>-0.085)].mean(),v[(v>-0.085)].std(),v[(v<-0.04)].mean(),v[(v<-0.04)].std())
    return froutput,v[(v<-0.04)].mean(),v[(v<-0.04)].std() # finally we get the output frequency



### ================================================
### ========== Transfer Functions ==================
### ================================================

### generate a transfer function's data
def generate_transfer_function(params,\
                               MAXfexc=40., MAXfinh=30., MINfinh=2.,\
                               discret_exc=9, discret_inh=8, MAXfout=35.,\
                               SEED=3,\
                               verbose=False,
                               filename='data/example_data.npy',
                               dt=5e-5, tstop=10):
    """ Generate the data for the transfer function  """
    
    t = np.arange(int(tstop/dt))*dt

    # this sets the boundaries (factor 20)
    dFexc = MAXfexc/discret_exc
    fiSim=np.linspace(MINfinh,MAXfinh, discret_inh)
    feSim=np.linspace(0, MAXfexc, discret_exc) # by default
    MEANfreq = np.zeros((fiSim.size,feSim.size))
    SDfreq = np.zeros((fiSim.size,feSim.size))
    Fe_eff = np.zeros((fiSim.size,feSim.size))
    JUMP = np.linspace(0,MAXfout,discret_exc) # constrains the fout jumps

    for i in range(fiSim.size):
        Fe_eff[i][:] = feSim # we try it with this scaling
        e=1 # we start at fe=!0
        while (e<JUMP.size):
            vec = np.zeros(SEED)
            vec[0],avv,stdv= single_experiment_2(t,\
                Fe_eff[i][e]*(1-params['gei'])*params['pconnec']*params['Ntot'],
                fiSim[i]*params['gei']*params['pconnec']*params['Ntot'], params, seed=0)

            if (vec[0]>JUMP[e-1]): # if we make a too big jump
                # we redo it until the jump is ok (so by a small rescaling of fe)
                # we divide the step by 2
                Fe_eff[i][e] = (Fe_eff[i][e]-Fe_eff[i][e-1])/2.+Fe_eff[i][e-1]
                if verbose:
                    print("we rescale the fe vector [...]")
                # now we can re-enter the loop as the same e than entering..
            else: # we can run the rest
                if verbose:
                    print("== the excitation level :", e+1," over ",feSim.size)
                    print("== ---- the inhibition level :", i+1," over ",fiSim.size)
                for seed in range(1,SEED):
                    params['seed'] = seed
                    vec[seed],avv,stdv = single_experiment_2(t,\
                            Fe_eff[i][e]*(1-params['gei'])*params['pconnec']*params['Ntot'],\
                            fiSim[i]*params['gei']*params['pconnec']*params['Ntot'], params, seed=seed)
                    if verbose:
                        print("== ---- _____________ seed :",seed)
                MEANfreq[i][e] = vec.mean()
                SDfreq[i][e] = vec.std()
                if verbose:
                    print("== ---- ===> Fout :",MEANfreq[i][e])
                if e<feSim.size-1: # we set the next value to the next one...
                    Fe_eff[i][e+1] = Fe_eff[i][e]+dFexc
                e = e+1 # and we progress in the fe loop
                
        # now we really finish the fe loop

    # then we save the results
    np.save(filename, np.array([MEANfreq, SDfreq, Fe_eff, fiSim, params]))
    print('numerical TF data saved in :', filename)

if __name__=='__main__':

    # First a nice documentation 
    parser=argparse.ArgumentParser(description=
     """ Runs two types of protocols on a given neuronal and network model
        1)  ==> Preliminary transfer function protocol ===
           to find the fixed point (with possibility to add external drive)
        2)  =====> Full transfer function protocol ==== 
           i.e. scanning the (fe,fi) space and getting the output frequency""",
              formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("Neuron_Model",help="Choose a neuronal model from 'neuronal_models.py'")
    parser.add_argument("Network_Model",help="Choose a network model (synaptic and connectivity properties)"+\
                        "\n      from 'network_models'.py")

    parser.add_argument("--max_Fe",type=float, default=30.,\
                        help="Maximum excitatory frequency (default=30.)")
    parser.add_argument("--discret_Fe",type=int, default=10,\
                        help="Discretization of excitatory frequencies (default=9)")
    parser.add_argument("--lim_Fi", type=float, nargs=2, default=[0.,20.],\
                help="Limits for inhibitory frequency (default=[1.,20.])")
    parser.add_argument("--discret_Fi",type=int, default=8,\
               help="Discretization of inhibitory frequencies (default=8)")
    parser.add_argument("--max_Fout",type=float, default=30.,\
                         help="Minimum inhibitory frequency (default=30.)")
    parser.add_argument("--tstop",type=float, default=30.,\
                         help="tstop in s")
    parser.add_argument("--dt",type=float, default=5e-6,\
                         help="dt in ms")
    parser.add_argument("--SEED",type=int, default=1,\
                  help="Seed for random number generation (default=1)")

    parser.add_argument("-s", "--save", help="save with the right name",
                         action="store_true")
    
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                         action="store_true")

    args = parser.parse_args()

    import sys
    sys.path.append('../')
    from single_cell_models.cell_library import get_neuron_params
    from synapses_and_connectivity.syn_and_connec_library import get_connectivity_and_synapses_matrix
    
    params = get_neuron_params(args.Neuron_Model, SI_units=True)
    M = get_connectivity_and_synapses_matrix(args.Network_Model, SI_units=True)

    reformat_syn_parameters(params, M) # merging those parameters

    if args.save:
        FILE = 'data/'+args.Neuron_Model+'_'+args.Network_Model+'.npy'
    else:
        FILE = 'data/example_data.npy'
    
    
    
    #For the DB --max Fe=500 instead of 30 --discretFe= 100 instead of 10
    if args.save:
        FILE = 'data/'+args.Neuron_Model+'_'+args.Network_Model+'_DB.npy'
    else:
        FILE = 'data/example_data.npy'
    
    generate_transfer_function(params,\
                               verbose=True,
                               MAXfexc=args.max_Fe, 
                               MINfinh=args.lim_Fi[0], MAXfinh=args.lim_Fi[1],\
                               discret_exc=args.discret_Fe,discret_inh=args.discret_Fi,\
                               filename=FILE,
                               dt=args.dt, tstop=args.tstop,
                               MAXfout=args.max_Fout, SEED=args.SEED)

