
PHOTOBOOTH_DIR="/opt/photobooth"
PHOTOBOOTH_LOG="/var/log/photobooth.log"

# check if user is root
# TODO

# download and install
cd /tmp
wget https://github.com/kartsims/raspberrypi-photobooth/archive/master.zip
unzip master.zip -d .
rm master.zip
mv raspberrypi-photobooth $PHOTOBOOTH_DIR

# add to startup
# TODO replace automatically with variable values
sudo sed -i '/^exit 0/ipython \/opt\/photobooth\/main.py >> \/var\/log\/photobooth.log &' /etc/rc.local
