Required

- Raspberry Pi 2 or 3 (not tested on v1)
- Raspberry Cam (tested with v2)
- micro SD card
- Screen (+ HDMI cable, or in my case VGA cable + VGA to HDMI adapter)

Optional :
- push button
- photo printer


First, prepare your Raspbian SD card
- Download official Raspbian image
- Flash the SD card (using Etcher is the simplest way I know, and works on Linux/Mac and Windows)
- Enable SSH by writing a file named "ssh" in the "boot/" directory

SD card ready ? Let's get the Pi started !
- Connect the camera
- Connect the screen
- Insert the SD card (obviously)
- Turn the power on

At this point, you should see the screen filled with the usual black screen and end up with a blinking cursor asking for your login.

Great, now that the Pi is up and running, we need to configure it. We will need two things : Internet and a terminal prompt.

Get Internet to your Pi :
Easiest way is to plug in an Ethernet cable from your router/box to your Pi. Instant access. See at the end of this tutorial how to set up Wifi.

Terminal prompt :

via SSH :
On Linux and OSX, the Terminal app is built in and can be accessed as every other app.
On windows, ...?

via physical interface (aka keyboard) :
Just plug in a USB keyboard, duh.


Configure your screen resolution

Following guidelines provided by the official Pi website (https://www.raspberrypi.org/documentation/configuration/config-txt.md)

Screen resolution can be set in `/boot/config.txt`

First, find which resolution is available for your screen :

- Edit /boot/config.txt and uncomment the following lines

```
#hdmi_group=1
#hdmi_mode=1
```

- Reboot

```
sudo reboot
```

- Run this command to get the list of resolutions available

```
/opt/vc/bin/tvservice -m DMT
```

I got the following output on mine (4/3 old monitor)

```
Group DMT has 8 modes:
           mode 4: 640x480 @ 60Hz 4:3, clock:25MHz progressive
           mode 6: 640x480 @ 75Hz 4:3, clock:31MHz progressive
           mode 9: 800x600 @ 60Hz 4:3, clock:40MHz progressive
           mode 11: 800x600 @ 75Hz 4:3, clock:49MHz progressive
           mode 16: 1024x768 @ 60Hz 4:3, clock:65MHz progressive
           mode 18: 1024x768 @ 75Hz 4:3, clock:78MHz progressive
           mode 35: 1280x1024 @ 60Hz 5:4, clock:108MHz progressive
           mode 36: 1280x1024 @ 75Hz 5:4, clock:135MHz progressive
```

You want to pick a low resolution, because the Pi is not fast enough to render smoothly the cam images as a video for high resolution.

In my case, I'll go for the lowest resolution 640x480, and lowest frequency. That is the first line of the output.

```
mode 4: 640x480 @ 60Hz 4:3, clock:25MHz progressive
```

- Now back to edit `/boot/config.txt` and choose mode #4 (the one displayed above)

```
hdmi_group=2
hdmi_mode=4
```
Note : hdmi_group = 2 is just the DMT mode, more info on the raspberry [config.txt page](https://www.raspberrypi.org/documentation/configuration/config-txt.md)

- Final reboot and you should see on your screen the updated resolution.

- If everything looks fine, it is time to update your `config.py` file with the new value. Edit the `config.py` file and update the following line

```
# enter here your screen resolution (will be used for the camera preview images)
SCREEN_RESOLUTION = 640, 480
```

In my case my resolution is `640x480` so it is already set, nothing to do here. If you have to change this value, remember to write `640, 480` with a COMMA otherwise the Python script will crash.
