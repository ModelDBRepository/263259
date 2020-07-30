
import numpy as np
import matplotlib.pylab as plt
import math
from scipy import fftpack

def bin_array(array, BIN, time_array):
    N0 = int(BIN/(time_array[1]-time_array[0]))
    N1 = int((time_array[-1]-time_array[0])/BIN)
    return array[:N0*N1].reshape((N1,N0)).mean(axis=1)



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

    parser.add_argument("-f", "--file",help="filename", default='data/example.npy')
    parser.add_argument("-z", "--zoom",help="zoom for activity", type=float, nargs=2)
    parser.add_argument("-b", "--bar_ms",help="bar for legend", type=int, default=100)
    parser.add_argument("-r", "--raster_number",help="max neuron number", type=int, default=10000)
    parser.add_argument("-s", "--save",action='store_true')

    args = parser.parse_args()
    
    time_array, rate_array, rate_exc, rate_inh,\
        Raster_exc, Raster_inh, Vm_exc, Vm_inh,\
        Ge_exc, Ge_inh, Gi_exc, Gi_inh = np.load(args.file,allow_pickle = True)
    
    
    plt.plot(Raster_exc[0], Raster_exc[1], '.g',ms=2)

    plt.plot(Raster_inh[0], Raster_inh[1], '.r', ms=2)
    plt.show()

    #plt.plot(time_array,Vm_exc[4,:])
    #plt.show()

    BIN=5
    tbinned,rebinned,ribibbed=bin_array(time_array, BIN, time_array),bin_array(rate_exc, BIN, time_array),bin_array(rate_inh, BIN, time_array)


    plt.plot(tbinned,rebinned,'g-',tbinned,ribibbed,'r')
    plt.show()


    sampling_frequency=1000./(1.*BIN)
    fftsig=fftpack.rfft(rebinned)
    #frequency=np.arange(len(fftsig))/len(fftsig)*sampling_frequency/2.
    todivide=len(fftsig)/sampling_frequency
    frequency=np.arange(len(fftsig))/(2.*todivide)
 
    plt.plot(frequency,np.abs(fftsig))
    plt.show()




    #calculate CV


    Ne=8000
    Ni=2000
    isi=np.zeros(Ne)
    isiav=np.zeros(Ne)
    told=np.zeros(Ne)
    isisq=np.zeros(Ne)
    cvv=np.zeros(Ne)
    spikenumber=np.zeros(Ne)
    indexA=np.linspace(0,8000,8000)






    for i in range(len(Raster_exc[0,:])):

        timepoint=Raster_exc[0,i]
        neuronindex=int(Raster_exc[1,i])
        timepointold=told[neuronindex]


        isi[neuronindex]=timepoint-timepointold


        if(spikenumber[neuronindex]>0):
            isiav[neuronindex]+=isi[neuronindex]
            isisq[neuronindex]+=isi[neuronindex]*isi[neuronindex]
        
        
        
        spikenumber[neuronindex]+=1
        
        told[neuronindex]=timepoint




    for i in range(len(isiav)):
        if(spikenumber[i]-1>10):
           
            auxil=math.sqrt(-((isiav[i]/(spikenumber[i]-1))*(isiav[i]/(spikenumber[i]-1))-(isisq[i]/(spikenumber[i]-1))))
            isiav[i]=isiav[i]/(spikenumber[i]-1)
            cvv[i]=auxil/isiav[i]
        else:
            cvv[i]=0
            isiav[i]=0
                



    plt.plot(indexA,isiav,'o')
    plt.show()

    plt.plot(indexA,cvv,'o')
    plt.show()



    #second way
    for i in range(len(isiav)):
    
        isiaux=Raster_exc[0][np.where((Raster_exc[1]>i-0.5) & (Raster_exc[1]<i+0.5)  )]
        
        
        print("isiaux",i,isiaux[:1])


        


        
