#!/usr/bin/env python3

"""
Geoscience Australia - Python Geodesy Package
Constants Module
"""

from math import sqrt
from datetime import date

c_vac = 299792.458
k_0 = 0.9996


# Ellipsoid Constants
class Ellipsoid(object):
    def __init__(self, semimaj, inversef):
        self.semimaj = semimaj
        self.inversef = inversef
        self.f = 1 / self.inversef
        self.semimin = float(self.semimaj * (1 - self.f))
        self.ecc1sq = float(self.f * (2 - self.f))
        self.ecc2sq = float(self.ecc1sq / (1 - self.ecc1sq))
        self.ecc1 = sqrt(self.ecc1sq)
        self.n = float(self.f / (2 - self.f))
        self.n2 = self.n ** 2
        self.meanradius = (2 * self.semimaj + self.semimin)/3


# Geodetic Reference System 1980 (http://www.epsg-registry.org/export.htm?gml=urn:ogc:def:ellipsoid:EPSG::7019)
grs80 = Ellipsoid(6378137, 298.257222101)

# World Geodetic System 1984 (http://www.epsg-registry.org/export.htm?gml=urn:ogc:def:ellipsoid:EPSG::7030)
wgs84 = Ellipsoid(6378137, 298.257223563)

# Australian National Spheroid (http://www.epsg-registry.org/export.htm?gml=urn:ogc:def:ellipsoid:EPSG::7003)
ans = Ellipsoid(6378160, 298.25)

# International (Hayford) 1924 (http://www.epsg-registry.org/export.htm?gml=urn:ogc:def:ellipsoid:EPSG::7022)
intl24 = Ellipsoid(6378388, 297)


# Projections
class Projection(object):
    def __init__(self, falseeast, falsenorth, cmscale, zonewidth, initialcm):
        self.falseeast = falseeast
        self.falsenorth = falsenorth
        self.cmscale = cmscale
        self.zonewidth = zonewidth
        self.initialcm = initialcm


utm = Projection(500000, 10000000, 0.9996, 6, -177)


# Helmert 14 Parameter Transformation Parameters
class Transformation(object):
    def __init__(self, from_datum, to_datum, ref_epoch,
                 tx, ty, tz, sc, rx, ry, rz,
                 d_tx=0.0, d_ty=0.0, d_tz=0.0, d_sc=0.0, d_rx=0.0, d_ry=0.0, d_rz=0.0):
        self.from_datum = from_datum    # Datum Transforming From
        self.to_datum = to_datum        # Datum Transforming To
        self.ref_epoch = ref_epoch      # Reference Epoch (datetime.date Object)
        self.tx = tx                    # Translation in x (m)
        self.ty = ty                    # Translation in y (m)
        self.tz = tz                    # Translation in z (m)
        self.sc = sc                    # Scale Change (parts per million)
        self.rx = rx                    # Rotation about x (arcseconds)
        self.ry = ry                    # Rotation about y (arcseconds)
        self.rz = rz                    # Rotation about z (arcseconds)
        self.d_tx = d_tx                # Rate of change in Translation in x (m per year)
        self.d_ty = d_ty                # Rate of change in Translation in y (m per year)
        self.d_tz = d_tz                # Rate of change in Translation in z (m per year)
        self.d_sc = d_sc                # Rate of change in Scale Change (parts per million per year)
        self.d_rx = d_rx                # Rate of change in Rotation about x (arcseconds per year)
        self.d_ry = d_ry                # Rate of change in Rotation about y (arcseconds per year)
        self.d_rz = d_rz                # Rate of change in Rotation about z (arcseconds per year)

    def __repr__(self):
        return ('Transformation: '
                + 'From ' + repr(self.from_datum) + ' to ' + repr(self.to_datum) + '\n'
                + 'Reference Epoch: ' + repr(self.ref_epoch) + '\n'
                + '  tx: ' + repr(self.tx) + 'm + ' + repr(self.d_tx) + 'm/yr' + '\n'
                + '  ty: ' + repr(self.ty) + 'm + ' + repr(self.d_ty) + 'm/yr' + '\n'
                + '  tz: ' + repr(self.tz) + 'm + ' + repr(self.d_tz) + 'm/yr' + '\n'
                + '  sc: ' + repr(self.sc) + 'ppm + ' + repr(self.d_sc) + 'ppm/yr' + '\n'
                + '  rx: ' + repr(self.rx) + '\" + ' + repr(self.d_rx) + '\"/yr' + '\n'
                + '  ry: ' + repr(self.ry) + '\" + ' + repr(self.d_ry) + '\"/yr' + '\n'
                + '  rz: ' + repr(self.rz) + '\" + ' + repr(self.d_rz) + '\"/yr' + '\n')

    def __neg__(self):
        """
        Reverses Direction of Transformation Object
        i.e. ITRF2014 to ITRF2000 transformation becomes ITRF2000 to ITRF2014 transformation
        :return: Reversed Direction Transformation Object
        """
        return Transformation(self.to_datum,
                              self.from_datum,
                              self.ref_epoch,
                              -self.tx, -self.ty, -self.tz,
                              -self.sc,
                              -self.rx, -self.ry, -self.rz,
                              -self.d_tx, -self.d_ty, -self.d_tz,
                              -self.d_sc,
                              -self.d_rx, -self.d_ry, -self.d_rz)

    def __add__(self, other):
        """
        Change Transformation Epoch to a specified date.
        Advances all transformation parameters by their respective rates of change.
        :param other: datetime.date Object
        :return: Transformation object with parameters and ref epoch moved to specified date
        """
        if type(other) == date:
            timediff = (other - self.ref_epoch).days/365.25
            return Transformation(self.to_datum,
                                  self.from_datum,
                                  other,
                                  round(self.tx + (self.d_tx * timediff), 8),
                                  round(self.ty + (self.d_ty * timediff), 8),
                                  round(self.tz + (self.d_tz * timediff), 8),
                                  round(self.sc + (self.d_sc * timediff), 8),
                                  round(self.rx + (self.d_rx * timediff), 8),
                                  round(self.ry + (self.d_ry * timediff), 8),
                                  round(self.rz + (self.d_rz * timediff), 8),
                                  self.d_tx,
                                  self.d_ty,
                                  self.d_tz,
                                  self.d_sc,
                                  self.d_rx,
                                  self.d_ry,
                                  self.d_rz)
        else:
            ValueError('supports adding datetime.date objects only')


def iers2trans(itrf_from, itrf_to, ref_epoch, tx, ty, tz, sc, rx, ry, rz, d_tx, d_ty, d_tz, d_sc, d_rx, d_ry, d_rz):
    """
    Used to convert IERS transformation parameters into Transformation Class parameters.
    Note: All rotation and delta rotation terms have sign change applied
    :param itrf_from: ITRF Realization Transforming From
    :param itrf_to: ITRF Realization Transforming To
    :param ref_epoch: Reference Epoch (YYYY.DOY)
    :param tx: Translation in x (mm)
    :param ty: Translation in y (mm)
    :param tz: Translation in z (mm)
    :param sc: Scale Change (parts per billion)
    :param rx: Rotation about x (milliarcseconds)
    :param ry: Rotation about y (milliarcseconds)
    :param rz: Rotation about z (milliarcseconds)
    :param d_tx: Rate of change in Translation in x (mm per year)
    :param d_ty: Rate of change in Translation in y (mm per year)
    :param d_tz: Rate of change in Translation in z (mm per year)
    :param d_sc: Rate of change in Scale Change (parts per billion per year)
    :param d_rx: Rate of change in Rotation about x (milliarcseconds per year)
    :param d_ry: Rate of change in Rotation about y (milliarcseconds per year)
    :param d_rz: Rate of change in Rotation about z (milliarcseconds per year)
    :return: Transformation Object following Australian Convention
    """
    return Transformation(itrf_from, itrf_to, ref_epoch,
                          round(tx / 1000, 8), round(ty / 1000, 8), round(tz / 1000, 8),
                          round(sc / 1000, 8),
                          round(-rx / 1000, 8), round(-ry / 1000, 8), round(-rz / 1000, 8),
                          round(d_tx / 1000, 8), round(d_ty / 1000, 8), round(d_tz / 1000, 8),
                          round(d_sc / 1000, 8),
                          round(-d_rx / 1000, 8), round(-d_ry / 1000, 8), round(-d_rz / 1000, 8))

# GDA1994 to GDA2020 Transformation Parameters from GDA2020 Tech Manual v1.2

gda94_to_gda2020 = Transformation('GDA1994', 'GDA2020', 0,
                                  0.06155, -0.01087, -0.04019, -0.009994, -0.0394924, -0.0327221, -0.0328979)

# ITRF2014 to GDA2020 (Australian Plate Motion Model) Transformation Parameters from GDA2020 Tech Manual v1.2. The
# model was derived using 109 ARGN and AuScope GNSS CORS which were used to define the RVS.

itrf14togda20 = Transformation('ITRF2014', 'GDA2020', date(2020, 1, 1),
                                0, 0, 0, 0, 0, 0, 0,
                                0, 0, 0, 0, 0.00150379, 0.00118346, 0.00120716)

# ATRF to GDA2020 (Australian Plate Motion Model) Transformation Parameters (as advised by N. Brown, Geoscience
# Australia). The model was derived using 109 ARGN and AuScope GNSS CORS which were used to define the RVS.

atrf_gda2020 = Transformation('ATRF', 'GDA2020', date(2020, 1, 1),
                              0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0.00150379, 0.00118346, 0.00120716)

# GDA1994 to ITRF Transformation Parameters from Dawson and Woods (2010)
# AGD66 and AGD84 to GDA94 Transformation Parameters from GDA94 Tech Manual v2.4
# link: http://www.icsm.gov.au/datum/gda2020-and-gda94-technical-manuals

itrf08togda94 = Transformation('ITRF2008', 'GDA1994', date(1994, 1, 1),
                               -0.08468, -0.01942, 0.03201, 0.00971, -0.0004254, 0.0022578, 0.0024015,
                               0.00142, 0.00134, 0.00090, 0.000109, 0.0015461, 0.001820, 0.0011551)

itrf05togda94 = Transformation('ITRF2005', 'GDA1994', date(1994, 1, 1),
                               -0.07973, -0.00686, 0.03803, 0.006636, -0.0000351, 0.0021211, 0.0021411,
                               0.00225, -0.00062, -0.00056, 0.000294, 0.0014707, 0.0011443, 0.0011701)

itrf00togda94 = Transformation('ITRF2000', 'GDA1994', date(1994, 1, 1),
                               -0.04591, -0.02985, -0.02037, 0.00707, -0.0016705, 0.0004594, 0.0019356,
                               -0.00466, 0.00355, 0.01124, 0.000249, 0.0017454, 0.0014868, 0.001224)

itrf97togda94 = Transformation('ITRF1997', 'GDA1994', date(1994, 1, 1),
                               -0.01463, -0.02762, -0.02532, 0.006695, -0.0017893, -0.0006047, 0.0009962,
                               -0.00860, 0.00036, 0.01125, 0.000007, 0.0016394, 0.0015198, 0.0013801)

itrf96togda94 = Transformation('ITRF1996', 'GDA1994', date(1994, 1, 1),
                               0.02454, -0.03643, -0.06812, 0.006901, -0.0027359, -0.0020431, 0.0003731,
                               -0.02180, 0.00471, 0.02627, 0.000388, 0.0020203, 0.0021735, 0.0016290)

agd84togda94 = Transformation('AGD84', 'GDA94', 0,
                              -117.763, -51.510, 139.061, -0.191, -0.292, -0.443, -0.277)

agd66togda94 = Transformation('AGD1966', 'GDA1994', 0,
                              -117.808, -51.536, 137.784, -0.290, -0.303, -0.446, -0.234)

agd66togda94_act = Transformation('AGD66', 'GDA94', 0,
                                  -129.193, -41.212, 130.730, -2.955, -0.246, -0.374, -0.329)

agd66togda94_tas = Transformation('AGD66', 'GDA94', 0,
                                  -120.271, -64.543, 161.632, 2.499, -0.217, 0.067, 0.129)

agd66togda94_vicnsw = Transformation('AGD66', 'GDA94', 0,
                                     -119.353, -48.301, 139.484, -0.613, -0.415, -0.260, -0.437)

agd66togda94_nt = Transformation('AGD66', 'GDA94', 0,
                                 -124.133, -42.003, 137.400, -1.854, 0.008, -0.557, -0.178)


# ITRF2014 Parameters
# link: http://itrf.ign.fr/doc_ITRF/Transfo-ITRF2014_ITRFs.txt

itrf14to08 = iers2trans('ITRF2014', 'ITRF2008', date(2010, 1, 1),
                        1.6, 1.9, 2.4, -0.02, 0, 0, 0,
                        0.0, 0.0, -0.1, 0.03, 0, 0, 0)

itrf14to05 = iers2trans('ITRF2014', 'ITRF2005', date(2010, 1, 1),
                        2.6, 1.0, -2.3, 0.92, 0, 0, 0,
                        0.3, 0.0, -0.1, 0.03, 0, 0, 0)

itrf14to00 = iers2trans('ITRF2014', 'ITRF2000', date(2010, 1, 1),
                        0.7, 1.2, -26.1, 2.12, 0, 0, 0,
                        0.1, 0.1, -1.9, 0.11, 0, 0, 0)

itrf14to97 = iers2trans('ITRF2014', 'ITRF1997', date(2010, 1, 1),
                        7.4, -0.5, -62.8, 3.80, 0, 0, 0.26,
                        0.1, -0.5, -3.3, 0.12, 0, 0, 0.02)

itrf14to96 = iers2trans('ITRF2014', 'ITRF1996', date(2010, 1, 1),
                        7.4, -0.5, -62.8, 3.80, 0, 0, 0.26,
                        0.1, -0.5, -3.3, 0.12, 0, 0, 0.02)

itrf14to94 = iers2trans('ITRF2014', 'ITRF1994', date(2010, 1, 1),
                        7.4, -0.5, -62.8, 3.80, 0, 0, 0.26,
                        0.1, -0.5, -3.3, 0.12, 0, 0, 0.02)

itrf14to93 = iers2trans('ITRF2014', 'ITRF1993', date(2010, 1, 1),
                        -50.4, 3.3, -60.2, 4.29, -2.81, -3.38, 0.40,
                        -2.8, -0.1, -2.5, 0.12, -0.11, -0.19, 0.07)

itrf14to92 = iers2trans('ITRF2014', 'ITRF1992', date(2010, 1, 1),
                        15.4, 1.5, -70.8, 3.09, 0, 0, 0.26,
                        0.1, -0.5, -3.3, 0.12, 0, 0, 0.02)

itrf14to91 = iers2trans('ITRF2014', 'ITRF1991', date(2010, 1, 1),
                        27.4, 15.5, -76.8, 4.49, 0, 0, 0.26,
                        0.1, -0.5, -3.3, 0.12, 0, 0, 0.02)

itrf14to90 = iers2trans('ITRF2014', 'ITRF1990', date(2010, 1, 1),
                        25.4, 11.5, -92.8, 4.79, 0, 0, 0.26,
                        0.1, -0.5, -3.3, 0.12, 0, 0, 0.02)

itrf14to89 = iers2trans('ITRF2014', 'ITRF1989', date(2010, 1, 1),
                        30.4, 35.5, -130.8, 8.19, 0, 0, 0.26,
                        0.1, -0.5, -3.3, 0.12, 0, 0, 0.02)

itrf14to88 = iers2trans('ITRF2014', 'ITRF1988', date(2010, 1, 1),
                        25.4, -0.5, -154.8, 11.29, 0.1, 0, 0.26,
                        0.1, -0.5, -3.3, 0.12, 0, 0, 0.02)

# ITRF2008 Parameters
# link: http://itrf.ign.fr/doc_ITRF/Transfo-ITRF2008_ITRFs.txt

itrf08to05 = iers2trans('ITRF2008', 'ITRF2005', date(2000, 1, 1),
                        -2.0, -0.9, -4.7, 0.94, 0, 0, 0,
                        0.3, 0.0, 0.0, 0.0, 0, 0, 0)

itrf08to00 = iers2trans('ITRF2008', 'ITRF2000', date(2000, 1, 1),
                        -1.9, -1.7, -10.5, 1.34, 0, 0, 0,
                        0.1, 0.1, -1.8, 0.08, 0, 0, 0)

itrf08to97 = iers2trans('ITRF2008', 'ITRF1997', date(2000, 1, 1),
                        4.8, 2.6, -33.2, 2.92, 0, 0, 0.06,
                        0.1, -0.5, -3.2, 0.09, 0, 0, 0.02)

itrf08to96 = iers2trans('ITRF2008', 'ITRF1996', date(2000, 1, 1),
                        4.8, 2.6, -33.2, 2.92, 0, 0, 0.06,
                        0.1, -0.5, -3.2, 0.09, 0, 0, 0.02)

itrf08to94 = iers2trans('ITRF2008', 'ITRF1994', date(2000, 1, 1),
                        4.8, 2.6, -33.2, 2.92, 0, 0, 0.06,
                        0.1, -0.5, -3.2, 0.09, 0, 0, 0.02)

itrf08to93 = iers2trans('ITRF2008', 'ITRF1993', date(2000, 1, 1),
                        -24.0, 2.4, -38.6, 3.41, -1.71, -1.48, -0.30,
                        -2.8, -0.1, -2.4, 0.09, -0.11, -0.19, 0.07)

itrf08to92 = iers2trans('ITRF2008', 'ITRF1992', date(2000, 1, 1),
                        12.8, 4.6, -41.2, 2.21, 0, 0, 0.06,
                        0.1, -0.5, -3.2, 0.09, 0, 0, 0.02)

itrf08to91 = iers2trans('ITRF2008', 'ITRF1991', date(2000, 1, 1),
                        24.8, 18.6, -47.2, 3.61, 0, 0, 0.06,
                        0.1, -0.5, -3.2, 0.09, 0, 0, 0.02)

itrf08to90 = iers2trans('ITRF2008', 'ITRF1990', date(2000, 1, 1),
                        22.8, 14.6, -63.2, 3.91, 0, 0, 0.06,
                        0.1, -0.5, -3.2, 0.09, 0, 0, 0.02)

itrf08to89 = iers2trans('ITRF2008', 'ITRF1989', date(2000, 1, 1),
                        27.8, 38.6, -101.2, 7.31, 0, 0, 0.06,
                        0.1, -0.5, -3.2, 0.09, 0, 0, 0.02)

itrf08to88 = iers2trans('ITRF2008', 'ITRF1988', date(2000, 1, 1),
                        22.8, 2.6, -125.2, 10.41, 0.10, 0, 0.06,
                        0.1, -0.5, -3.2, 0.09, 0, 0, 0.02)

# ITRF2005 Parameters
# link: http://itrf.ensg.ign.fr/ITRF_solutions/2005/tp_05-00.php

itrf05to00 = iers2trans('ITRF2005', 'ITRF2000', date(2000, 1, 1),
                        0.1, -0.8, -5.8, 0.40, 0, 0, 0,
                        -0.2, 0.1, -1.8, 0.08, 0, 0, 0)

# ITRF2000 Parameters
# link: ftp://itrf.ensg.ign.fr/pub/itrf/ITRF.TP
# NOTE: This ref lists translations in centimetres. All other ITRF transformations are shown in millimetres.
# NOTE: All translations and rates of translation shown below have been converted to millimetres.

itrf00to97 = iers2trans('ITRF2000', 'ITRF1997', date(1997, 1, 1),
                        6.7, 6.1, -18.5, 1.55, 0, 0, 0,
                        0.0, -0.6, -1.4, 0.01, 0, 0, 0.02)

itrf00to96 = iers2trans('ITRF2000', 'ITRF1996', date(1997, 1, 1),
                        6.7, 6.1, -18.5, 1.55, 0, 0, 0,
                        0.0, -0.6, -1.4, 0.01, 0, 0, 0.02)

itrf00to94 = iers2trans('ITRF2000', 'ITRF1994', date(1997, 1, 1),
                        6.7, 6.1, -18.5, 1.55, 0, 0, 0,
                        0.0, -0.6, -1.4, 0.01, 0, 0, 0.02)

itrf00to93 = iers2trans('ITRF2000', 'ITRF1993', date(1988, 1, 1),
                        12.7, 6.5, -20.9, 1.95, -0.39, 0.80, -1.14,
                        -2.9, -0.2, -0.6, 0.01, -0.11, -0.19, 0.07)

itrf00to92 = iers2trans('ITRF2000', 'ITRF1992', date(1988, 1, 1),
                        14.7, 13.5, -13.9, 0.75, 0, 0, -0.18,
                        0.0, -0.6, -1.4, 0.01, 0, 0, 0.02)

itrf00to91 = iers2trans('ITRF2000', 'ITRF1991', date(1988, 1, 1),
                        26.7, 27.5, -19.9, 2.15, 0, 0, -0.18,
                        0.0, -0.6, -1.4, 0.01, 0, 0, 0.02)

itrf00to90 = iers2trans('ITRF2000', 'ITRF1990', date(1988, 1, 1),
                        14.7, 13.5, -13.9, 0.75, 0, 0, -0.18,
                        0.0, -0.6, -1.4, 0.01, 0, 0, 0.02)

itrf00to89 = iers2trans('ITRF2000', 'ITRF1989', date(1988, 1, 1),
                        29.7, 47.5, -73.9, 5.85, 0, 0, -0.18,
                        0.0, -0.6, -1.4, 0.01, 0, 0, 0.02)

itrf00to88 = iers2trans('ITRF2000', 'ITRF1988', date(1988, 1, 1),
                        24.7, 11.5, -97.9, 8.95, 0, 0, -0.18,
                        0.0, -0.6, -1.4, 0.01, 0, 0, 0.02)

# The locations of files used in the height module
file_DOV_PV='/vsicurl/https://geoid.s3-ap-southeast-2.amazonaws.com/AVWS/DOV_PV.tif'
file_DOV_PM='/vsicurl/https://geoid.s3-ap-southeast-2.amazonaws.com/AVWS/DOV_PM.tif'
file_AG2020='/vsicurl/https://geoid.s3-ap-southeast-2.amazonaws.com/AVWS/AUSGeoid2020_RELEASEV20170908.tif'
file_AG2020_STD='/vsicurl/https://geoid.s3-ap-southeast-2.amazonaws.com/AVWS/AUSGeoid2020_RELEASEV20170908_err.tif'
file_AVWS='/vsicurl/https://geoid.s3-ap-southeast-2.amazonaws.com/AVWS/AVWS_20191107.tif'
file_AVWS_STD='/vsicurl/https://geoid.s3-ap-southeast-2.amazonaws.com/AVWS/AVWS_STD_20191107.tif'
file_GRAV_BA='/vsicurl/https://geoid.s3-ap-southeast-2.amazonaws.com/AVWS/Bouguer_Grav_RELEASE20191107.tif'

# GRS80 normal gravity flattening (Moritz, 2000 Section 4)
grs80_ngf = 0.005302440112
