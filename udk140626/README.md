140626
======

_own projects_

extra: install puredata
--
this will install pd-vanilla on the beaglebone black.

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install puredata
```

to try it out copy the two simple test patches found in this folder (sinetest.pd and mictest.pd) to the bbb.  on your laptop do:
```bash
cd udk140626 #or where ever you have stored the two patches on your machine
scp sinetest.pd debian@beaglebone.local:/home/debian/sinetest.pd
scp mictest.pd debian@beaglebone.local:/home/debian/mictest.pd
```

then connect usb soundcard + headphones + mic, log in to the bbb and try these two - one after the other and use ctrl+c to quit in between.

```bash
pd -nogui -audiodev 4 -rt sinetest.pd
pd -nogui -audiodev 4 -rt mictest.pd
```

note: you will need a [loadbang] + [del 500] to start dsp.  sound will not start without this little extra delay when running pd as headless.
