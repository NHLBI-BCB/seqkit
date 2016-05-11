#!/usr/bin/env python
""" Methods and functionalites to perform peak-calling """
import os
import pdb
from glob import glob
from seqkit import CONFIG as conf
from seqkit.utils.find_samples import find_samples


def run_peakcall(project,peak_call):
	""" Will run the preffered peak-calling software """
	root_dir = conf.get('root_dir','')
	proj_dir = os.path.join (root_dir,project)
	if peak_call == "macs2":
		load_module = ('module load MACS/2.1.0\n')
		macs2_cmd = ('macs2 callpeak -t ${treatment} -c ${control} -n ${name} -g mm -f BED -p 0.001 -m 10 30\n')
		template = ('#!/bin/bash -l\n'
                           '#SBATCH -A b2012025\n'
                           '#SBATCH -J {}_peakcall\n'
                           '#SBATCH -p core -n 2 \n'
                           '#SBATCH -t 10:00:00\n'
                           '#SBATCH --mail-type=FAIL\n'
                           '#SBATCH --mail-user=\'ashwini.jeggari@scilifelab.se\'\n\n'
                           'module load bioinfo-tools\n'
			   ''+load_module''
			   ''+macs2_cmd+''
			)
	