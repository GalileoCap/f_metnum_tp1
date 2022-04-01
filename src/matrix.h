#ifndef _MATRIX_
#define _MATRIX_

#include "utils.h"

struct Matrix {
  Matrix(uint n = 0);
  Matrix(const std::vector<std::vector<double>>& m); 
  Matrix(const Matrix&);
  Matrix& operator=(const Matrix&);
  
  double& operator()(uint row, uint col); //U: Returns an element by row and column
  const double& operator()(uint row, uint col) const;

  std::vector<double>& get_row(uint row); 

  std::vector<std::vector<double>> _m;

  //TODO: Custom struct for rows/cols
  //TODO: Iterator
};

Matrix apply_gauss(Matrix&);

#include "matrix.hpp"

#endif
