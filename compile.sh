#!/bin/sh

g++ -o tp1 -D _ENTREGA_ src/main.cc
g++ -o tp1.debug src/main.cc
g++ -o tp1.nband -D _NBAND_ src/main.cc
g++ -o tp1.float -D _FLOAT_ src/main.cc
