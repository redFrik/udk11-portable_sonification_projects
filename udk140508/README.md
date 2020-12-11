140508
======

_more supercollider (mic input)_

inspiration
===========
first some inspiration for today's exercises.  check these...

eargasm... https://www.youtube.com/watch?v=51ucXcWt-pg

world quantizer... https://www.youtube.com/watch?v=_cFtXS7g48A

both are 'scenes' for the rjdj app running on iphone (or sceneplayer on android).
rjdj is/was actually puredata and eargasm, world quantizer etc are relatively simple pd patches.
we can quite easily code the same thing with our beaglebone+supercollider setup.

another system written by [katja](www.katjaas.nl) in pure data is instant decomposer... https://www.youtube.com/watch?v=oML8PzMu3Zs
read more about it here... [slicejockey](https://www.katjaas.nl/slicejockey/slicejockey.html) and here... [beatdetection](https://www.katjaas.nl/beatdetection/beatdetection.html).
you can also download the pd patches and study them.

microphone cutup
================

```supercollider
//f0 sound detector - automatically record sound into buffers - with playback - originally written for av-programming udk class ws2011/12
//added more examples and feedback version for av-programming udk ss2014
(
z= 16;	//number of buffers in b
l= 2;	//length of buffers in seconds
x= false;	//mute recording
s.latency= 0.05;
s.waitForBoot{
	var detectorSynth, recorderSynths, responder;
	SynthDef(\f0SoundDetector, {|thresh= 0.075, time= 0.2|
		var input= SoundIn.ar;
		var off= DetectSilence.ar(input, thresh, time);
		var on= 1-off;				//invert
		var cnt= PulseCount.ar(on)%z+1;	//buffer index counter
		var changed= HPZ1.ar(on).abs>0;	//trigger
		SendTrig.ar(changed, 0, on*cnt);	//0= rec off, >0 rec start index
	}).add;
	SynthDef(\f0SoundRecorder, {|buf, t_trig= 0|
		var src= DelayN.ar(SoundIn.ar, 0.1, 0.1);	//compensate for detector latency
		RecordBuf.ar(src, buf, loop: 0, trigger: t_trig);
	}).add;
	SynthDef(\f0SoundPlayer, {|out= 0, buf, pan= 0, amp= 0.1, atk= 0.01, rel= 0.1, gate= 1, speed= 1|
		var env= EnvGen.ar(Env.asr(atk, amp, rel), gate, doneAction:2);
		var src= PlayBuf.ar(1, buf, speed, loop:1);
		Out.ar(out, Pan2.ar(src*env, pan));
	}).add;
	s.sync;
	b= {Buffer.alloc(s, s.sampleRate*l)}.dup(z);	//mono buffer
	s.sync;
	responder= OSCresponder(s.addr, \tr, {|t, r, m|
		var index= m[3].asInteger;
		if(x.not, {						//if not muted
			if(index>=1, {
				("recording"+index).postln;
				recorderSynths[index-1].set(\t_trig, 1);	//start sound recording
			}, {
				if(index==0, {
					"recording stopped".postln;
				});
			});
		});
	}).add;
	detectorSynth= Synth(\f0SoundDetector);
	recorderSynths= b.collect{|x| Synth(\f0SoundRecorder, [\buf, x])};
	CmdPeriod.doOnce({b.do{|x| x.free}; responder.remove});
	s.sync;
	Pdef(\pattern1).clear;
	Pdef(\pattern1).play(quant:1);
	Pdef(\pattern1, Pbind(
		\instrument, \f0SoundPlayer,
		\index, Pn(Pshuf((0..(z-1)), 4)),	//index selector, scramble every 4th time
		\buf, Pfunc({|ev| b[ev.index]}),
		\amp, 0.8,
		\dur, Pseq([0.25, 0.25, 0.5, 1], inf),
		\pan, Pwhite(-0.8, 0.8, inf),
		\speed, Prand([1, 1.2], inf)
	));
};
)

x= true;	//mute recording (stop collecting more)
x= false;	//unmute

(	//rewite the playback as it is running
	Pdef(\pattern1, Pbind(
		\instrument, \f0SoundPlayer,
		\index, Pseq((0..(z-1)), inf),	//index selector, played in order
		\buf, Pfunc({|ev| b[ev.index]}).trace,
		\amp, 0.8,
		\dur, Prand([0.25, 0.5, 1, 2, Pn(0.125, 4)], inf),
		\pan, Pwhite(-0.8, 0.8, inf),
		\speed, Prand([1, 1.25, 1.5, 1.75, 0.75, 0.5], inf)*Prand([1, -1], inf)	//back and forth
	));
)

(	//overlaps
	Pdef(\pattern1, Pbind(
		\instrument, \f0SoundPlayer,
		\index, Pseq((0..(z-1)), inf),	//index selector, played in order
		\buf, Pfunc({|ev| b[ev.index]}),
		\amp, [0.8, 0.5, 0.25, 0.125],
		\dur, Prand([0.25, 0.5, 1, 2, Pn(0.125, 4)], inf),
		\legato, 2,
		\pan, Pwhite(-0.8, 0.8, inf),
		\speed, Prand([1, 1.25, 1.5, 1.75, 0.75, 0.5], inf)*Prand([1, -1], inf)	//back and forth
	));
)

Pdef(\pattern1).stop

```

feedback cutup
==============
now the same thing but cutting up the output of the beatcutter itself.  so it's a feedback system.

```supercollider
//f0 sound detector FB - feedback version - cutting up itself
//you will need to trigger it with some input sounds - see sine and noise below
(
z= 16;	//number of buffers in b
l= 2;	//length of buffers in seconds
x= false;	//mute recording
s.latency= 0.05;
s.waitForBoot{
	var detectorSynth, recorderSynths, responder;
	SynthDef(\f0SoundDetectorFB, {|thresh= 0.075, time= 0.2|
		var input= InFeedback.ar;//note: here was mic input before
		var off= DetectSilence.ar(input, thresh, time);
		var on= 1-off;				//invert
		var cnt= PulseCount.ar(on)%z+1;	//buffer index counter
		var changed= HPZ1.ar(on).abs>0;	//trigger
		SendTrig.ar(changed, 0, on*cnt);	//0= rec off, >0 rec start index
	}).add;
	SynthDef(\f0SoundRecorderFB, {|buf, t_trig= 0|
		var src= DelayN.ar(InFeedback.ar, 0.1, 0.1);	//note: here was mic input before
		RecordBuf.ar(src, buf, loop: 0, trigger: t_trig);
	}).add;
	SynthDef(\f0SoundPlayer, {|out= 0, buf, pan= 0, amp= 0.1, atk= 0.01, rel= 0.1, gate= 1, speed= 1|
		var env= EnvGen.ar(Env.asr(atk, amp, rel), gate, doneAction:2);
		var src= PlayBuf.ar(1, buf, speed, loop:1);
		Out.ar(out, Pan2.ar(src*env, pan));
	}).add;
	s.sync;
	b= {Buffer.alloc(s, s.sampleRate*l)}.dup(z);	//mono buffer
	s.sync;
	responder= OSCresponder(s.addr, \tr, {|t, r, m|
		var index= m[3].asInteger;
		if(x.not, {						//if not muted
			if(index>=1, {
				("recording"+index).postln;
				recorderSynths[index-1].set(\t_trig, 1);	//start sound recording
			}, {
				if(index==0, {
					"recording stopped".postln;
				});
			});
		});
	}).add;
	detectorSynth= Synth(\f0SoundDetectorFB);
	recorderSynths= b.collect{|x| Synth(\f0SoundRecorderFB, [\buf, x])};
	CmdPeriod.doOnce({b.do{|x| x.free}; responder.remove});
	s.sync;
	Pdef(\pattern1).clear;
	Pdef(\pattern1).play(quant:1);
	Pdef(\pattern1, Pbind(
		\instrument, \f0SoundPlayer,
		\index, Pn(Pshuf((0..(z-1)), 4)),	//index selector, scramble every 4th time
		\buf, Pfunc({|ev| b[ev.index]}),
		\amp, 1,
		\dur, Pseq([0.25, 0.25, 0.5, 1], inf),
		\pan, Pwhite(-0.8, 0.8, inf),
		\speed, Prand([1, 1.2], inf)
	));
};
)

//--here some simple synths to kickstart the feedback system.
//run them and wait a little bit in between each.
//then let the system work for itself for a while.
//you can add more sounds (your own) when you like.
{WhiteNoise.ar(Line.kr(1, 0, 1, doneAction:2))!2}.play//warning - loud
{BrownNoise.ar(Line.kr(0, 1, 1, doneAction:2))!2}.play//warning - loud
{SinOsc.ar([400, 404], 0, Line.kr(1, 0, 2, doneAction:2))}.play//loud


//or rewrite the pattern...
(
Pdef(\pattern1, Pbind(
		\instrument, \f0SoundPlayer,
	\index, Pseq((0..(z-1)), inf),	//index selector, scramble every 4th time
		\buf, Pfunc({|ev| b[ev.index]}),
		\amp, 1,
\legato, 2,
		\dur, 0.4,
		\pan, Pwhite(-0.8, 0.8, inf),
		\speed, Prand([1, 1.2, 0.9], inf)
	));
)

(
Pdef(\pattern1, Pbind(
		\instrument, \f0SoundPlayer,
	\index, Pseq((0..(z-1)), inf),	//index selector, scramble every 4th time
		\buf, Pfunc({|ev| b[ev.index]}),
		\amp, 1,
\legato, 0.5,
		\dur, 0.25,
		\pan, Pwhite(-0.8, 0.8, inf),
		\speed, Pseq([1, 1.01, 0.99], inf)
	));
)

Pdef(\pattern1).stop
```
