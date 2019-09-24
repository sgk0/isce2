#!/usr/bin/env python3
#
# Author: Piyush Agram
# Copyright 2016
#

from .runTopo import filenameWithLooks
import os

def runNormalize(self, normalize=True):
    '''
    Make sure that a DEM is available for processing the given data.
    '''
    if not normalize:
        return

    refPol = self._grd.polarizations[0]
    master = self._grd.loadProduct( os.path.join(self._grd.outputFolder, 'beta_{0}.xml'.format(refPol)))

    azlooks, rglooks = self._grd.getLooks( self.posting, master.groundRangePixelSize, master.azimuthPixelSize, self.numberAzimuthLooks, self.numberRangeLooks)

    outname = os.path.join(self._grd.outputFolder, self._grd.gamma0FileName)
    incname = os.path.join(self._grd.geometryFolder, self._grd.incFileName)
    maskname = os.path.join(self._grd.geometryFolder, self._grd.slMaskFileName)

    for pol in self._grd.polarizations:
        cmd = "imageMath.py --e='a*cos(b_0*PI/180.)/cos(b_1*PI/180.) * (c==0)' --a={beta} --b={inc} --c={mask} -o {out} -t FLOAT -s BIL" 

        spl = os.path.splitext(outname)
        outpolname = spl[0] + '_' + pol +  spl[1]
        if (azlooks != 1) or (rglooks != 1):
            outpolname = filenameWithLooks(outpolname, azlooks, rglooks)

        betaname = os.path.join( self._grd.outputFolder, 'beta_{0}.img'.format(pol))
        if (azlooks != 1) or (rglooks != 1):
            betaname = filenameWithLooks(betaname, azlooks, rglooks)

        cmdrun = cmd.format(inc = incname,
                            beta = betaname,
                            out = outpolname,
                            mask = maskname)

        status = os.system(cmdrun)

        if status:
            raise Exception('{0} Failed.'.format(cmdrun))
