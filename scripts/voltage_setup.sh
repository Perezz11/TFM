#!/bin/bash
vh=5.0
vl=1.
hh=3.0
hl=-0.5

#set clock voltages
lta set v1ah $vh
lta set v1al $vl
lta set v1bh $vh
lta set v1bl $vl
lta set v2ch $vh
lta set v2cl $vl
lta set v3ah $vh
lta set v3al $vl
lta set v3bh $vh
lta set v3bl $vl
lta set h1ah $hh
lta set h1al $hl
lta set h1bh $hh
lta set h1bl $hl
lta set h2ch $hh
lta set h2cl $hl
lta set h3ah $hh
lta set h3al $hl
lta set h3bh $hh
lta set h3bl $hl

lta set swah -3.
lta set swal -9.
lta set swbh -3.
lta set swbl -3.

lta set rgah 5.0
lta set rgal 3.0
lta set rgbh 5.0
lta set rgbl 5.0

lta set ogah -4.
lta set ogal -8.
lta set ogbh -4.
lta set ogbl -4.

lta set dgah -4.
lta set dgal -11.
lta set dgbh -4.
lta set dgbl -4

lta set tgah 4.5
lta set tgal 0.5
lta set tgbh 4.5
lta set tgbl 4.5

#set bias voltages
lta set vdrain -22
lta set vdd -14 
lta set vr -10.5
lta set vsub $VSUB

#enable bias switches
lta set vdrain_sw 1
lta set vdd_sw 1
lta set vsub_sw 1
lta set vr_sw 1
lta set p15v_sw 1
lta set m15v_sw 1

