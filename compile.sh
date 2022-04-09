#!/bin/sh

g++ -o tp1 src/main.cc
g++ -o tp1.debug -D _PROFILING_ src/main.cc
