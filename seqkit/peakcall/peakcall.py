#!/usr/bin/env python
""" Methods and functionalites to perform peak-calling """
import os
import pdb
from glob import glob
from seqkit import CONFIG as conf
from seqkit.utils.find_samples import find_samples


def run_peakcall(project, input_file, mode, peak_call):
    """ Will run the preffered peak-calling software """
    root_dir = conf.get('root_dir','')  
    proj_dir = os.path.join (root_dir,project)
    load_module = ('module load MACS/2.1.0\n')
    sbatch_template = ('#!/bin/bash -l\n'
                       '#SBATCH -A b2012025\n'
                       '#SBATCH -J {name}_peakcall\n'
                       '#SBATCH -p core -n 1 \n'
                       '#SBATCH -t 5:00:00\n'
                       '#SBATCH --mail-type=FAIL\n'
                       '#SBATCH --mail-user=\'ashwini.jeggari@scilifelab.se\'\n\n'
                       'module load bioinfo-tools\n'
                        )
    if mode == "TF":
        if peak_call == "macs2":
            macs2_cmd = conf.get('macs2_TF','')
            template = ('## Running Peak-calling for TF-ChIP data\n'
                        ''+load_module+''
                        'cd {peaks_dir}\n'
			''+macs2_cmd+''
		        )
        else:
            raise SystemExit("Please mention the type of peak caller - macs2")
    elif mode == "HM":   
        if peak_call == "macs2":
            macs2_cmd = conf.get('macs2_HM','')
            template = ('# Running macs2 peak-calling for HM data\n'
                        ''+load_module+''
                        ''+macs2_cmd+'')
    
        elif peak_call == "danpos2":
            danpos_path = "export danpos2 path"
            danpos_cmd = ('python danpos.py dpeak ${treatment} -b ${control}')
            template = ('# Running danpos2 peakcalling for HM data\n'
                        ''+danpos_cmd+'')
        else:
            raise SystemExit("Please mention the type of peak_Caller (macs2/danpos2)")
    else:
        raise SystemExit("Please mention the type of mode - either TF or HM")

        
    pk_file = open(input_file,'r')
    pk_file.next()
    for ln in iter(pk_file):	
        ln = ln.strip()
        ln =  ln.split('\t')
        treat = ln[0]
        ctrl = ln[1]
        name = "{}_Vs_{}".format(treat,ctrl)
	treat_fl = ''.join(glob("{}/{}/alignment_*/bedfiles/{}*uniq.bed".format(proj_dir,treat,treat)))
	control_fl = ''.join(glob("{}/{}/alignment*/bedfiles/{}.*uniq.bed".format(proj_dir,treat,treat)))
        peaks_dir = os.path.join(proj_dir,treat,"{}_{}".format(peak_call,mode))
        if not peaks_dir:
            os.mkdir(peaks_dir)
        jb_fl = os.path.join(proj_dir,treat,"scripts","{}_peakcall.sh".format(name))
        template_pc = sbatch_template + template
        with open(jb_fl,'w') as jb_fl:
            jb_fl.write(template_pc.format(name=name, treatment=treat_fl, control=control_fl,peaks_dir=peaks_dir))
