140424
======

_supercollider in more detail (soundfiles and sensor inputs)_

soundfiles
==========

```
s.boot

b= Buffer.loadDialog
b.plot //see that it loaded
b.numChannels //report number of channels
b.numFrames //how many samples
b.duration //how long (in seconds)

Ndef(\soundfile).play
Ndef(\soundfile, {PlayBuf.ar(b.numChannels, b, 1, loop:1)})

Ndef(\soundfile, {PlayBuf.ar(b.numChannels, b, 2, loop:1)}) //double as fast

Ndef(\soundfile, {PlayBuf.ar(b.numChannels, b, MouseX.kr(-2, 2), loop:1)}) //set playbackrate with mouse

Ndef(\soundfile, {PlayBuf.ar(b.numChannels, b, 1, MouseX.kr(0, 1)>0.5, MouseY.kr(0, b.numFrames))}) //trigger

//etc
```

bbb sensor data
===============

```
//test with beaglebone black broadcasting data from three sensors
NetAddr.langPort;//should return 57120
OSCFunc.trace(true);//posting all incoming osc data
OSCFunc.trace(false);//stop posting

(
Ndef.control(\temp);
Ndef.control(\button);
Ndef.control(\light);
Ndef.control(\accx);
Ndef.control(\accy);
Ndef.control(\accz);
OSCFunc({|msg|
	//msg.postln;//debug
	Ndef(\temp).source= msg[7];
	Ndef(\button).source= msg[6];
	Ndef(\light).source= msg[5];
	Ndef(\x).source= msg[4];
	Ndef(\y).source= msg[3];
	Ndef(\z).source= msg[2];
}, \broadcast);
)
```
