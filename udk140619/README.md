140619
======

_delay lines_

delaying sound from the microphone
--

```supercollider
s.boot

a= {DelayN.ar(SoundIn.ar, 3, 3)}.play //mono delay

a= {DelayN.ar(SoundIn.ar, 3, 3)!2}.play //mono delay in both left and right (!2 is same as .dup(2))
```

note the maximum delay time versus the actual delaytime.  the maximum allocates memory and makes room for say 3 seconds of mono sound.  3 seconds means 3*44100= 132300 samples if you are running the server at samplerate 44.1kHz.  if you start to get out-of-memory errors in sc, you should check that you don't have any unreasonable numbers in the maxdelaytime (not more than 30sec or so).  if you still get the error you can increase the memory given to sc (very low by default).  put the following line in you startup file (see under File menu) and recompile.

`Server.local.options.memSize= 65536; //increase memory 8x`


```supercollider
( //stereo
a= {  [
	DelayN.ar(SoundIn.ar, 3, 1.5),
	DelayN.ar(SoundIn.ar, 3, 2.2)*0.25
	]
}.play;
)

a.free;

(
a= {  [
	DelayN.ar(SoundIn.ar, 3, 1.5)*SinOsc.ar(500), //delay + ring modulation on left channel
	DelayN.ar(SoundIn.ar, 3, 2.2)*SinOsc.ar(600) //delay + ring modulation on right channel
	]
}.play;
)

a.free;

//mixing many ringmodulated and delayed signals together in left and right channels
(
a= {  [
	(DelayN.ar(SoundIn.ar, 1.5, 1.5)*SinOsc.ar(500)) + (DelayN.ar(SoundIn.ar, 2, 2)*SinOsc.ar(600)) + (DelayN.ar(SoundIn.ar, 2.5, 2.5)*SinOsc.ar(700)),
	(DelayN.ar(SoundIn.ar, 1.2, 1.2)*SinOsc.ar(6000)) + (DelayN.ar(SoundIn.ar, 2.2, 2.2)*SinOsc.ar(7000)) + (DelayN.ar(SoundIn.ar, 2.3, 2.3)*SinOsc.ar(8000))
	]
}.play;
)

a.free;
```

changing delaytimes
--
DelayC is better to use when modulating (changing) the delaytime dynamically.

```supercollider
//doppler effect
a= {DelayC.ar(SoundIn.ar, 3, LFSaw.ar(0.1).range(3, 0))!2}.play //pitchup

a= {DelayC.ar(SoundIn.ar, 3, LFSaw.ar(0.1).range(0, 3))!2}.play //pitchdown

//another way to change pitch up vs down is to use negative freq for the modulator
a= {|freq= 0.1| DelayC.ar(SoundIn.ar, 3, LFSaw.ar(freq).range(0, 3))!2}.play
a.set(\freq, -0.1)
a.set(\freq, 0.1)
a.set(\freq, -0.05)
a.set(\freq, 0) //no change in delaytime (lfo stands still) and no shift in pitch



//also try with different lfos
{LFSaw.ar(500)}.plot

a= {|freq= 0.1| DelayC.ar(SoundIn.ar, 3, LFNoise0.ar(freq).range(0, 3))!2}.play

a= {|freq= 0.1| DelayC.ar(SoundIn.ar, 3, LFTri.ar(freq).range(0, 3))!2}.play

a= {|freq= 0.1| DelayC.ar(SoundIn.ar, 3, SinOsc.ar(freq).range(0, 3))!2}.play
```


echo effect
--
```supercollider
//careful with feedback below.  use headphones
a= {CombN.ar(SoundIn.ar, 3, 1, 5)}.play

a= {CombN.ar(SoundIn.ar, 3, 3, 35)}.play //very long decay - add sounds and the gradually disappear

a= {CombN.ar(SoundIn.ar, 3, 0.1, 0.9)}.play

a= {CombN.ar(SoundIn.ar, 1, 1/400, 0.1)}.play //karpus strong (400hz)
a= {CombN.ar(SoundIn.ar, 1, 1/300, 0.1)}.play //(300hz)

a= {CombN.ar(Impulse.ar(0.5), 1, 1/100, 0.2)}.play //karpus strong sort of

a= {CombN.ar(SoundIn.ar, 1, 1/[400, 500], 0.1)}.play

a= {CombC.ar(SoundIn.ar, 1, 1/[400+SinOsc.ar(0.1, 0, 10), 500+SinOsc.ar(0.12, 0, 20)], 0.1)}.play //chords
```

and also there is a C version on CombN that is better to use when the delaytime is changing dynamically (less artifacts because it will use cubic interpolation internally).

```supercollider
a= {CombC.ar(SoundIn.ar, 3, LFSaw.ar(0.05).range(0, 3), 3)!2}.play
```


more examples
--
```supercollider
{AllpassN.ar(SoundIn.ar, 0.1, 0.1, 0.3)}.play

{CombN.ar(SoundIn.ar, 0.1, 0.1, 0.3)}.play

{DelayC.ar(SinOsc.ar(400), 0.3, LFTri.ar(1).range(0, 0.3))}.play

{DelayC.ar(DelayN.ar(SoundIn.ar, 1, 1), 0.3, LFSaw.ar(MouseX.kr(-1, 1)).range(0, 0.3))}.play

{AllpassC.ar(DelayN.ar(SoundIn.ar, 1, 1), 0.3, LFSaw.ar(MouseX.kr(-1, 1)).range(0, 0.3))}.play

{CombC.ar(DelayN.ar(SoundIn.ar, 1, 1), 0.3, LFSaw.ar(MouseX.kr(-1, 1)).range(0, 0.3))}.play
```
