# AstroCompute CASA Scripts
A collection of python scripts to create high time resolution light curves from calibrated interferometric data sets. These scripts run in the Common Astronomy Software Application (CASA; http://casa.nrao.edu) and have been tested with VLA, SMA and NOEMA data sets.

## Links for importing data into CASA
* VLA: Can be downloaded from archive in CASA format.
* SMA: Can be calibrated in CASA. Follow instructions at https://www.cfa.harvard.edu/sma/casa for reduction details and details on how to convert to a CASA MS data set for use by these scripts
* NOEMA: Must be calibrated beforehand. Follow instructions at http://www.iram.fr/IRAMFR/ARC/documents/filler/casa-gildas.pdf to convert to a CASA MS data set for use by these scripts.

##Description of scripts
1. **casa_timing_script.py**: intended to be run within CASA. This script does all the hard work.
   * All parameters need to be carefully considered and changed for each new data set.
   * If you have a complicated field with other sources it is recommended that you use your own mask file (with clean boxes     around bright sources; mask_option='file') for cleaning, or run object detection, which will create a mask file with a       boxed region around each detected source (mask_option='aegean').
   * Included in casa_timing_script.py is the option to run basic variability analysis:
      * Calculate weighted mean and do a chi^2 with a constant flux model,
      * Calculate excess variance (Vaughn et al. 2003; Bell et al., 2015),
      * Calculate fractional RMS (Vaughn et al. 2003; Bell et al., 2015), and
      * Make power spectrum using generalized lomb-periodogram (Zechmeister and Kurster, 2009); implemented with
       the astroML package.
2. **Aegean_ObjDet.py**: detects objects in a fits image.
   * Is integrated into casa_timing_script.py, but can be run on its own too.
   * Data file of detected object properties is output.
   * Detected object positions are printed to terminal too
3. **utils.py**: module of tools used in casa_timing_script.py.
4. **download_data_AWS.py**: downloads data from an AWS bucket.
5. **upload_data_AWS.py**: uploads data to an AWS bucket.
6. **remove_bucket_AWS.py**: removes a bucket from AWS.
7. **sim.py**: creates a simulated CASA MS of time-variable source for testing using CASA's simulation toolbox.

###User Parameters
* All input parameters are set in the parameter file (param.txt)
* A complete description of each parameter is provided in param_description.txt.

####
Support from the SKA/AWS AstroCompute Program
