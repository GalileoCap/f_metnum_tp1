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
#ifdef _FLOAT_
typedef float floating_t;
#else
typedef long double floating_t;
#endif

#include "matrix.h"

long get_time(); //U: Returns the current time in milliseconds

#include "utils.cpp"

#endif
