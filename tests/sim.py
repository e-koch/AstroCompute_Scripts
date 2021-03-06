
import sys
from os.path import join as osjoin
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii
from astropy.table import Table, Column, MaskedColumn
from astropy import units as u
from astropy.time import Time

from tasks import clean, concat

'''
simulate CASA timing test dataset

Call as: casa -c sim.py OUTPUT_PATH PATH_TO_CASA

'''

# p
# User input
####################
# path_dir = '/mnt/bigdata/tetarenk/timing_test'
path_dir = sys.argv[-2]
casa_path = sys.argv[-1]

# flux model vs time
integ = 10.
total_time = 10. * 60.
num_points = total_time / integ
time_bins = np.arange(integ, total_time + integ, integ)  # end of bins
noise = np.random.randn(len(time_bins))
fluxarray = 5. * np.sin((2 * np.pi / 160) * time_bins) + 10 + noise * 0.5
plt.plot(time_bins, fluxarray, marker='o', ls='')

# array config
# MAC:configf='/Applications/CASA-4.6.app/Contents/data/alma/simmos/vla.c.cfg'
# configf = '/usr/local/bin/CASA-4.6/casa-release-4.6.0-el6/data/alma/simmos/vla.c.cfg'
configf = osjoin(casa_path, 'data/alma/simmos/vla.c.cfg')
data = ascii.read(configf, data_start=1,
                  names=['X', 'Y', 'Z', 'DIAM', 'ANT'], guess=True)
xx = data['X']
yy = data['Y']
zz = data['Z']
diam = data['DIAM']

# src info
loca = "J2000 10h00m00.00s -30d00m00.0s"
hrsref = loca.split(' ')[1].split('h')[0] + 'h'
minref = loca.split(' ')[2].split('d')[0] + 'deg'
freq = '5GHz'
mj = "0.5arcsec"
ma = '0.1arcsec'
pa = '45.0deg'
imsize = 256
cellsize = '0.3arcsec'
starttime = '2017/02/10/07:00:02.00'
####################

# makes an MS for each time bin with a point source of flux equal to
# fluxarray for that time bin
mslist = []
for i in range(0, len(time_bins)):
    # make point source model image for each time bin
    cl.done()
    cl.addcomponent(dir=loca,
                    flux=fluxarray[i], fluxunit='Jy', freq=freq, shape="Gaussian",
                    majoraxis=mj, minoraxis=ma, positionangle=pa)
    ia.fromshape(path_dir + "Gaussian.im",
                 [imsize, imsize, 1, 1], overwrite=True)
    cs = ia.coordsys()
    cs.setunits(['rad', 'rad', '', 'Hz'])
    cell_rad = qa.convert(qa.quantity(cellsize), "rad")['value']
    cs.setincrement([-cell_rad, cell_rad], 'direction')
    cs.setreferencevalue([qa.convert(hrsref, 'rad')['value'], qa.convert(
        minref, 'rad')['value']], type="direction")
    cs.setreferencevalue(freq, 'spectral')
    cs.setincrement('1GHz', 'spectral')
    ia.setcoordsys(cs.torecord())
    ia.setbrightnessunit("Jy/pixel")
    ia.modify(cl.torecord(), subtract=False)

    # make simulated MS for each time bin
    os.system('rm -rf ' + path_dir + 'testsrc' + str(i) + '.ms')
    sm.open(path_dir + 'testsrc' + str(i) + '.ms')
    mslist.append(path_dir + 'testsrc' + str(i) + '.ms')
    posvla = me.observatory('vla')
    sm.setconfig(telescopename='VLA', x=xx, y=yy, z=zz, dishdiameter=diam, mount='alt-az',
                 antname='VLA', coordsystem='local', referencelocation=posvla)
    sm.setspwindow(spwname='band', freq=freq, deltafreq='50MHz', freqresolution='50MHz', nchannels=128,
                   stokes='RR RL LR LL')
    sm.setfield(sourcename='MyPointSrc', sourcedirection=loca.split(' '))
    #sm.setlimits(shadowlimit=0.001, elevationlimit='8.0deg')
    sm.setauto(autocorrwt=0.0)
    sm.settimes(integrationtime=integ, usehourangle=F,
                referencetime=me.epoch('utc', starttime))
    sm.observe('MyPointSrc', 'band',
               starttime=str(int(time_bins[i] - integ)) + 's', stoptime=str(int(time_bins[i])) + 's')
    sm.setdata(spwid=0, fieldid=0)
    sm.predict(imagename=path_dir + 'Gaussian.im')
    sm.setnoise(mode='tsys-atm', pwv='4mm')
    sm.close()
    print 'Done ', i, ' of ', len(time_bins), '.'

# concat all time bin MSs
concat(mslist, concatvis=osjoin(path_dir, 'testconcat.ms'))

# check output and clean to make sure everything works!
# os.system('rm -rf ' + path_dir + 'testsrc*.ms')

# listobs(path_dir + 'testconcat.ms', listfile=path_dir + 'listobs.txt')
# os.system('pluma ' + path_dir + 'listobs.txt &')

# plotms(vis=path_dir + 'testconcat.ms', xaxis="time", yaxis="amp",
#        coloraxis="field", iteraxis="antenna", avgtime='60s')

# clean(vis=path_dir + 'testconcat.ms', imagename=path_dir + 'whole_dataset', field='', mode='mfs',
#       imsize=imsize, cell=cellsize, weighting='natural', spw='', nterms=1,
#       niter=0, gain=0.1, threshold='100mJy', interactive=T)

# imview(path_dir + 'whole_dataset.image')

# exportfits(imagename=path_dir + 'whole_dataset.image',
#            fitsimage=path_dir + 'whole_dataset.fits')
