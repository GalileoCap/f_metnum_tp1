#ifndef _SYSTEM_
#define _SYSTEM_

#include "matrix.h"
#include "utils.h"

struct System {
  System(char*, char);
    
  void calc_lu(); //U: Calculates the LU factorization

  void solve_all();
  void solve(uint); //U: Solves a specific time instance using the specified method
  void _solve_gauss(uint); 
  void _solve_lu(uint); 

  void find_iso(uint);

  void write_output(char *dataOut) const;

  char method; //U: 0 for Gauss 1 for LU
  floating_t ri, re, iso, //U: Internal/External radius, isotherm temperature
             dr, dt; //U: Delta radius, delta theta
  uint mp1, n, ninst; //U: m+1 radii, n angles, ninst time instances
  Matrix A, L;
  std::vector<std::vector<floating_t>> //TODO: They could be lists
    T, //U: Solution vector for each instance
    b, //U: Resulting vector //TODO: Can be calc'd when needed
    isotherm; //U: Radii for the isotherm for each instance

  std::vector<long> times; //U: Profiling times
};

#include "system.cpp"

#endif
