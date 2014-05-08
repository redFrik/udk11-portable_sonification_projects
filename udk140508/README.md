140508
======

_more supercollider (mic input) and some python_


```
//f0 sound detector - automatically record sound into buffers - with playback - originally written for av-programming udk class ws2011/12
//added more examples for av-programming udk ss2014
(
z= 16;	//number of buffers in b
l= 2;	//length of buffers in seconds
x= false;	//mute recording
Server.default= s= Server.local;
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

/*
x= true;	//mute recording (stop collecting more)
x= false;	//unmute
*/

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
