140424
======

_supercollider in more detail (soundfiles and sensor inputs)_


python - sensor input (also output like led control, pwm for servos etc)

supercollider - sound (filtering and interpreting sensor data, logic)


soundfiles
==========

```supercollider
//boot the server and load two soundfiles into two buffers
s.boot
b= Buffer.loadDialog(s)
c= Buffer.read(s, "/Applications/SuperCollider344/sounds/OrchTuning01.wav")


b.play
b.plot //careful - only plot short files
c.play

b.numChannels //report number of channels
b.numFrames //how many samples
b.duration //how long (in seconds)

//the second buffer
c.numChannels
c.numFrames
c.duration


Ndef(\looper).play

Ndef(\looper, {PlayBuf.ar(b.numChannels, b.bufnum, 1, 1, 0, 1)})
Ndef(\looper, {PlayBuf.ar(b.numChannels, b.bufnum, -1, 1, 0, 1)})
Ndef(\looper, {PlayBuf.ar(b.numChannels, b.bufnum, 0.75, 1, 0, 1)})
Ndef(\looper, {PlayBuf.ar(b.numChannels, b.bufnum, 1.4, 1, 0, 1)})
//etc

//make changes with a crossfade (here 8 sec)
Ndef(\looper).fadeTime= 8
Ndef(\looper, {PlayBuf.ar(b.numChannels, b.bufnum, -0.4, 1, 0, 1)})
Ndef(\looper, {PlayBuf.ar(b.numChannels, b.bufnum, 1.8, 1, 0, 1)})
Ndef(\looper, {PlayBuf.ar(b.numChannels, b.bufnum, 8, 1, 0, 1)})

Ndef(\looper).release(10) //end in 10 seconds

b.free
c.free
Ndef(\looper).clear
//--
```


```supercollider
//again
s.boot
d= Buffer.loadDialog(s)
d.play


Ndef(\chaos).play
Ndef(\chaos).fadeTime= 5 //five seconds crossfade
Ndef(\chaos, {PlayBuf.ar(d.numChannels, d.bufnum, MouseX.kr(-2, 2), 1, 0, 1)}) //interactive

Ndef(\chaos, {PlayBuf.ar(d.numChannels, d.bufnum, LFNoise2.kr(50)*2, 1, 0, 1)}) //"standalone"

Ndef(\chaos, {PlayBuf.ar(d.numChannels, d.bufnum, SinOsc.ar(SinOsc.ar(SinOsc.ar(0.01)))*2, 1, 0, 1)}) //simple swing

Ndef(\chaos, {PlayBuf.ar(d.numChannels, d.bufnum, PlayBuf.kr(d.numChannels, d.bufnum, 1, 1, 0, 1)*2, 1, 0, 1)}) //modulation of itself
Ndef(\chaos).release

d.plot
Ndef(\maschine).play
Ndef(\maschine, {PlayBuf.ar(d.numChannels, d.bufnum, 1, MouseX.kr(0, 1)>0.5, d.numFrames/2)})

Ndef(\maschine, {PlayBuf.ar(d.numChannels, d.bufnum, 1, MouseX.kr(0, 1)>0.5, MouseY.kr(0, d.numFrames))})


Ndef(\maschine, {PlayBuf.ar(d.numChannels, d.bufnum, 1, SinOsc.kr(2), SinOsc.kr(0.1)* d.numFrames)})

Ndef(\maschine, {PlayBuf.ar(d.numChannels, d.bufnum, 1, SinOsc.kr(SinOsc.kr(0.1)*8), SinOsc.kr(0.1)* d.numFrames)})
```


```supercollider
//last time same thing

e= Buffer.loadDialog(s)
Ndef(\soundfile).play
Ndef(\soundfile, {PlayBuf.ar(e.numChannels, e.bufnum, 1, loop:1)})

Ndef(\soundfile, {PlayBuf.ar(e.numChannels, e.bufnum, 2, loop:1)}) //double as fast

Ndef(\soundfile, {PlayBuf.ar(e.numChannels, e.bufnum, MouseX.kr(-2, 2), loop:1)}) //set playbackrate with mouse

Ndef(\soundfile, {PlayBuf.ar(e.numChannels, e.bufnum, 1, MouseX.kr(0, 1)>0.5, MouseY.kr(0, e.numFrames))}) //trigger

//etc
```


bbb sensor data
===============

```supercollider
//test with beaglebone black broadcasting data from three sensors
//NOTE: this will not work without the bbb running in the classroom

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

Ndef(\snd, {SinOsc.ar([400, 404]+(400*Ndef.kr(\temp)), 0, Ndef.kr(\button).lag(1))}).play //with a one second lag
Ndef(\snd).stop

Ndef(\newlooper).play
Ndef(\newlooper, {PlayBuf.ar(d.numChannels, d.bufnum, Ndef.kr(\light)*2+1, 1, 0, 1)})

Ndef(\newlooper, {PlayBuf.ar(d.numChannels, d.bufnum, Ndef.kr(\accx).linlin(0.28, 0.69, 2, 20).lag(1), 1, 0, 1)})

```
