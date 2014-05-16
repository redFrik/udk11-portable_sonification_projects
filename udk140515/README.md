140515
======

_installing and preparing a system on the beaglebone black_

for this you will need a beaglebone black (bbb), an sd-card, one mini usb cable, headphones, and a usb soundcard.

installing debian linux
--

download the latest debian image... http://beagleboard.org/latest-images/ (Debian (BeagleBone, BeagleBone Black - 2GB SD) 2014-04-23)

mac osx: extract the .xy image with 'the unarchiver' or similar.

mac osx: use Pi Filler <http://ivanx.com/raspberrypi/> or similar to copy over the image.

on windows you can use win32diskimager <http://sourceforge.net/projects/win32diskimager/>

there are good general instructions here... https://learn.adafruit.com/beaglebone-black-installing-operating-systems/overview

starting for the first time
--

insert the micro sdcard in the bbb, connect mini usb cable to computer and it should start booting up - check the blue leds.

open terminal/console application on you laptop and type `ssh debian@beaglebone.local` and the default password is `temppwd`.

```
//new debian bbb image bone-debian-7.4-2014-04-23-2gb.img
//onto a 8gb card
//ssh debian@beaglebone.local #log in with temppwd from you laptop

sudo passwd debian #and change it to something easy that you will remember
date
sudo dpkg-reconfigure tzdata
echo 'export LC_ALL="en_US.UTF-8"' >> ~/.bashrc

//—expand filesystem
df # show something like 97% full
sudo /opt/scripts/tools/grow_partition.sh
sudo reboot # and log in again
df # should now show a lot more free space

sudo apt-get update
sudo apt-get upgrade

//—install python osc
git clone git://gitorious.org/pyosc/devel.git
cd devel
sudo ./setup.py install
cd ..
sudo rm -r devel

//—hostname
echo mybbb > /etc/hostname #pick a useful name instead of mybbb
sudo pico /etc/hosts #and edit 127.0.1.1 to match mybbb (or what ever name you picked)

//—optional: disable hdmi and emmc
sudo mkdir /mnt/boot
sudo mount /dev/mmcblk0p1 /mnt/boot
sudo pico /mnt/boot/uEnv.txt
uncomment the following line… (Disable HDMI/eMMC)
capemgr.disable_partno=BB-BONELT-HDMI,BB-BONELT-HDMIN,BB-BONE-EMMC-2G
sudo reboot

//—optional: turn off some services
sudo systemctl disable cloud9.socket
sudo systemctl disable bonescript-autorun.service
sudo systemctl disable bonescript.socket
sudo systemctl enable multi-user.target

//—optional: automatic startup service
sudo pico /lib/systemd/system/mystartup.service
	[Unit]
	Description=Start a pythonscript at boot
	[Service]
	WorkingDirectory=/home/debian/
	ExecStart=/usr/bin/python myscript.py
	SyslogIdentifier=mystartup
	Restart=on-failure
	RestartSec=5
	[Install]
	WantedBy=multi-user.target
sudo systemctl enable /lib/systemd/system/mystartup.service

//—install jack
sudo apt-get install libsamplerate0-dev libsndfile1-dev libreadline-dev cmake libxt-dev gcc-4.7 g++-4.7
sudo apt-get remove --auto-remove gcc-4.6
sudo ln -s /usr/bin/gcc-4.7 /usr/bin/gcc
sudo ln -s /usr/bin/g++-4.7 /usr/bin/g++
sudo apt-get clean
git clone git://github.com/jackaudio/jack2.git
cd jack2
./waf configure --alsa
./waf build
sudo ./waf install
cd ..
sudo rm -r jack2
sudo ldconfig

//—install sc3.7
git clone --recursive git://github.com/supercollider/supercollider.git supercollider
cd supercollider
git checkout c7600cc1c9
#git checkout ddd8c8d75dd00263acf593b062ecbb06686a4574
git submodule init && git submodule update
mkdir build && cd build
cmake -L -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF -DSSE=OFF -DSSE2=OFF -DSUPERNOVA=OFF -DNOVA_SIMD=ON -DNATIVE=OFF -DSC_QT=OFF -DSC_WII=OFF -DSC_ED=OFF -DSC_IDE=OFF -DSC_EL=OFF -DCMAKE_C_FLAGS="-march=armv7-a -mtune=cortex-a8 -mfloat-abi=hard -mfpu=neon" -DCMAKE_CXX_FLAGS="-march=armv7-a -mtune=cortex-a8 -mfloat-abi=hard -mfpu=neon" ..
make
sudo make install
sudo ldconfig
cd ../..
sudo rm -r supercollider
sudo pico /usr/local/share/SuperCollider/SCClassLibrary/Common/GUI/Base/QtGUI.sc #comment out:
	//this.style = "Plastique";
	//this.palette = QPalette.light;
sudo pico /usr/local/share/SuperCollider/SCClassLibrary/Common/GUI/Base/QFont.sc #comment out:
	//defaultSansFace = this.prDefaultFamilyForStyle(0);
	//defaultSerifFace = this.prDefaultFamilyForStyle(1);
	//defaultMonoFace = this.prDefaultFamilyForStyle(2);
sudo reboot

//—optional: connecting an usb wlan adapter
sudo pico /etc/network/interfaces
	auto wlan0
	iface wlan0 inet dhcp
		wpa-ssid "your_wlan_name" #Medienhaus R112
		wpa-psk "your_wlan_pass" #_the_password_
		wireless-power off
sudo ifup wlan0

//—optional: install python twitter library
sudo pip install twython

//—test alsa
speaker-test -Ddefault:CARD=Device # should play sound through usb soundcard

//—realtime
sudo pico /etc/security/limits.conf
#add the following the the end of the file
@audio - memlock 256000
@audio - rtprio 95

//-test sc
sudo jackd -P95 -dalsa -dhw:1,0 -p1024 -n3 -s &
sudo sclang
> s.boot
> a= {SinOsc.ar([400,404],0,0.1)}.play

//—optional: save some diskspace
sudo rm -r /usr/share/opencv
sudo rm -r /usr/share/desktop-*
sudo rm -r /usr/share/kde4
sudo rm -r /usr/share/lxde
sudo rm -r /usr/share/java
sudo rm -r /usr/share/gnome*
sudo rm -r /usr/share/wallpapers
sudo rm -r /usr/share/doc
sudo rm -r /usr/share/man
sudo rm -r /usr/share/locale

//—supercollider automatic startup
sudo pico /usr/local/share/SuperCollider/SCClassLibrary/DefaultLibrary/Main.sc
#and add to the run method…
"/home/debian/mysc.scd".load;

sudo crontab -e #and add…
@reboot /bin/bash /home/debian/autostart.sh

pico autostart.sh
	#!/bin/bash
	/usr/local/bin/jackd -P95 -dalsa -dhw:1,0 -p1024 -n3 -s &
	/usr/local/bin/scsynth -u 57110 &
	/usr/local/bin/sclang -rD >> /home/debian/temp.log
chmod +x autostart.sh

//—minimal mysc.scd file:
pico mysc.scd
	s.serverRunning= true;
	s.initTree;
	"sudo jack_connect system:capture_1 SuperCollider:in_1 &".unixCmd;
	"sudo jack_connect SuperCollider:out_1 system:playback_1 &".unixCmd;
	"sudo jack_connect SuperCollider:out_2 system:playback_2 &".unixCmd;
	a= {SinOsc.ar([400,404],0,0.2)}.play;
```
