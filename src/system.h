#ifndef _SYSTEM_
#define _SYSTEM_

#include "matrix.h"
#include "utils.h"

struct System {
  System(
    double ri, double re, uint mp1, uint n, uint size, double iso, uint ninst, char method,
    const std::vector<std::vector<double>>& Ti,
    const std::vector<std::vector<double>>& Te
  );
  
  void calc_lu(); //U: Calculates the LU factorization
  std::vector<double> solve(uint) const; //U: Solves a specific time instance using the specified method

  char _method; uint _ninst;
  std::vector<std::vector<double>> _Ti, _Te, //U: Internal/External temperatures per time instance //TODO: Can we use lists instead of vectors?
                                   _b; //U: Result vector //TODO: Can be removed and calc'd on the moment
  Matrix _A, _L; //U: A = LU factorization //NOTE: To save space I'll save U in _A

  std::vector<double> _solve_gauss(uint) const; 
  std::vector<double> _solve_lu(uint) const; 

  double _calc_coefficient(uint, double) const;
};

System read_file(char* dataIn, char method);

#include "system.hpp"

#endif
