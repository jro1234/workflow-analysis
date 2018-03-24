

import radical.analytics as ra
import radical.pilot as rp
import pprint
import radical.utils as ru
import os 
import glob
import numpy as np


nm_run = 'testrun'
d_run  = 'rawdata/{}'.format(nm_run)

newest  = max(glob.glob(
    os.path.join(d_run, 'rp.session.*')),
    key=os.path.getctime)

session = ra.Session(newest, 'radical.pilot')

import pprint

entities_objects = session.get()
pprint.pprint(entities_objects)

state_models = session.describe('state_model')
pprint.pprint(state_models)
state_model = session.describe('state_model', etype='unit')
pprint.pprint(state_model)
state_models = session.describe('state_model', etype=['unit', 'pilot'])
pprint.pprint(state_models)
event_models = session.describe('event_model')
pprint.pprint(event_models)
relations = session.describe('relations')
pprint.pprint(relations)

unit = session.get(etype='unit')
uids=[]
for i in range(len(unit)):
  uids.append(unit[i].uid)

u=unit[0]
ostates=sorted(u.states.items(), key=lambda s: s[1][0])
pprint.pprint(ostates)

args=np.argsort(uids)

iter_cuts=[]
for i in args:
    if 'post_analyze.py' in str(unit[i].description):
        print('iter_cut', str(unit[i].description).split("iter_")[1][0],
              unit[i].uid, unit[i].duration(event=[{ru.EVENT: 'exec_start'},
              {ru.EVENT: 'exec_stop'}])
             )
        iter_cuts.append(unit[i].uid)

