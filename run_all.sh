#!/bin/sh

./compile.sh
./tp1 $1.in $1.out $2
./tp1.isotherm $1.in $1.isotherm.out $2
./tp1.profiling $1.in $1.profiling.out $2
