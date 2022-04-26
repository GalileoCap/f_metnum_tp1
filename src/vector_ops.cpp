#include "vector_ops.h"

template<typename T>
std::vector<T> operator*(std::vector<T> v, floating_t k) { //U: Scalar product
  for (T& x : v) x *= k;
  return v;
}

template<typename T>
std::vector<T> operator*(floating_t k, const std::vector<T>& v) { //U: Scalar product
  return v * k;
}

template<typename T>
T operator*(const std::vector<T>& v0, const std::vector<T>& v1) { //U: Dot product
  if (v0.size() != v1.size()) throw std::invalid_argument("vectors must be of same size");

  T res = 0;
  for (int i = 0; i < v0.size(); i++)
    res += v0[i] * v1[i];

  return res;
}

template<typename T>
std::vector<T> operator+(const std::vector<T>& v0, const std::vector<T>& v1) {
  if (v0.size() != v1.size()) throw std::invalid_argument("vectors must be of same size");
  std::vector<T> res (v0);
  for (int i = 0; i < v0.size(); i++) res[i] += v1[i];
  return res;
}

template<typename T>
std::vector<T> operator-(const std::vector<T>& v0, const std::vector<T>& v1) {
  if (v0.size() != v1.size()) throw std::invalid_argument("vectors must be of same size");
  std::vector<T> res (v0);
  for (int i = 0; i < v0.size(); i++) res[i] -= v1[i];
  return res;
}
