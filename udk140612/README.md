140612
======

_panning sounds and multi channel speaker setups_


speaker tests
--
two useful tools to keep around and easily accessible.

```
//my speaker test - noise!
(
var channels= [0, 1]; //edit here for multi channel tests e.g. [0, 1, 2, 3, 4, 5] for a 6ch system
var amp= 0.5;
s.waitForBoot{

	SynthDef(\speakertest, {|out= 0, amp= 0.5|
		var env= EnvGen.kr(Env.perc(0.01, 0.5), doneAction:2);
		var src= PinkNoise.ar;
		Out.ar(out, src*env*amp);
	}).add;

	s.sync;

	Pbind(\instrument, \speakertest, \out, Pseq(channels, inf), \amp, amp).play;
};
)

//my speaker test2 - tones!
(
var channels= [0, 1]; //edit here for multi channel tests e.g. [0, 1, 2, 3] for a 4ch system
var amp= 0.5;
s.waitForBoot{

	SynthDef(\speakertest2, {|out= 0, amp= 0.5, freq= 400|
		var env= EnvGen.kr(Env.perc(0.01, 0.5), doneAction:2);
		var src= SinOsc.ar(freq);
		Out.ar(out, src*env*amp);
	}).add;

	s.sync;

	Pbind(\instrument, \speakertest2, \out, Pseq(channels, inf), \amp, amp, \degree, Pseq(channels, inf)).play;
};
)
```



redSys quark
--
my personal speaker tests.  i have put the tests into classes to have them hidden but still directly available.  i just type...
```
RedTest.speaker([0, 1, 2, 3, 4, 5])
RedTest.speaker2([0, 1, 2, 3])
```
to try out the speakers.  these are the sc classes i use every time i set up for a concert, lecture, talk or workshop.

to try them out install the redSys quark by `Quarks.install("redSys");`.  but i encourage you to write your own.

panning
--
```
s.boot

(
SynthDef(\pantest1, {|out= 0|
	var src= PinkNoise.ar(0.1);
	Out.ar(out, Pan2.ar(src, MouseX.kr(-1, 1)));
}).add;
)

Synth(\pantest1)


(
SynthDef(\pantest2, {|out= 0|
	var src= PinkNoise.ar(0.1);
	Out.ar(out, Pan2.ar(src, LFTri.ar(100)));
}).add;
)

Synth(\pantest2)


(
SynthDef(\pantest3, {|out= 0|
	var src= SinOsc.ar(400);
	Out.ar(out, Pan2.ar(src, LFTri.ar(3000)));
}).add;
)

Synth(\pantest3)


(
SynthDef(\pantest4, {|out= 0|
	var pan= PinkNoise.ar(1);
	var src= SinOsc.ar(400+(pan*100)); //389 hz left, 411 hz right
	Out.ar(out, Pan2.ar(src, pan));
}).add;
)

Synth(\pantest4)
```

pingpong delay
--
```
PingPong //look at helpfile and compare to your version
```

```
(
SynthDef(\pingpongeffect, {|in= 0|
	var src= InFeedback.ar(in, 1);
	var del1= DelayN.ar(src*0.5, 0.25, 0.25);
	var del2= DelayN.ar(src*0.4, 0.5, 0.5);
	var del3= DelayN.ar(src*0.3, 0.756, 0.756);
	var del4= DelayN.ar(src*0.2, 1.01, 1.01);
	var del5= DelayN.ar(src*0.1, 1.23, 1.23);
	Out.ar(0, Pan2.ar(del1+del3+del5, -1)+Pan2.ar(del2+del4, 1));
}).add;
)

{SoundIn.ar}.play(outbus:40)
Synth(\pingpongeffect, [\in, 40])
Pbind(\dur, 4, \legato, 0.1, \out, 42, \amp, 0.5).play
Synth(\pingpongeffect, [\in, 42])



Synth(\pingpongeffect, [\in, 0])
a= {SoundIn.ar}.play(outbus:0)
a.free
```

multi-channel systems
--
example code you can add to your startup file to automatically configure your soundcard.
note that you will need to edit name and exact number of channels to match which soundcard model you are using.  below only three examples.
```
Server.local.options.device= "2882 [3712]";
Server.local.options.numInputBusChannels= 8;
Server.local.options.numOutputBusChannels= 18;

Server.local.options.device= "Scarlett 18i20 USB";
Server.local.options.numInputBusChannels= 14;
Server.local.options.numOutputBusChannels= 20;

Server.local.options.device= "Fireface 400 (30D)";
Server.local.options.numInputBusChannels= 18;
Server.local.options.numOutputBusChannels= 18;
```

try out PanAz.  change the `width` and the number of channels.
```
s.options.numOutputBusChannels= 18;
s.meter;
{PanAz.ar(18, PinkNoise.ar(0.1), MouseX.kr(-1, 1), width: 8)}.play;
```

other
--
```
PanAz.ar
VBap //in sc3 plugins
Ambisonics //look into Quarks AmbIEM
```
