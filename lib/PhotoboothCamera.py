import picamera
import atexit
import io
import time
import yuv2rgb
from config import *

# Buffers for viewfinder data
rgb = bytearray(SCREEN_RESOLUTION[0] * SCREEN_RESOLUTION[1] * 3)
yuv = bytearray(SCREEN_RESOLUTION[0] * SCREEN_RESOLUTION[1] * 3 / 2)

class PhotoboothCamera:
    def __init__(self):
        self.lastPhoto = None

        # init Pi camera
        if CAMERA_TYPE == 'picamera':
            self.cam = picamera.PiCamera()
            self.cam.resolution = SCREEN_RESOLUTION
            self.cam.rotation = CAMERA_ROTATION
            self.cam.crop = CAMERA_CROP
            # close camera when script is exited
            atexit.register(self.cam.close)

        # if other types of camera should be supported, code would go here


    # get the camera's image in a stream
    def preview(self):
        stream = io.BytesIO()
        self.cam.capture(stream, use_video_port=True, format='raw')
        stream.seek(0)
        stream.readinto(yuv)
        stream.close()
        yuv2rgb.convert(yuv, rgb, SCREEN_RESOLUTION[0],
        SCREEN_RESOLUTION[1])
        return rgb[0: (SCREEN_RESOLUTION[0] * SCREEN_RESOLUTION[1] * 3)]

    def takePicture(self):
    	filepath = PHOTOS_DIR + "PHOTOBOOTH-" + time.strftime("%Y%m%d-%H%M%S") + ".jpg"
        print "Saving picture to %s" % filepath
    	scaled = None
    	self.cam.resolution = CAMERA_RESOLUTION
    	self.cam.crop = CAMERA_CROP
        # TODO something so that the photo is not taken right after changing the settings, bc the camera can't adjust
    	try:
    		self.cam.capture(filepath, use_video_port=False, format='jpeg', thumbnail=None)
    		self.lastPhoto = filepath

    	finally:
    		# TODO add error handling/indicator (disk full, etc.)
    		self.cam.resolution = SCREEN_RESOLUTION
    		self.cam.crop = CAMERA_CROP

    	return filepath
