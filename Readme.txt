!/bin/sh

#  Script.sh
#  
#
#  Created by Matteo di Volo on 18/03/2018.
#

Related article: Carlu, Mallory, et al. "A mean-field approach to the dynamics of networks of complex neurons, from nonlinear Integrate-and-Fire to Hodgkin-Huxley models." Journal of Neurophysiology (2020) in press



Go to folder "network simulations"

#FIRST THE NETORK SIMULATION go to folder "network simulations"

python ntwk_sim_demo.py --CONFIG 'HH_RS--HH_FS--CONFIG1' --tstop 5000


#THEN PLOTTING THE RESULTS

python plot_single_sim.py




# SIMULATION OF THE MEAN FIELD, SPONTANEOUS ACTIVITY

python compare_with_mean_field.py --CONFIG 'HH_RS--HH_FS--CONFIG1' #(READ THE GOOD FILE)

# RESPONSE TO AN INPUT

python waveform_input.py  --CONFIG 'HH_RS--HH_FS--CONFIG1' -S #simulation of the network

python waveform_input.py  --CONFIG 'HH_RS--HH_FS--CONFIG1'  #corresponding mean field
















