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
