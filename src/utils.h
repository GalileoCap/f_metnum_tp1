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

#include "matrix.h"

void read_input();
void write_output();

extern char *dataIn, *dataOut, method; //U: Files, method 0 for Gauss 1 for LU
extern double ri, re, iso, //U: Internal/External radius, isotherm temperature
       dr, dt; //U: Delta radius, delta theta
extern uint mp1, n, ninst; //U: m+1 radii, n angles, ninst time instances
extern std::vector<std::vector<double>> //TODO: They could be lists
  T, //U: Solution vector for each instance
  b; //U: Resulting vector //TODO: Can be calc'd when needed
extern Matrix A, L;

extern std::vector<double> times; //U: Profiling times

#include "utils.hpp"

#endif
