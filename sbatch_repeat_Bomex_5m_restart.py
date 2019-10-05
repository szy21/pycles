#import netCDF4 as nc
import numpy as np
import json
import time
import os
import sys
import glob

simname = 'Bomex_5m_restart'
restart_count = '.Restart_0'

input_file = '/home/zhaoyi/pycles/'+simname+'.in'
with open(input_file) as f:
    namelist = json.load(f)
restart_path = namelist['restart']['input_path']
restart_path_org = restart_path+'_original'

stats_root = namelist['output']['output_root']+'Output.'+namelist['meta']['simname']+'.'+namelist['meta']['uuid'][-5:]+'/'+'stats/'
stats_path = stats_root+'Stats.'+namelist['meta']['simname']+restart_count+'.nc'
print restart_path_org
print restart_path
print stats_path

script_name = '/home/zhaoyi/pycles/'+'run_'+simname+'.sh'
state_file = '/home/zhaoyi/pycles/'+simname+'.out'
tail_output = '/home/zhaoyi/pycles/'+'tmp_'+simname+'.out'

if os.path.exists(stats_path):
    print stats_path+ ' exists!'
    sys.exit()

count = 0
count_max = 30

while True:
    flag = False
    if os.path.exists(state_file):
        with open(state_file,'r') as f:
            last_line = f.readlines()[-1]
        if 'slurm' in last_line:
            slurm_output = '/home/zhaoyi/pycles/'+last_line[:-1]
            cmd = 'tail -10 '+slurm_output+'>'+tail_output
            print cmd
            returned_value = os.system(cmd)
            print returned_value
            if 'Killed' in open(tail_output,'r').read():
                with open(state_file,'a') as f:
                    f.write('check\n')
                flag = True
            elif 'nan' in open(tail_output,'r').read():
                with open(state_file,'a') as f:
                    f.write('check\n')
                    f.write('Found NaN\n')
                flag = True
                cmd = 'scancel '+last_line[6:-5]
                print cmd
                returned_value = os.system(cmd)
                print returned_value
                break
            elif 'walltime' in open(tail_output,'r').read():
                flag = False
                with open(state_file,'a') as f:
                    f.write('check\n')
                    f.write('This simulation runs smoothly!\n')
                break
            if count>=count_max:
                with open(state_file,'a') as f:
                    f.write('Last try!\n')
            
    if count==0 or flag:
        if os.path.exists(restart_path_org):
            cmd = 'mv '+restart_path_org+'/ '+restart_path
            print cmd
            returned_value = os.system(cmd)
            print returned_value
        if os.path.exists(stats_path):
            cmd = 'rm -f '+stats_path
            print cmd
            returned_value = os.system(cmd)
            print returned_value
        if count>=count_max:
            print 'Tried '+str(count)+' times!'
            break 
        cmd = 'sbatch '+script_name 
        returned_value = -1
        returned_value = os.system(cmd)
        print cmd+' returned_value: ', returned_value
        count+=1

    time.sleep(1200)
