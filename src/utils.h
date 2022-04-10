#ifndef _UTILS_
#define _UTILS_

#include <math.h>
#include <vector>
#include <fstream>
#include <iostream>
#include <stdio.h>
#include <string.h>
#include <chrono>
#include <stdexcept>

typedef unsigned int uint;
typedef double floating_t;

#include "matrix.h"

long get_time(); //U: Returns the current time in milliseconds

void read_input();
void write_output();

extern char *dataIn, *dataOut, method; //U: Files, method 0 for Gauss 1 for LU
extern floating_t ri, re, iso, //U: Internal/External radius, isotherm temperature
       dr, dt; //U: Delta radius, delta theta
extern uint mp1, n, ninst; //U: m+1 radii, n angles, ninst time instances
extern Matrix A, L;
extern std::vector<std::vector<floating_t>> //TODO: They could be lists
  T, //U: Solution vector for each instance
  b; //U: Resulting vector //TODO: Can be calc'd when needed
extern std::vector<std::vector<floating_t>> isotherm; //U: Radii for the isotherm for each instance

extern std::vector<ulong> times; //U: Profiling times

#include "utils.hpp"

#endif
