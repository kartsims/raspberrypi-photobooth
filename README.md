Turn a RaspberryPi into the perfect photobooth

> Inspired by [this Python script](https://github.com/da-steve101/photobooth) and [Adafruit's Pi Cam example using PiTFT](https://github.com/adafruit/adafruit-pi-cam)


# How to start the photobooth

```
python photobooth.py
```

# Install on Raspbian Jessie Lite


Install X Server for graphical display

```
sudo apt-get install -y --no-install-recommends xserver-xorg
sudo apt-get install -y --no-install-recommends xinit
sudo apt-get install -y lxde-core
```

Install Python dependencies

```
sudo apt-get install -y python3 python3-picamera
```

Install the photobooth software

```
mkdir ~/raspberrypi-photobooth
cd ~/raspberrypi-photobooth
wget https://github.com/kartsims/raspberrypi-photobooth/archive/master.zip
unzip master.zip
rm master.zip
```

# Improvements

Load at startup

```
# TODO
```
