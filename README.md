# enigma_anonymization
## Requires
Freesurfer <br>
https://surfer.nmr.mgh.harvard.edu/fswiki/rel7downloads <br>
-See below in install-

#
## Install
```
pip install git+https://github.com/nih-megcore/enigma_anonymization_lite
```
```
## Testing
```
Under Construction 
```

## Running
```
usage: process_anonymization_lite.py [-h] [-topdir TOPDIR]
                                [-csvfile CSVFILE] [-njobs NJOBS]
				[-linefreq LINEFREQ]

This function takes a csv file containing a list of datasets to
convert to BIDS format. A sample file (sample.csv) is distributed
with this package and contains the following fields:
subjid: 	This is the subject ID, will be appended with sub- in the BIDS output
full_mri_path: 	The full path to the T1 weighted MRI
full_meg_path: 	The full path to the raw MEG dataset
session:	Session, to permit multiple images per participant
trans_fname:	The full path to the .fif transform file

Upon execution, this function places the mri files into a staging directory, then does
basic freesurfer processing (not the full segmentation) to obtain a surface of the 
head and perform defacing. Next, the BIDS structure is created and populated
with the MRI and MEG data. Finally, a QA HTML report document is created, so that you
can easily view all the resultant MRI images to ensure that the anonymization
is adequate and that the coregistration is accurate.

optional arguments:
  -h, --help            show this help message and exit
  -topdir TOPDIR        The directory for the outputs
  -csvfile CSVFILE	The name of the CSV file described above
  -njobs NJOBS		Optional, number of jobs for Freesurfer processing
  -linefreq LINEFREQ	Optional, powerline frequency, defaults to 60s

```
