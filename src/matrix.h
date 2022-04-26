#ifndef _MATRIX_
#define _MATRIX_

#include "utils.h"
#include "vector_ops.h"

struct Matrix {
  Matrix(uint n = 0);
  Matrix(const std::vector<std::vector<floating_t>>& m); 
  Matrix(const Matrix&);
  Matrix& operator=(const Matrix&);
  
  floating_t& operator()(uint row, uint col); //U: Returns an element by row and column
  const floating_t& operator()(uint row, uint col) const;

  std::vector<floating_t>& get_row(uint row); 

  std::vector<std::vector<floating_t>> _m;
};

#include "matrix.cpp"

#endif
