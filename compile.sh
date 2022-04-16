#!/bin/sh

g++ -O3 -o tp1 src/main.cc
g++ -O3 -o tp1.profiling -D _PROFILING_ src/main.cc
g++ -O3 -o tp1.nband -D _NBAND_ src/main.cc
g++ -O3 -o tp1.float -D _FLOAT_ src/main.cc
