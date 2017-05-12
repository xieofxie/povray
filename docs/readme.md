# Guide

## Setup

1. Compile povray like [unix](../unix/README) or [windows](../windows/readme.txt)

2. Download living_room_code from [VaFRIC](http://www.doc.ic.ac.uk/~ahanda/VaFRIC/living_room.html), put it into docs. use [living_room_camera.inc](living_room_code/living_room_camera.inc) in git

3. pip install pyquaternion [pyquaternion](http://kieranwynn.github.io/pyquaternion/)

## Usage

Try [commands.txt](example/commands.txt)

## Math

Pos means x,y,z. Quat means w,x,y,z. Coordinate system is right handed.
While povray is left handed, so flip x when providing path positions

## Camera format

See [example](example/camera.xml). Camera is rotated by quat first, then translated by pos.
Relative to a virtual center 0,0,0 looking towards 0,0,1
