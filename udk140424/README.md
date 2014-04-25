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
Ndef(\temp, {|val| Lag.kr(val, 1/50)});
Ndef(\button, {|val| Lag.kr(val, 1/50)});
Ndef(\light, {|val| Lag.kr(val, 1/50)});
Ndef(\accx, {|val| Lag.kr(val, 1/50)});
Ndef(\accy, {|val| Lag.kr(val, 1/50)});
Ndef(\accz, {|val| Lag.kr(val, 1/50)});
OSCFunc({|msg|
	msg.postln;//debug
	Ndef(\temp).set(\val, msg[7]);
	Ndef(\button).set(\val, msg[6]);
	Ndef(\light).set(\val, msg[5]);
	Ndef(\accx).set(\val, msg[4]);
	Ndef(\accy).set(\val, msg[3]);
	Ndef(\accz).set(\val, msg[2]);
}, \broadcast);
)


Ndef(\snd, {SinOsc.ar([400, 404]+(400*Ndef.kr(\temp)), 0, Ndef.kr(\button))}).play //use temperature as frequency and button as volume
```
