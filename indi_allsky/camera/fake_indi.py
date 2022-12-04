import logging

logger = logging.getLogger('indi_allsky')


class FakeIndiClient(object):

    def __init__(
        self,
        config,
        image_q,
        latitude_v,
        longitude_v,
        gain_v,
        bin_v,
    ):
        super(FakeIndiClient, self).__init__()

        self.config = config
        self.image_q = image_q

        self.latitude_v = latitude_v
        self.longitude_v = longitude_v
        self.gain_v = gain_v
        self.bin_v = bin_v

        self._ccd_device = None

        self._ccd_gain = -1
        self._ccd_bin = 1
        self._ccd_frame_type = 'LIGHT'

        self.camera_info = {
            'width'         : None,
            'height'        : None,
            'pixel'         : None,
            'min_gain'      : 0,
            'max_gain'      : 100,
            'min_exposure'  : 0.0000032,
            'max_exposure'  : 300.0,
            'cfa'           : None,
            'bit_depth'     : 12,
        }


        self._telescope_device = None
        self.telescope_info = {
            'lat'           : 0.0,
            'long'          : 0.0,
        }

        self._gps_device = None
        self.gps_info = {
            'lat'           : 0.0,
            'long'          : 0.0,
        }


        self._filename_t = 'ccd{0:d}_{1:s}.{2:s}'

        self._timeout = 65.0
        self._exposure = 0.0

        self.exposureStartTime = None

        logger.info('creating an instance of FakeIndiClient')



    @property
    def ccd_device(self):
        return self._ccd_device

    @ccd_device.setter
    def ccd_device(self, new_ccd_device):
        self._ccd_device = new_ccd_device


    @property
    def telescope_device(self):
        return self._telescope_device

    @telescope_device.setter
    def telescope_device(self, new_telescope_device):
        self._telescope_device = new_telescope_device


    @property
    def gps_device(self):
        return self._gps_device

    @gps_device.setter
    def gps_device(self, new_gps_device):
        self._gps_device = new_gps_device


    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, new_timeout):
        self._timeout = float(new_timeout)

    @property
    def exposure(self):
        return self._exposure

    @exposure.setter
    def exposure(self, new_exposure):
        self._exposure = float(new_exposure)

    @property
    def filename_t(self):
        return self._filename_t

    @filename_t.setter
    def filename_t(self, new_filename_t):
        self._filename_t = new_filename_t


    def setServer(self, *args, **kwargs):
        # does nothing
        pass


    def connectServer(self):
        # does nothing
        return True


    def disconnectServer(self):
        # does nothing
        pass


    def connectDevice(self, *args, **kwargs):
        # does nothing
        pass


    def getHost(self):
        return self.__class__.__name__


    def getPort(self):
        return 0


    def updateCcdBlobMode(self, *args, **kwargs):
        # does nothing
        pass


    def disableDebug(self, *args, **kwargs):
        # does nothing
        pass


    def disableDebugCcd(self):
        self.disableDebug(self._ccd_device)


    def saveCcdConfig(self):
        # does nothing
        pass


    def resetCcdFrame(self, *args, **kwargs):
        # does nothing
        pass


    def setCcdFrameType(self, frame_type):
        self._ccd_frame_type = frame_type


    def getDeviceProperties(self, device):
        properties = dict()
        return properties


    def getCcdDeviceProperties(self):
        return self.getDeviceProperties(self._ccd_device)


    def getCcdInfo(self):
        ccdinfo = dict()

        ccdinfo['CCD_EXPOSURE'] = dict()
        ccdinfo['CCD_EXPOSURE']['CCD_EXPOSURE_VALUE'] = {
            'current' : None,
            'min'     : self._ccd_device.min_exposure,
            'max'     : self._ccd_device.max_exposure,
            'step'    : None,
            'format'  : None,
        }

        ccdinfo['CCD_INFO'] = dict()
        ccdinfo['CCD_INFO']['CCD_MAX_X'] = dict()
        ccdinfo['CCD_INFO']['CCD_MAX_Y'] = dict()
        ccdinfo['CCD_INFO']['CCD_PIXEL_SIZE'] = dict()
        ccdinfo['CCD_INFO']['CCD_PIXEL_SIZE_X'] = dict()
        ccdinfo['CCD_INFO']['CCD_PIXEL_SIZE_Y'] = dict()

        ccdinfo['CCD_INFO']['CCD_BITSPERPIXEL'] = {
            'current' : self._ccd_device.bit_depth,
            'min'     : None,
            'max'     : None,
            'step'    : None,
            'format'  : None,
        }

        ccdinfo['CCD_CFA'] = dict()
        ccdinfo['CCD_CFA']['CFA_TYPE'] = {
            'text' : self._ccd_device.cfa,
        }

        ccdinfo['CCD_FRAME'] = dict()
        ccdinfo['CCD_FRAME']['X'] = dict()
        ccdinfo['CCD_FRAME']['Y'] = dict()
        ccdinfo['CCD_FRAME']['WIDTH'] = dict()
        ccdinfo['CCD_FRAME']['HEIGHT'] = dict()

        ccdinfo['CCD_FRAME_TYPE'] = {
            'FRAME_LIGHT' : 1,
            'FRAME_BIAS'  : 0,
            'FRAME_DARK'  : 0,
            'FRAME_FLAT'  : 0,
        }

        ccdinfo['GAIN_INFO'] = {
            'current' : 0,
            'min'     : self._ccd_device.min_gain,
            'max'     : self._ccd_device.max_gain,
            'step'    : None,
            'format'  : None,
        }

        return ccdinfo


    def findCcd(self):
        # override
        # create FakeIndiCcd object here
        pass


    def findTelescope(self, *args):
        # override
        # create FakeIndiTelescope object here
        pass


    def findGps(self, *args):
        # override
        # create FakeIndiTelescope object here
        pass


    def configureCcdDevice(self, *args, **kwargs):
        # does nothing
        pass


    def configureTelescopeDevice(self, *args, **kwargs):
        # does nothing
        pass


    def configureGpsDevice(self, *args, **kwargs):
        # does nothing
        pass


    def getCcdTemperature(self):
        temp_val = -273.15  # absolute zero  :-)
        return temp_val


    def setCcdExposure(self, exposure, sync=False, timeout=None):
        # override
        pass


    def getCcdExposureStatus(self):
        # override
        # returns camera_ready, exposure_state
        pass



    def getCcdGain(self):
        return self._ccd_gain


    def setCcdGain(self, new_gain_value):
        self._ccd_gain = int(new_gain_value)

        # Update shared gain value
        with self.gain_v.get_lock():
            self.gain_v.value = int(new_gain_value)


    def setCcdBinning(self, new_bin_value):
        if type(new_bin_value) is int:
            new_bin_value = [new_bin_value, new_bin_value]
        elif type(new_bin_value) is str:
            new_bin_value = [int(new_bin_value), int(new_bin_value)]
        elif not new_bin_value:
            # Assume default
            return


        self._ccd_bin = int(new_bin_value[0])

        # Update shared gain value
        with self.bin_v.get_lock():
            self.bin_v.value = int(new_bin_value[0])



class FakeIndiDevice(object):

    def __init__(self):
        super(FakeIndiDevice, self).__init__()

        # these should be set
        self._device_name = 'UNDEFINED'
        self._driver_exec = 'UNDEFINED'


    @property
    def device_name(self):
        return self._device_name

    @device_name.setter
    def device_name(self, new_device_name):
        self._device_name = new_device_name


    @property
    def driver_exec(self):
        return self._driver_exec

    @driver_exec.setter
    def driver_exec(self, new_driver_exec):
        self._driver_exec = new_driver_exec


    def getDeviceName(self):
        return self._device_name


    def getDriverExec(self):
        return self._driver_exec



class FakeIndiCcd(FakeIndiDevice):

    def __init__(self):
        super(FakeIndiCcd, self).__init__()

        self._width = None
        self._height = None
        self._pixel = None

        self._min_gain = None
        self._max_gain = None

        self._min_exposure = None
        self._max_exposure = None

        self._cfa = None
        self._bit_depth = None


    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, new_width):
        self._width = int(new_width)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new_height):
        self._height = int(new_height)


    @property
    def pixel(self):
        return self._pixel

    @pixel.setter
    def pixel(self, new_pixel):
        self._pixel = float(new_pixel)


    @property
    def min_gain(self):
        return self._min_gain

    @min_gain.setter
    def min_gain(self, new_min_gain):
        self._min_gain = float(new_min_gain)


    @property
    def max_gain(self):
        return self._max_gain

    @max_gain.setter
    def max_gain(self, new_max_gain):
        self._max_gain = float(new_max_gain)


    @property
    def min_exposure(self):
        return self._min_exposure

    @min_exposure.setter
    def min_exposure(self, new_min_exposure):
        self._min_exposure = float(new_min_exposure)


    @property
    def max_exposure(self):
        return self._max_exposure

    @max_exposure.setter
    def max_exposure(self, new_max_exposure):
        self._max_exposure = float(new_max_exposure)


    @property
    def min_gain(self):
        return self._min_gain

    @min_gain.setter
    def min_gain(self, new_min_gain):
        self._min_gain = float(new_min_gain)


    @property
    def max_gain(self):
        return self._max_gain

    @max_gain.setter
    def max_gain(self, new_max_gain):
        self._max_gain = float(new_max_gain)


    @property
    def cfa(self):
        return self._cfa

    @cfa.setter
    def cfa(self, new_cfa):
        self._cfa = new_cfa


    @property
    def bit_depth(self):
        return self._bit_depth

    @bit_depth.setter
    def bit_depth(self, new_bit_depth):
        self._bit_depth = int(new_bit_depth)


class FakeIndiTelescope(FakeIndiDevice):

    def __init__(self):
        super(FakeIndiTelescope, self).__init__()

        self._lat = 0.0
        self._long = 0.0


    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, new_lat):
        self._lat = float(new_lat)


    @property
    def long(self):
        return self._long

    @long.setter
    def long(self, new_long):
        self._long = float(new_long)


class FakeIndiGps(FakeIndiDevice):

    def __init__(self):
        super(FakeIndiGps, self).__init__()

        self._lat = 0.0
        self._long = 0.0


    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, new_lat):
        self._lat = float(new_lat)


    @property
    def long(self):
        return self._long

    @long.setter
    def long(self, new_long):
        self._long = float(new_long)


