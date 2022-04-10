#include "matrix.h"

Matrix::Matrix(uint n) : _m(n, std::vector<floating_t> (n, 0)) { //U: Defaults to identity 
  for (uint i = 0; i < n; i++) _m[i][i] = 1;
}

Matrix::Matrix(const std::vector<std::vector<floating_t>>& m) :
  _m(m) {}

Matrix::Matrix(const Matrix& M) : _m(M._m) {};

Matrix& Matrix::operator=(const Matrix& M) {
  _m = M._m;

  return *this;
}

floating_t& Matrix::operator()(uint row, uint col) { //U: Returns a value
  return _m[row][col];
}
  
const floating_t& Matrix::operator()(uint row, uint col) const { //A: Returns a value
  return _m[row][col];
}

std::vector<floating_t>& Matrix::get_row(uint row) {
  return _m[row];
}


