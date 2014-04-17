general course introduction
--------------------

* links to previous semesters... <http://redfrik.github.io/udk00-Audiovisual_Programming/>
* and dates + times for this course... <https://github.com/redFrik/udk11-Portable_sonification_projects> <-save this page
* no need to buy any hardware - the mini computers and other stuff will be provided as a loan

140417
======

_introduction to sensors, sonification and supercollider_

sensors
=======

let's make a list of different types of sensors / inputs / detectors.

then see [arduino playground](http://playground.arduino.cc/Main/InterfacingWithHardware#InputTOC) for a great overview.  and for more inspiration look at sensors category at for example [sparkfun](https://www.sparkfun.com/categories/23) or [adafruit](http://www.adafruit.com/category/35).

* [LDR](http://en.wikipedia.org/wiki/Photodetector) (aka light sensors or photodetectors - most often a light dependent resistors but can also be a photodiode / light sensitive transistor)
* IR sensors (infra red light - you can find them in printers)
* UV sensors (ultraviolet light)
* DIY light sensors with colour filters (add pieces of thin plastic film in front of the LDR)

* webcamera (but to do serious tracking you often need to use standard software / systems like [tuio](http://tuio.lfsaw.de) or [open cv](http://opencv.org) and then run it within python, max, processing, pd etc)
* radioactive source + webcam (ref. David's project last year)
* webcamera used as a single colour sensor (a bit of an overkill but works well and is easy to set up)
* [kinect](http://en.wikipedia.org/wiki/Kinect) (3d scenery - can track people very well - but need a fast computer)
* [leap motion](http://www.onformative.com/lab/leapmotionp5/) (works like a miniature kinect - 3d - good for hand gestures)

* electret mic (with sound analysis in computer - track things like loudness, pitch, timbre, chords, tempo etc etc - voice analysis possible but hard)
* piezo (aka contact mic - also works as knock, shock or vibration detector)
* springs (can act as cheap vibration/shock sensors - DIY with a spring inside a metal tube - ultra cheap)

* switches (with one or more states)
* buttons (momentary connection)
* potentiometers (knobs, sliders etc.)
* rotary encoders (a knob that can turn endless - used for detecting turns, velocity and direction)

* conductive thread/yarn (silver particles come closer when the yarn is stretched and thereby gives less resistance)
* [conductive fabric](http://www.instructables.com/id/Flexible-Fabric-Pressure-Sensor/)
* conductive paint/ink (might be used as resistive sensors)
* conductive foam (aka anti-static foam - usually black)

* reed switches (magnetic switches - digital - use a magnet to switch them on - cheap and reliable - range up to around 10cm depending on magnet strength)
* hall effect sensor (also magnetic - analog - often used in spinning wheels to detect number or laps or speed - no physical contact needed)
* [EMF](http://www.instructables.com/id/Arduino-EMF-Detector/) (use a single bare wire to detect electromagnetic fields - works like an antenna)
* [theremin](http://en.wikipedia.org/wiki/Theremin) (proximity)

* thermistor (temperature)

* bend sensors (often used in ['powergloves'](http://en.wikipedia.org/wiki/Power_Glove) - not working so well in my experience)

* [FSR](http://www.openmusiclabs.com/learning/sensors/fsr/) like the 3M touch sensor (FSR = force sensitive resistors - works very well - also to embedded and put under things)
* [DIY pressure sensor](http://www.instructables.com/id/Stickytape-Sensors/)

* tilt sensor / mercury switch (cheap and can also build them yourself - basically just a metal ball and a plastic tube)

* accelerometer (one to three axis - with analog and digital interface, a common analog one is [ADXL335](https://www.sparkfun.com/products/9269) and a digital one is [ADXL345](https://www.sparkfun.com/products/9836))
* magnetometers (aka compass)
* gyroscope
* [IMU](http://www.instructables.com/id/Accelerometer-Gyro-Tutorial/?ALLSTEPS) (inertial measurement unit - basically a combination of the three above - gives 6DOF, 9DOF, etc - DOF = degrees of freedom)

* SDR (software defined radio - can track things like satellites, mobiles, police radio, airplanes etc etc - try the [funcube dongle](http://www.funcubedongle.com) or [rtl-sdr](http://sdr.osmocom.org/trac/wiki/rtl-sdr) (cheap tv-tuner used for sdr))

* [inductive charger](http://www.adafruit.com/products/1407) (can be used as a sensor in combo with a current sensor)
* [current sensors](http://www.adafruit.com/products/904) (measure power consumption - also household power meters etc - in circuit or as a clamp meter that you can put around the cable - both AC and DC)
* voltage (it's easy to read voltage directly with an analog input - though take care not to exceed the maximum (1.8v on bbb, 5v on arduino) - use voltage dividers / optoisolators for protection)

* RFID (for example the [id-20](https://www.sparkfun.com/products/11828) together with a small breakout board - passive tags - great and the tags are cheap - note the different frequencies - 125khz is a common standard)
* NFC (near field communication - read and write data to tags - reader often built into mobiles - active tags - drawback is that the tags are more expensive)

* [emotive](http://emotiv.com) (read brainwaves - EEG)
* [GSR](http://www.cooking-hacks.com/galvanic-skin-response-sensor-gsr-sweating-ehealth-medical) (galvanic skin response - aka lie detector)
* [EMG](https://www.sparkfun.com/products/11776) (electromyography - muscle tension)
* [heart/pulse sensor](https://www.sparkfun.com/products/11574) (also easy to DIY - most often just a simple ir-sensor that you clip on to a finger or ear)

* gas (lots of different types)
* smell (?)
* smoke detector (?)
* chemical detectors / chemistry sensors (?)

* GPS (global positioning system - only work outdoors - built into mobiles but also available as modules)
* GSM (crude positioning using triangulation)
* [DC77](http://en.wikipedia.org/wiki/DCF77) (clock signal sent out from frankfurt - DIY receiver or kit (available at segor))

* ultrasound (good for proximity - used in cars)

* using data from online sensors and databases (twitter feeds, weather data etc...)

* hijack the sensors in your mobile (try out the app [androsensor](https://play.google.com/store/apps/details?id=com.fivasim.androsensor) on android or [sensor monitor](https://sites.google.com/a/fuzzface.net/app//sensor-monitor) on iphone)

sonification
============

discuss.

inspiration: biohacking / sensory expansion: <https://www.youtube.com/watch?v=a-Dv6dDtdcs> (part2 @ 3:00 talk about magnet sensors implanted in fingertips)

supercollider
=============

official homepage: [http://supercollider.github.io]

```
s.boot

Ndef(\test).play
Ndef(\test, {LFSaw.ar([400,400], 0, MouseX.kr(0, 0.5))})
Ndef(\test, {LFSaw.ar(MouseY.kr(100, 4000, 'exponential'), 0, MouseX.kr(0, 0.5))})

s.scope
```

```
//test with beaglebone black broadcasting data from three sensors
NetAddr.langPort;//should return 57120
OSCFunc.trace(true);//posting all incoming osc data
OSCFunc.trace(false);//stop posting

o= OSCFunc({|msg| msg.postln}, \broadcast)

(
s.waitForBoot{
	Ndef.control(\temp);
	Ndef.control(\button);
	Ndef.control(\light);
	OSCFunc({|msg|
		//msg.postln;//debug
		Ndef(\temp).source= msg[7];
		Ndef(\button).source= msg[6];
		Ndef(\light).source= msg[5];
	}, \broadcast);

	Ndef(\snd).play;
	Ndef(\snd, {SinOsc.ar([400, 400+(Ndef.kr(\light).lag(1)*4)], 0, 0.1)});
};
)
```
