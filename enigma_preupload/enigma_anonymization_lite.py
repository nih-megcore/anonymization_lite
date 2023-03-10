#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 09:28:56 2022

@author: nugenta
"""

import pandas as pd 
import os, os.path as op 
import logging
import argparse

import matplotlib
matplotlib.use('Qt5agg'); 

logger = logging.getLogger()
os.environ['MNE_3D_OPTION_ANTIALIAS']='false'

from enigma_preupload.enigma_anonymization_lite_functions import initialize, stage_mris, parallel_make_scalp_surfaces, process_meg_bids, process_mri_bids, loop_QA_report

if __name__=='__main__':

    # parse the arguments and initialize variables   

    parser = argparse.ArgumentParser()
    parser.add_argument('-topdir', help='''The base directory for outputs, defaults to current directory''')
    parser.add_argument('-csvfile', help='''The name of the csv file with paths and filenames''')
    parser.add_argument('-njobs',help='''The number of jobs for parallel processing, defaults to one''', type=int)
    parser.add_argument('-linefreq',help='''The linefrequency for the country of data collection''', type=int)
    parser.description='''This python script implements anonymization and BIDSification of a dataset. We hope you enjoy using it as much as we enjoyed making it.'''
    
    args = parser.parse_args()
    
    if not args.njobs:
        njobs=1
    else:
        njobs=args.njobs
                   
    if args.topdir:
        topdir=args.topdir
    else:
        topdir=os.getcwd()
        
    if not args.csvfile:
        print('''-csvfile is a required argument''')
        raise ValueError
    else:
        csvfile=args.csvfile
        csvpath = op.join(topdir, csvfile)
        
    if not args.linefreq:
        print('''setting linefreq to 60, hope that's okay!''')
        linefreq=60
    else:
        linefreq=args.linefreq
        
    initialize(topdir=topdir)
    subjects_dir = op.join(topdir,'SUBJECTS_DIR')

    # read the csv file containing all the path information and check to see that all the required columns are present

    dframe=pd.read_csv(csvpath)
    if not set(['bids_subjid','full_mri_path','full_meg_path','session','trans_fname']).issubset(dframe.columns):
        print('csvfile does not have all required elements - must contain: bids_subjid, full_mri_path, full_meg_path, session, trans_fname')
        print('There is an additional optional column empty_room')
        raise ValueError
        
    if not set(['empty_room']).issubset(dframe.columns):
        print('no empty room datasets detected in input csv datafile. If this is not correct check column namesj')
    
    # stage the mris into the staging directory
    
    mri_frame = stage_mris(topdir, dframe)
    
    # do the basic freesurfer processing to deface the data
    
    parallel_make_scalp_surfaces(dframe=mri_frame, topdir=topdir, subjdir=subjects_dir, njobs=njobs)
    
    # create the BIDS structure for the MRI scans
    
    process_mri_bids(dframe=dframe, topdir=topdir)
    
    # create the BIDS structure for the MEG scans - if there's an empty room dataset, do that one first
    
    process_meg_bids(dframe=dframe, topdir=topdir, linefreq=60)
    
    # make the QA report document
    
    loop_QA_report(dframe, subjects_dir=subjects_dir, topdir=topdir)
    