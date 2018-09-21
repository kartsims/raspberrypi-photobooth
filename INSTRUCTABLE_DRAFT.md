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

# Launch at startup

Add the following line to `/etc/rc.local` *just above the final `exit 0`*

```
python /opt/photobooth/main.py >> /opt/photobooth/logs/$(date +%Y-%m-%d).log 2>&1 &
```

# Launch at startup (systemd)

A executer en root :

```
cp /opt/photobooth/photobooth@.service /etc/systemd/user/
systemctl --user enable photobooth
```

# Disable screensaver

https://www.raspberrypi.org/forums/viewtopic.php?t=57552

# CPU temperature

```
/opt/vc/bin/vcgencmd measure_temp
```

# Configure as a Wifi AP

https://frillip.com/using-your-raspberry-pi-3-as-a-wifi-access-point-with-hostapd/

Install required packages

```
apt-get update && apt-get install hostapd dnsmasq iptables
```

Create a new file `/etc/hostapd/hostapd.conf`

```
# This is the name of the WiFi interface we configured above
interface=wlan0

# Use the nl80211 driver with the brcmfmac driver
driver=nl80211

# This is the name of the network
ssid=PHOTOBOOTH

# Use the 2.4GHz band
hw_mode=g

# Use channel 6
channel=6

# Enable 802.11n
ieee80211n=1

# Enable 40MHz channels with 20ns guard interval
ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]

# Accept all MAC addresses
macaddr_acl=0
```

Set as default config

- Open `/etc/default/hostapd`
- Find and replace `#DAEMON_CONF=` by `DAEMON_CONF=/etc/hostapd/hostapd.conf`

Configure dnsmasq

Backup original configuration

```
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
```

Put this in file `/etc/dnsmasq.conf`

```
interface=wlan0      # Use interface wlan0
listen-address=172.24.1.1 # Explicitly specify the address to listen on
bind-interfaces      # Bind to the interface to make sure we aren't sending things elsewhere
server=8.8.8.8       # Forward DNS requests to Google DNS
domain-needed        # Don't forward short names
bogus-priv           # Never forward addresses in the non-routed address spaces.
dhcp-range=172.24.1.50,172.24.1.150,12h # Assign IP addresses between 172.24.1.50 and 172.24.1.150 with a 12 hour lease time
```

Start services

```
service hostapd start
service dnsmasq start
```

Raspberry is accessible via the IP address `172.24.1.1` (ie. `ssh pi@172.24.1.1`)


# Install photo gallery

First, install npm and the Node Gallery

```
sudo apt-get install -y nodejs npm
cd /opt/photobooth/node-gallery
npm install
```

Test it
```
node app.js
```

If the console says `Listening on port 3000`, it's all good.

Add the following line to `/etc/rc.local`

```
node /opt/photobooth/node-gallery/app.js >> /opt/photobooth/logs/node-$(date +%Y-%m-%d).log 2>&1 &
```

Access the UI through
```
http://172.24.1.1:3000
```
