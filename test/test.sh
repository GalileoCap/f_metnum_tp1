#!/bin/sh

g++ -o tp1 -D _PROFILING_ src/main.cc
./tp1 ./data/$1.in ./data/$1.out $2
cat ./data/$1.out
