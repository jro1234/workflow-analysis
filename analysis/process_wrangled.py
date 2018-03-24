
import radical.utils     as ru
import radical.pilot     as rp
import radical.analytics as ra
from   radical.utils.profile import *
from   radical.pilot.states  import *

#import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import glob
import os

from analysis.notebook_utils import *



UNIT_DURATIONS = {
        'exec-tot' : [{STATE: AGENT_EXECUTING,              EVENT: 'state'        },
                      {STATE: AGENT_STAGING_OUTPUT_PENDING, EVENT: 'state'        }],
        'exec-rp'  : [{STATE: None,                         EVENT: 'exec_start'   },
                      {STATE: None,                         EVENT: 'exec_stop'    }],
        'exec-cu'  : [{STATE: None,                         EVENT: 'cu_start'     },
                      {STATE: None,                         EVENT: 'cu_exec_stop' }],
        'exec-orte': [{STATE: None,                         EVENT: 'cu_exec_start'},
                      {STATE: None,                         EVENT: 'cu_exec_stop' }],
        'exec-app' : [{STATE: None,                         EVENT: 'app_start'    },
                      {STATE: None,                         EVENT: 'app_stop'     }]}


data = dict()
for dname in UNIT_DURATIONS:
    data[dname]  = list()


nm_run = 'testrun'
d_run  = 'rawdata/{}'.format(nm_run)

f_run  = 'rp.session.titan-ext1.jrossyra.017614.0002'
#f_run  = 'rp.session.titan-ext1.jrossyra.017614.0003'

a_run = os.path.join(d_run, f_run)
#a_run  = max(glob.glob(
#    os.path.join(d_run, 'rp.session.*')),
#    key=os.path.getctime)

session = ra.Session(a_run, 'radical.pilot')

# Load wrangled data saved in .csv files for both synapse, microbenchmarks and gromacs.
sws_sessions = pd.read_csv(os.path.join(a_run,'sessions.csv'), index_col=0)
sws_pilots   = pd.read_csv(os.path.join(a_run,'pilots.csv'),   index_col=0)
sws_units    = pd.read_csv(os.path.join(a_run,'units.csv'),    index_col=0)

print 'Total number of successful runs: %s' % sws_sessions.shape[0]
print 'Total number of pilots: %s'          % sws_pilots.shape[0]
print 'Total number of units: %s\n'         % sws_units.shape[0]


units   = session.filter(etype='unit', inplace=True)
for unit in units.get():
    print "In unit", unit
    for dname in UNIT_DURATIONS:
        print "Get Duration", dname
        try:
            dur = unit.duration(event=UNIT_DURATIONS[dname])
    #    if dur > 1000.0:
    #        ocnt += 1
    #        fout.write('%10.1f  %s\n' % (dur, src))
    #        fout.flush()
#   #          sys.stdout.write('#')
    #    else:
    #        ucnt += 1
    #        data[dname].append(dur)
            data[dname].append(dur)
            print dname, dur
        except:
            print " -- This one didn't work"


# The duration measure to plot
cu_duration = 'exec-tot'
n_bins = 3
#fig, ax = fig_setup(figsize=(13,4))
fig, ax = plt.subplots(figsize=(13,4))
data_mean = np.mean(data[cu_duration])
data_sigma = np.sqrt(np.var(data[cu_duration]))
ax.hist(data[cu_duration], bins=n_bins, color=tableau20[9])#, histtype='step')
ax.axvline(x=data_mean, color='black', linestyle='dashed')
ax.axvspan(data_mean-data_sigma, data_mean+data_sigma, alpha=0.25, color=tableau20[9])
ax.set_xlabel('Runtime (s)')
ax.set_ylabel('Number of Tasks')
ax.legend(['Mean $T_x$ (%ss)' %  round(data_mean, 2), 
           '$\sigma$ (%s)'    % round(data_sigma, 2), 
           '$T_x$'])
plt.savefig('cu_duration_distribution.{}.pdf'.format(cu_duration), dpi=300, bbox_inches='tight')
plt.savefig('cu_duration_distribution.{}.png'.format(cu_duration))
