﻿from os.path import join, isdir, basename
from os import walk, makedirs, system
import sys
from mavr.processing import get_ps
from time import time
from numpy import mean

def scan_year(params, parent = None, level = 0):
    sets = list(walk(params['input']['year']))[0][1]
        
    for month in sets:
        params['input']['set'] = join(params['input']['year'], month)
        params['output']['set'] = join(params['output']['year'], month)
        print('\t'*level + params['input']['set'])
        scan_set(params, parent, level+1)
        
def scan_set(params, parent = None, level = 0):
    if isdir(join(params['input']['set'], 'cut')):
        params['input']['subdir'] = join(params['input']['set'], 'cut')
    elif isdir(join(params['input']['set'], 'rebuild')):
        params['input']['subdir'] = join(params['input']['set'], 'rebuild')
    elif isdir(join(params['input']['set'], 'rebuilded')):
        params['input']['subdir'] = join(params['input']['set'], 'rebuilded')
    else:
        print('Error')
        return 1
    nights = list(walk(params['input']['subdir']))[0][1]
    for night in nights:
        params['input']['night'] = join(params['input']['subdir'], night)
        params['output']['night'] = join(params['output']['set'], night)
        print('\t'*level + params['input']['night'])        
        scan_night(params, parent)
        
def scan_night(params, parent = False, level = 0):
    stars = []
    try:
        makedirs(params['output']['night'])
    except:
        pass
    for root, dirs, files in walk(params['input']['night']):
        for name in files:
            if not name.endswith('.dat') or name.startswith('dark') or name.startswith('flat') or 'moon' in name or 'bin' in name:
                continue
            else:
                stars.append(join(root, name))
        break
    for star in stars:
        print('\t'*level + star)                
        get_ps(star, diff=params['diff'], acf=params['acf'], save=params['save'], shape=params['shape'], output=params['output']['night'], rmbgr_on=params['rmbgr'])
        