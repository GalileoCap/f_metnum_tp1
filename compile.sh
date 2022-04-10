#!/bin/sh

g++ -o tp1 src/main.cc
g++ -o tp1.isotherm -D _ISOTHERM_ src/main.cc
g++ -o tp1.profiling -D _PROFILING_ src/main.cc
