#!/usr/bin/env python3

"""
Geoscience Australia - Python Geodesy Package
Convert Module
"""

from math import (sin, cos, atan2, radians, degrees,
                  sqrt, cosh, sinh, tan, atan, log)
import datetime
from geodepy.constants import utm, grs80

# Universal Transverse Mercator Projection Parameters
proj = utm


class DMSAngle(object):
    """
    Class for working with angles in Degrees, Minutes and Seconds format
    """
    def __init__(self, degree=0, minute=0, second=0.0):
        """
        :param degree: Angle: whole degrees component (floats truncated)
        :param minute: Angle: whole minutes component (floats truncated)
        :param second: Angle: seconds component (floats preserved)
        """
        # Set sign of object based on sign of any variable
        if degree == 0:
            if str(degree)[0] == '-':
                self.sign = -1
            elif minute < 0:
                self.sign = -1
            elif second < 0:
                self.sign = -1
            else:
                self.sign = 1
        elif degree > 0:
            self.sign = 1
        else:  # degree < 0
            self.sign = -1
        self.degree = abs(int(degree))
        self.minute = abs(int(minute))
        self.second = abs(second)

    def __repr__(self):
        if self.sign == -1:
            signsymbol = '-'
        elif self.sign == 1:
            signsymbol = '+'
        else:
            signsymbol = 'error'
        return '{DMSAngle: ' + signsymbol + str(self.degree) + 'd ' +\
               str(self.minute) + 'm ' + str(self.second) + 's}'

    def __add__(self, other):
        try:
            return dec2dms(self.dec() + other.dec())
        except AttributeError:
            raise TypeError('Can only add DMSAngle and/or DDMAngle objects '
                            'together')

    def __radd__(self, other):
        try:
            return dec2dms(other.dec() + self.dec())
        except AttributeError:
            raise TypeError('Can only add DMSAngle and/or DDMAngle objects '
                            'together')

    def __sub__(self, other):
        try:
            return dec2dms(self.dec() - other.dec())
        except AttributeError:
            raise TypeError('Can only subtract DMSAngle and/or DDMAngle '
                            'objects together')

    def __rsub__(self, other):
        try:
            return dec2dms(other.dec() - self.dec())
        except AttributeError:
            raise TypeError('Can only subtract DMSAngle and/or DDMAngle '
                            'objects together')

    def __mul__(self, other):
        try:
            return dec2dms(self.dec() * other)
        except TypeError:
            raise TypeError('Multiply only defined between DMSAngle Object '
                            'and Int or Float')

    def __rmul__(self, other):
        try:
            return dec2dms(other * self.dec())
        except TypeError:
            raise TypeError('Multiply only defined between DMSAngle Object '
                            'and Int or Float')

    def __truediv__(self, other):
        try:
            return dec2dms(self.dec() / other)
        except TypeError:
            raise TypeError('Division only defined between DMSAngle Object '
                            'and Int or Float')

    def __abs__(self):
        return DMSAngle(self.degree, self.minute, self.second)

    def __neg__(self):
        if self.sign == 1:
            return DMSAngle(-self.degree, -self.minute, -self.second)
        else:  # sign == -1
            return DMSAngle(self.degree, self.minute, self.second)

    def __eq__(self, other):
        return self.dec() == other.dec()

    def __ne__(self, other):
        return self.dec() != other.dec()

    def __lt__(self, other):
        return self.dec() < other.dec()

    def __gt__(self, other):
        return self.dec() > other.dec()

    def dec(self):
        """
        Convert to Decimal Degrees
        :return: Decimal Degrees
        :rtype: float
        """
        return self.sign * (self.degree + (self.minute / 60) +
                            (self.second / 3600))

    def hp(self):
        """
        Convert to HP Notation
        :return: HP Notation (DDD.MMSSSS)
        :rtype: float
        """
        return self.sign * (self.degree + (self.minute / 100) +
                            (self.second / 10000))

    def ddm(self):
        """
        Convert to Degrees, Decimal Minutes Object
        :return: Degrees, Decimal Minutes Object
        :rtype: DDMAngle
        """
        if self.sign == 1:
            return DDMAngle(self.degree, self.minute + (self.second/60))
        else:  # sign == -1
            return -DDMAngle(self.degree, self.minute + (self.second/60))


class DDMAngle(object):
    """
    Class for working with angles in Degrees, Decimal Minutes format
    """
    def __init__(self, degree=0, minute=0.0):
        """
        :param degree: Angle: whole degrees component (floats truncated)
        :param minute: Angle:minutes component (floats preserved)
        """
        # Set sign of object based on sign of any variable
        if degree == 0:
            if str(degree)[0] == '-':
                self.sign = -1
            elif minute < 0:
                self.sign = -1
            else:
                self.sign = 1
        elif degree > 0:
            self.sign = 1
        else:  # degree < 0
            self.sign = -1
        self.degree = abs(int(degree))
        self.minute = abs(minute)

    def __repr__(self):
        if self.sign == -1:
            signsymbol = '-'
        elif self.sign == 1:
            signsymbol = '+'
        else:
            signsymbol = 'error'
        return '{DDMAngle: ' + signsymbol + str(self.degree) + 'd ' + \
               str(self.minute) + 'm}'

    def __add__(self, other):
        try:
            return dec2ddm(self.dec() + other.dec())
        except AttributeError:
            raise TypeError('Can only add DMSAngle and/or DDMAngle objects '
                            'together')

    def __radd__(self, other):
        try:
            return dec2ddm(other.dec() + self.dec())
        except AttributeError:
            raise TypeError('Can only add DMSAngle and/or DDMAngle objects '
                            'together')

    def __sub__(self, other):
        try:
            return dec2ddm(self.dec() - other.dec())
        except AttributeError:
            raise TypeError('Can only add DMSAngle and/or DDMAngle objects '
                            'together')

    def __rsub__(self, other):
        try:
            return dec2ddm(other.dec() - self.dec())
        except AttributeError:
            raise TypeError('Can only add DMSAngle and/or DDMAngle objects '
                            'together')

    def __mul__(self, other):
        try:
            return dec2ddm(self.dec() * other)
        except TypeError:
            raise TypeError('Multiply only defined between DMSAngle Object '
                            'and Int or Float')

    def __rmul__(self, other):
        try:
            return dec2ddm(other * self.dec())
        except TypeError:
            raise TypeError('Multiply only defined between DMSAngle Object '
                            'and Int or Float')

    def __truediv__(self, other):
        try:
            return dec2ddm(self.dec() / other)
        except TypeError:
            raise TypeError('Division only defined between DMSAngle Object '
                            'and Int or Float')

    def __abs__(self):
        return DDMAngle(self.degree, self.minute)

    def __neg__(self):
        if self.sign == 1:
            return DDMAngle(-self.degree, -self.minute)
        else:  # sign == -1
            return DDMAngle(self.degree, self.minute)

    def __eq__(self, other):
        return self.dec() == other.dec()

    def __ne__(self, other):
        return self.dec() != other.dec()

    def __lt__(self, other):
        return self.dec() < other.dec()

    def __gt__(self, other):
        return self.dec() > other.dec()

    def dec(self):
        """
        Convert to Decimal Degrees
        :return: Decimal Degrees
        :rtype: float
        """
        return self.sign * (self.degree + (self.minute / 60))

    def hp(self):
        """
        Convert to HP Notation
        :return: HP Notation (DDD.MMSSSS)
        :rtype: float
        """
        minute_int, second = divmod(self.minute, 1)
        return self.sign * (self.degree + (minute_int / 100) +
                            (second * 0.006))

    def dms(self):
        """
        Convert to Degrees, Minutes, Seconds Object
        :return: Degrees, Minutes, Seconds Object
        :rtype: DMSAngle
        """
        minute_int, second = divmod(self.minute, 1)
        return self.sign * DMSAngle(self.degree, minute_int, second * 60)


def dec2hp(dec):
    """
    Converts Decimal Degrees to HP Notation
    :param dec: Decimal Degrees
    :type dec: float
    :return: HP Notation (DDD.MMSSSS)
    :rtype: float
    """
    minute, second = divmod(abs(dec) * 3600, 60)
    degree, minute = divmod(minute, 60)
    hp = degree + (minute / 100) + (second / 10000)
    return hp if dec >= 0 else -hp


def hp2dec(hp):
    """
    Converts HP Notation to Decimal Degrees
    :param hp: HP Notation (DDD.MMSSSS)
    :type hp: float
    :return: Decimal Degrees
    :rtype: float
    """
    degmin, second = divmod(abs(hp) * 1000, 10)
    degree, minute = divmod(degmin, 100)
    dec = degree + (minute / 60) + (second / 360)
    return dec if hp >= 0 else -dec


def dec2dms(dec):
    """
    Converts Decimal Degrees to Degrees, Minutes, Seconds Object
    :param dec: Decimal Degrees
    :type dec: float
    :return: Degrees, Minutes, Seconds Object
    :rtype: DMSAngle
    """
    minute, second = divmod(abs(dec) * 3600, 60)
    degree, minute = divmod(minute, 60)
    return (DMSAngle(degree, minute, second) if dec >= 0
            else DMSAngle(-degree, minute, second))


def dec2ddm(dec):
    """
    Converts Decimal Degrees to Degrees, Decimal Minutes Object
    :param dec: Decimal Degrees
    :type dec: float
    :return: Degrees, Decimal Minutes Object
    :rtype: DDMAngle
    """
    minute, second = divmod(abs(dec) * 3600, 60)
    degree, minute = divmod(minute, 60)
    minute = minute + (second / 60)
    return DDMAngle(degree, minute) if dec >= 0 else DDMAngle(-degree, minute)


def hp2dms(hp):
    """
    Converts HP Notation to Degrees, Minutes, Seconds Object
    :param hp: HP Notation (DDD.MMSSSS)
    :type hp: float
    :return: Degrees, Minutes, Seconds Object
    :rtype: DMSAngle
    """
    degmin, second = divmod(abs(hp) * 1000, 10)
    degree, minute = divmod(degmin, 100)
    return (DMSAngle(degree, minute, second * 10) if hp >= 0
            else DMSAngle(-degree, minute, second * 10))


def hp2ddm(hp):
    """
    Converts HP Notation to Degrees, Decimal Minutes Object
    :param hp: HP Notation (DDD.MMSSSS)
    :type hp: float
    :return: Degrees, Decimal Minutes Object
    :rtype: DDMAngle
    """
    degmin, second = divmod(abs(hp) * 1000, 10)
    degree, minute = divmod(degmin, 100)
    minute = minute + (second / 6)
    return DDMAngle(degree, minute) if hp >= 0 else DDMAngle(-degree, minute)


def polar2rect(r, theta):
    """
    Converts point in polar coordinates to corresponding rectangular coordinates
    Theta is degrees and is measured clockwise from the positive y axis
    (i.e. north)
    :param r: Radius
    :param theta: Angle (decimal degrees)
    :type theta: Float (decimal degrees), DMSAngle or DDMAngle
    :return: Rectangular Coordinates X, Y
    """
    theta = angular_typecheck(theta)
    x = r * sin(radians(theta))
    y = r * cos(radians(theta))
    return x, y


def rect2polar(x, y):
    """
    Converts point in rectangular coordinates to corresponding polar coordinates
    Angular component of polar coordinates (theta) is in decimal degrees and
    is measured clockwise from the positive y axis (i.e. north)
    :param x: Rectangular Coordinate X
    :param y: Rectangular Coordinate Y
    :return r: Radius
    :return theta: Angle (decimal degrees)
    :rtype theta: float (decimal degrees)
    """
    r = sqrt(x ** 2 + y ** 2)
    theta = atan2(x, y)
    if theta < 0:
        theta = degrees(theta) + 360
    else:
        theta = degrees(theta)
    return r, theta


def dd2sec(dd):
    """
    Converts angle in decimal degrees to angle in seconds
    :param dd: Decimal Degrees
    :return: Seconds
    """
    minute, second = divmod(abs(dd) * 3600, 60)
    degree, minute = divmod(minute, 60)
    sec = (degree * 3600) + (minute * 60) + second
    return sec if dd >= 0 else -sec


def dec2hp_v(dec):
    minute, second = divmod(abs(dec) * 3600, 60)
    degree, minute = divmod(minute, 60)
    hp = degree + (minute / 100) + (second / 10000)
    hp[dec <= 0] = -hp[dec <= 0]
    return hp


def hp2dec_v(hp):
    degmin, second = divmod(abs(hp) * 1000, 10)
    degree, minute = divmod(degmin, 100)
    dec = degree + (minute / 60) + (second / 360)
    dec[hp <= 0] = -dec[hp <= 0]
    return dec


def angular_typecheck(angle):
    # Converts DMSAngle and DDMAngle Objects to Decimal Degrees
    if type(angle) is DMSAngle or type(angle) is DDMAngle:
        return angle.dec()
    else:
        return angle


def rect_radius(ellipsoid):
    """
    Computes the Rectifying Radius of an Ellipsoid with specified Inverse
    Flattening (See Ref 2 Equation 3)
    :param ellipsoid: Ellipsoid Object
    :type ellipsoid: Ellipsoid
    :return: Ellipsoid Rectifying Radius
    """
    nval = (1 / float(ellipsoid.inversef)) /\
           (2 - (1 / float(ellipsoid.inversef)))
    nval2 = nval**2
    return (ellipsoid.semimaj / (1 + nval) * ((nval2 *
                                              (nval2 *
                                               (nval2 *
                                                (25 * nval2 + 64)
                                                + 256)
                                               + 4096)
                                              + 16384)
                                              / 16384.))


def alpha_coeff(ellipsoid):
    """
    Computes the set of Alpha coefficients of an Ellipsoid with specified
    Inverse Flattening (See Ref 2 Equation 5)
    :param ellipsoid: Ellipsoid Object
    :type ellipsoid: Ellipsoid
    :return: Alpha coefficients a2, a4 ... a16
    :rtype: tuple
    """
    nval = ellipsoid.n
    a2 = ((nval *
           (nval *
            (nval *
             (nval *
              (nval *
               (nval *
                ((37884525 - 75900428 * nval)
                 * nval + 42422016)
                - 89611200)
               + 46287360)
              + 63504000)
             - 135475200)
            + 101606400))
          / 203212800.)

    a4 = ((nval ** 2 *
           (nval *
            (nval *
             (nval *
              (nval *
               (nval *
                (148003883 * nval + 83274912)
                - 178508970)
               + 77690880)
              + 67374720)
             - 104509440)
            + 47174400))
          / 174182400.)

    a6 = ((nval ** 3 *
           (nval *
            (nval *
             (nval *
              (nval *
               (318729724 * nval - 738126169)
               + 294981280)
              + 178924680)
             - 234938880)
            + 81164160))
          / 319334400.)

    a8 = ((nval ** 4 *
           (nval *
            (nval *
             ((14967552000 - 40176129013 * nval) * nval + 6971354016)
             - 8165836800)
            + 2355138720))
          / 7664025600.)

    a10 = ((nval ** 5 *
            (nval *
             (nval *
              (10421654396 * nval + 3997835751)
              - 4266773472)
             + 1072709352))
           / 2490808320.)

    a12 = ((nval ** 6 *
            (nval *
             (175214326799 * nval - 171950693600)
             + 38652967262))
           / 58118860800.)

    a14 = ((nval ** 7 *
            (13700311101 - 67039739596 * nval))
           / 12454041600.)

    a16 = (1424729850961 * nval ** 8) / 743921418240.
    return a2, a4, a6, a8, a10, a12, a14, a16


def beta_coeff(ellipsoid):
    """
    Computes the set of Beta coefficients of an Ellipsoid with specified
    Inverse Flattening (See Ref 2 Equation 23)
    :param ellipsoid: Ellipsoid Object
    :type ellipsoid: Ellipsoid
    :return: Alpha coefficients a2, a4 ... a16
    :rtype: tuple
    """
    nval = ellipsoid.n
    b2 = ((nval *
           (nval *
            (nval *
             (nval *
              (nval *
               (nval *
                ((37845269 - 31777436 * nval) - 43097152)
                + 42865200)
               + 752640)
              - 104428800)
             + 180633600)
            - 135475200))
          / 270950400.)

    b4 = ((nval ** 2 *
           (nval *
            (nval *
             (nval *
              (nval *
               ((-24749483 * nval - 14930208) * nval + 100683990)
               - 152616960)
              + 105719040)
             - 23224320)
            - 7257600))
          / 348364800.)

    b6 = ((nval ** 3 *
           (nval *
            (nval *
             (nval *
              (nval *
               (232468668 * nval - 101880889)
               - 39205760)
              + 29795040)
             + 28131840)
            - 22619520))
          / 638668800.)

    b8 = ((nval ** 4 *
           (nval *
            (nval *
             ((-324154477 * nval - 1433121792) * nval + 876745056)
             + 167270400)
            - 208945440))
          / 7664025600.)

    b10 = ((nval ** 5 *
            (nval *
             (nval *
              (312227409 - 457888660 * nval)
              + 67920528)
             - 70779852))
           / 2490808320.)

    b12 = ((nval ** 6 *
            (nval *
             (19841813847 * nval + 3665348512)
             - 3758062126))
           / 116237721600.)

    b14 = ((nval ** 7 *
            (1989295244 * nval - 1979471673))
           / 49816166400.)

    b16 = ((-191773887257 * nval ** 8) / 3719607091200.)
    return b2, b4, b6, b8, b10, b12, b14, b16


def psfandgridconv(xi1, eta1, lat, lon, cm, conf_lat, ellipsoid=grs80):
    """
    Calculates Point Scale Factor and Grid Convergence. Used in convert.geo2grid
    and convert.grid2geo
    :param xi1: Transverse Mercator Ratio Xi
    :param eta1: Transverse Mercator Ratio Eta
    :param lat: Latitude
    :type lat: Decimal Degrees, DMSAngle or DDMAngle
    :param lon: Longitude
    :type lon: Decimal Degrees, DMSAngle or DDMAngle
    :param cm: Central Meridian
    :param conf_lat: Conformal Latitude
    :param ellipsoid: Ellipsoid Object (default: GRS80)
    :return: Point Scale Factor, Grid Convergence (Decimal Degrees)
    :rtype: tuple
    """
    lat = angular_typecheck(lat)
    lon = angular_typecheck(lon)
    A = rect_radius(ellipsoid)
    a = alpha_coeff(ellipsoid)
    lat = radians(lat)
    long_diff = radians(lon - cm)

    # Point Scale Factor
    p = 1
    q = 0
    for r in range(1, 9):
        p += 2*r * a[r-1] * cos(2*r * xi1) * cosh(2*r * eta1)
        q += 2*r * a[r-1] * sin(2*r * xi1) * sinh(2*r * eta1)
    q = -q
    psf = (float(proj.cmscale)
           * (A / ellipsoid.semimaj)
           * sqrt(q**2 + p**2)
           * ((sqrt(1 + (tan(lat)**2))
               * sqrt(1 - ellipsoid.ecc1sq * (sin(lat)**2)))
              / sqrt((tan(conf_lat)**2) + (cos(long_diff)**2))))

    # Grid Convergence
    grid_conv = degrees(atan(abs(q / p))
                        + atan(abs(tan(conf_lat) * tan(long_diff))
                               / sqrt(1 + tan(conf_lat)**2)))
    if cm > lon and lat < 0:
        grid_conv = -grid_conv
    elif cm < lon and lat > 0:
        grid_conv = -grid_conv

    return psf, grid_conv


def geo2grid(lat, lon, zone=0, ellipsoid=grs80):
    """
    Takes a geographic co-ordinate (latitude, longitude) and returns its
    corresponding Hemisphere, Zone and Projection Easting and Northing, Point
    Scale Factor and Grid Convergence. Default Projection is Universal
    Transverse Mercator Projection using
    GRS80 Ellipsoid parameters.
    :param lat: Latitude
    :type lat: Float (Decimal Degrees), DMSAngle or DDMAngle
    :param lon: Longitude
    :type lon: Float (Decimal Degrees, DMSAngle or DDMAngle
    :param zone: Optional Zone Number - Only required if calculating grid
                                        co-ordinate outside zone boundaries
    :param ellipsoid: Ellipsoid Object
    :type ellipsoid: Ellipsoid
    :return: hemisphere, zone, east (m), north (m), Point Scale Factor,
             Grid Convergence (Decimal Degrees)
    :rtype: tuple
    """

    # Convert DMSAngle and DDMAngle to Decimal Angle
    lat = angular_typecheck(lat)
    lon = angular_typecheck(lon)
    # Input Validation - UTM Extents and Values
    zone = int(zone)
    if zone < 0 or zone > 60:
        raise ValueError('Invalid Zone - Zones from 1 to 60')

    if lat < -80 or lat > 84:
        raise ValueError('Invalid Latitude - Latitudes from -80 to +84')

    if lon < -180 or lon > 180:
        raise ValueError('Invalid Longitude - Longitudes from -180 to +180')

    A = rect_radius(ellipsoid)
    a = alpha_coeff(ellipsoid)
    lat = radians(lat)
    # Calculate Zone
    if zone == 0:
        zone = int((float(lon) - (
                    proj.initialcm - (1.5 * proj.zonewidth))) / proj.zonewidth)
    cm = float(zone * proj.zonewidth) + (proj.initialcm - proj.zonewidth)

    # Conformal Latitude
    sigx = (ellipsoid.ecc1 * tan(lat)) / sqrt(1 + (tan(lat) ** 2))
    sig = sinh(ellipsoid.ecc1 * (0.5 * log((1 + sigx) / (1 - sigx))))
    conf_lat = tan(lat) * sqrt(1 + sig ** 2) - sig * sqrt(1 + (tan(lat) ** 2))
    conf_lat = atan(conf_lat)

    # Longitude Difference
    long_diff = radians(lon - cm)
    # Gauss-Schreiber Ratios
    xi1 = atan(tan(conf_lat) / cos(long_diff))
    eta1x = sin(long_diff) / (sqrt(tan(conf_lat) ** 2 + cos(long_diff) ** 2))
    eta1 = log(eta1x + sqrt(1 + eta1x ** 2))

    # Transverse Mercator Ratios
    eta = eta1
    xi = xi1
    for r in range(1, 9):
        eta += a[r-1] * cos(2*r * xi1) * sinh(2*r * eta1)
        xi += a[r-1] * sin(2*r * xi1) * cosh(2*r * eta1)

    # Transverse Mercator Co-ordinates
    x = A * eta
    y = A * xi

    # Hemisphere-dependent UTM Projection Co-ordinates
    east = proj.cmscale * x + proj.falseeast
    if y < 0:
        hemisphere = 'South'
        north = proj.cmscale * y + proj.falsenorth
    else:
        hemisphere = 'North'
        falsenorth = 0
        north = proj.cmscale * y + falsenorth

    # Point Scale Factor and Grid Convergence
    psf, grid_conv = psfandgridconv(xi1, eta1, degrees(lat), lon, cm, conf_lat)

    return (hemisphere, zone,
            round(float(east), 4),
            round(float(north), 4),
            round(psf, 8), grid_conv)


def grid2geo(zone, east, north, hemisphere='south', ellipsoid=grs80):
    """
    Takes a Transverse Mercator grid co-ordinate (Zone, Easting, Northing,
    Hemisphere) and returns its corresponding Geographic Latitude and Longitude,
    Point Scale Factor and Grid Convergence. Default Projection is Universal
    Transverse Mercator Projection using GRS80 Ellipsoid parameters.
    :param zone: Zone Number - 1 to 60
    :param east: Easting (m, within 3330km of Central Meridian)
    :param north: Northing (m, 0 to 10,000,000m)
    :param hemisphere: String - 'North' or 'South'(default)
    :param ellipsoid: Ellipsoid Object
    :type ellipsoid: Ellipsoid
    :return: Latitude and Longitude (Decimal Degrees), Point Scale Factor,
             Grid Convergence (Decimal Degrees)
    :rtype: tuple
    """
    # Input Validation - UTM Extents and Values
    zone = int(zone)
    if zone < 0 or zone > 60:
        raise ValueError('Invalid Zone - Zones from 1 to 60')

    if east < -2830000 or east > 3830000:
        raise ValueError('Invalid Easting - Must be within'
                         '3330km of Central Meridian')

    if north < 0 or north > 10000000:
        raise ValueError('Invalid Northing - Must be between 0 and 10,000,000m')

    h = hemisphere.lower()
    if h != 'north' and h != 'south':
        raise ValueError('Invalid Hemisphere - String, either North or South')

    A = rect_radius(ellipsoid)
    b = beta_coeff(ellipsoid)
    # Transverse Mercator Co-ordinates
    x = (east - float(proj.falseeast)) / float(proj.cmscale)
    if hemisphere.lower() == 'north':
        y = -(north / float(proj.cmscale))
        hemisign = -1
    else:
        y = (north - float(proj.falsenorth)) / float(proj.cmscale)
        hemisign = 1

    # Transverse Mercator Ratios
    xi = y / A
    eta = x / A

    # Gauss-Schreiber Ratios
    eta1 = eta
    xi1 = xi
    for r in range(1, 9):
        eta1 += b[r-1] * cos(2*r * xi) * sinh(2*r * eta)
        xi1 += b[r-1] * sin(2*r * xi) * cosh(2*r * eta)

    # Conformal Latitude
    conf_lat = (sin(xi1)) / (sqrt((sinh(eta1)) ** 2 + (cos(xi1)) ** 2))
    t1 = conf_lat
    conf_lat = atan(conf_lat)

    # Finding t using Newtons Method
    def sigma(tn, ecc1):
        return (sinh(ecc1
                     * 0.5
                     * log((1 + ((ecc1 * tn) / (sqrt(1 + tn ** 2))))
                           / (1 - ((ecc1 * tn) / (sqrt(1 + tn ** 2)))))))

    def ftn(tn, ecc1):
        return (t * sqrt(1 + (sigma(tn, ecc1)) ** 2) -
                sigma(tn, ecc1) * sqrt(1 + tn ** 2) - t1)

    def f1tn(tn, ecc1, ecc1sq):
        return ((sqrt(1 + (sigma(tn, ecc1)) ** 2) * sqrt(1 + tn ** 2)
                 - sigma(tn, ecc1) * tn)
                * (((1 - float(ecc1sq)) * sqrt(1 + t ** 2))
                   / (1 + (1 - float(ecc1sq)) * t ** 2)))

    diff = 1
    t = t1
    itercount = 0
    while diff > 1e-15 and itercount < 100:
        itercount += 1
        t_before = t
        t = t - (ftn(t, ellipsoid.ecc1)
                 / f1tn(t, ellipsoid.ecc1, ellipsoid.ecc1sq))
        diff = abs(t - t_before)
    lat = degrees(atan(t))

    # Compute Longitude
    cm = float((zone * proj.zonewidth) + proj.initialcm - proj.zonewidth)
    long_diff = degrees(atan(sinh(eta1) / cos(xi1)))
    long = cm + long_diff

    # Point Scale Factor and Grid Convergence
    psf, grid_conv = psfandgridconv(xi1, eta1, lat, long, cm, conf_lat)

    return (hemisign * round(lat, 11),
            round(long, 11), round(psf, 8),
            hemisign * grid_conv)


def xyz2llh(x, y, z, ellipsoid=grs80):
    """
    Converts Cartesian X, Y, Z coordinate to Geographic Latitude, Longitude and
    Ellipsoid Height. Default Ellipsoid parameters used are GRS80.
    :param x: Cartesian X Coordinate (metres)
    :param y: Cartesian Y Coordinate (metres)
    :param z: Cartesian Z Coordinate (metres)
    :param ellipsoid: Ellipsoid Object
    :type ellipsoid: Ellipsoid
    :return: Geographic Latitude (Decimal Degrees), Longitude (Decimal Degrees)
    and Ellipsoid Height (metres)
    :rtype: tuple
    """
    # Calculate Longitude
    long = atan2(y, x)
    # Calculate Latitude
    p = sqrt(x**2 + y**2)
    latinit = atan((z*(1+ellipsoid.ecc2sq))/p)
    lat = latinit
    itercheck = 1
    while abs(itercheck) > 1e-10:
        nu = ellipsoid.semimaj/(sqrt(1 - ellipsoid.ecc1sq * (sin(lat))**2))
        itercheck = lat - atan((z + nu * ellipsoid.ecc1sq * sin(lat))/p)
        lat = atan((z + nu * ellipsoid.ecc1sq * sin(lat))/p)
    nu = ellipsoid.semimaj/(sqrt(1 - ellipsoid.ecc1sq * (sin(lat))**2))
    ellht = p/(cos(lat)) - nu
    # Convert Latitude and Longitude to Degrees
    lat = degrees(lat)
    long = degrees(long)
    return lat, long, ellht


def llh2xyz(lat, lon, ellht=0, ellipsoid=grs80):
    """
    Converts Geographic Latitude, Longitude and Ellipsoid Height to Cartesian
    X, Y and Z Coordinates. Default Ellipsoid parameters used are GRS80.
    :param lat: Geographic Latitude
    :type lat: Float (Decimal Degrees), DMSAngle or DDMAngle
    :param lon: Geographic Longitude
    :type lon: Float (Decimal Degrees), DMSAngle or DDMAngle
    :param ellht: Ellipsoid Height (metres, default is 0m)
    :param ellipsoid: Ellipsoid Object
    :type ellipsoid: Ellipsoid
    :return: Cartesian X, Y, Z Coordinate in metres
    :rtype: tuple
    """
    # Convert lat & long to radians
    lat = radians(angular_typecheck(lat))
    lon = radians(angular_typecheck(lon))
    # Calculate Ellipsoid Radius of Curvature in the Prime Vertical - nu
    if lat == 0:
        nu = grs80.semimaj
    else:
        nu = ellipsoid.semimaj/(sqrt(1 - ellipsoid.ecc1sq * (sin(lat)**2)))
    # Calculate x, y, z
    x = (nu + ellht) * cos(lat) * cos(lon)
    y = (nu + ellht) * cos(lat) * sin(lon)
    z = ((ellipsoid.semimin**2 / ellipsoid.semimaj**2) * nu + ellht) * sin(lat)
    return x, y, z


def date_to_yyyydoy(date):
    """
    Convert a datetime.date object to a string in the form 'yyyy.doy',
    where yyyy is the 4 character year number and doy is the 3 character
    day of year
    :param date: datetime.date object
    :type date: datetime.date
    :return: string with date in the form 'yyyy.doy'
    :rtype: str
    """
    try:
        return (str(date.timetuple().tm_year) + '.' +
                str(date.timetuple().tm_yday).zfill(3))
    except AttributeError:
        raise AttributeError('Invalid date: date must be datetime.date object')


def yyyydoy_to_date(yyyydoy):
    """
    Convert a string in the form of either 'yyyydoy' or 'yyyy.doy' to a
    datetime.date object, where yyyy is the 4 character year number and doy
    is the 3 character day of year
    :param yyyydoy: string with date in the form 'yyyy.doy' or 'yyyydoy'
    :return: datetime.date object
    :rtype: datetime.date
    """
    try:
        if '.' in yyyydoy:
            if len(yyyydoy) != 8:
                raise ValueError('Invalid string: must be yyyydoy or yyyy.doy')
            yyyy, doy = yyyydoy.split('.')
        else:
            if len(yyyydoy) != 7:
                raise ValueError('Invalid string: must be yyyydoy or yyyy.doy')
            yyyy = yyyydoy[0:4]
            doy = yyyydoy[4:7]
        return datetime.date(int(yyyy), 1, 1) + datetime.timedelta(int(doy) - 1)
    except ValueError:
        raise ValueError('Invalid string: must be yyyydoy or yyyy.doy')
