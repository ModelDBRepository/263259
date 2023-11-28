"""
Some configuration of neuronal properties so that we pick up
within this file
"""
from __future__ import print_function

def get_neuron_params(NAME, name='', number=1, SI_units=False):

    if NAME=='HH_FS':
        params = {'name':name, 'N':number,\
                'Gl':10.,'GNa':20000.,'GK':6000,'GM':0.,  'Cm':200.,'Trefrac':5.,\
                'El':-65.,'EK':-90.,'ENa':50., 'Vthre':-40., 'Vreset':-60., 'VT':-53.5, 'delta_v':0.,'hhtype':1,'hhtype':1,\
                'a':0., 'b': 0., 'tauw':1e9}


    elif NAME=='HH_RS':
        params = {'name':name, 'N':number,\
                'Gl':10.,'GNa':20000.,'GK':6000,'GM':30.,  'Cm':200.,'Trefrac':5.,\
                'El':-65.,'EK':-90.,'ENa':50., 'Vthre':-40., 'Vreset':-60., 'VT':-53.5, 'delta_v':0.,'hhtype':1,\
                'a':0., 'b': 0., 'tauw':1e9}


    elif NAME=='HH_RS_DB':
        params = {'name':name, 'N':number,\
                'Gl':10.,'GNa':20000.,'GK':6000,'GM':30.,  'Cm':200.,'Trefrac':5.,\
                'El':-65.,'EK':-90.,'ENa':50., 'Vthre':-40., 'Vreset':-60., 'VT':-53.5, 'delta_v':0.,'hhtype':1,\
                'a':0., 'b': 0., 'tauw':1e9}


    elif NAME=='HH_RS_A':
        params = {'name':name, 'N':number,\
            'Gl':10.,'GNa':20000.,'GK':6000,'GM':30.,  'Cm':50.,'Trefrac':5.,\
            'El':-65.,'EK':-90.,'ENa':50., 'Vthre':-40., 'Vreset':-60., 'VT':-53.5, 'delta_v':0.,'hhtype':1,\
                'a':0., 'b': 0., 'tauw':1e9}

    elif NAME=='HH_RS_noAd':
        params = {'name':name, 'N':number,\
                'Gl':20.,'GNa':20000.,'GK':6000,'GM':0.,  'Cm':200.,'Trefrac':5.,\
                'El':-65.,'EK':-90.,'ENa':50., 'Vthre':-40., 'Vreset':-60., 'VT':-53.5, 'delta_v':0.,'hhtype':1,\
                'a':0., 'b': 0., 'tauw':1e9}


    elif NAME=='HH_RS1':
        params = {'name':name, 'N':number,\
                'Gl':10.,'GNa':20000.,'GK':6000,'GM':80.,  'Cm':200.,'Trefrac':5.,\
                'El':-65.,'EK':-90.,'ENa':50., 'Vthre':-40., 'Vreset':-60., 'VT':-53.5, 'delta_v':0.,'hhtype':1,\
                'a':0., 'b': 0., 'tauw':1e9}


    elif NAME=='HH_RS2':
        params = {'name':name, 'N':number,\
                'Gl':10.,'GNa':20000.,'GK':6000,'GM':15.,  'Cm':200.,'Trefrac':5.,\
                'El':-65.,'EK':-90.,'ENa':50., 'Vthre':-40., 'Vreset':-60., 'VT':-53.5, 'delta_v':0.,'hhtype':1,\
                'a':0., 'b': 0., 'tauw':1e9}

    else:
        print('====================================================')
        print('------------ CELL NOT RECOGNIZED !! ---------------')
        print('====================================================')


    if SI_units:
        print('cell parameters in SI units')
        # mV to V
        params['El'], params['Vthre'], params['Vreset'], params['delta_v'] =\
            1e-3*params['El'], 1e-3*params['Vthre'], 1e-3*params['Vreset'], 1e-3*params['delta_v']
        # ms to s
        params['Trefrac'], params['tauw'] = 1e-3*params['Trefrac'], 1e-3*params['tauw']
        # nS to S
        #params['a'], params['Gl'],params['GNa'],params['GK'] = 1e-9*params['a'], 1e-9*params['Gl'],1e-9*params['GNa'],1e-9*params['GK']
        params['a'], params['Gl']= 1e-9*params['a'], 1e-9*params['Gl']
        # pF to F and pA to A
        params['Cm'], params['b'] = 1e-12*params['Cm'], 1e-12*params['b']

        if(params['hhtype']>0):
            params['GNa'],params['GK'],params['GM'] = 1e-9*params['GNa'],1e-9*params['GK'],1e-9*params['GM']
            params['VT'],params['ENa'],params['EK'] =1e-3*params['VT'],1e-3*params['ENa'],1e-3*params['EK']
    else:
        print('cell parameters --NOT-- in SI units')
        
    return params.copy()

if __name__=='__main__':

    print(__doc__)
