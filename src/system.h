#ifndef _SYSTEM_
#define _SYSTEM_

#include "matrix.h"
#include "utils.h"

void construct_system();
  
void calc_lu(); //U: Calculates the LU factorization

void solve(uint); //U: Solves a specific time instance using the specified method
void _solve_gauss(uint); 
void _solve_lu(uint); 

void find_iso(double);

#include "system.hpp"

#endif
