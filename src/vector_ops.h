#ifndef _VECTOR_OPS_
#define _VECTOR_OPS_

#include "utils.h"

template<typename T>
std::vector<T> operator*(std::vector<T>, floating_t); //U: Scalar product

template<typename T>
std::vector<T> operator*(floating_t, const std::vector<T>&); //U: Scalar product

template<typename T>
std::vector<T> operator*(const std::vector<T>&, const std::vector<T>&); //U: Dot product

template<typename T>
std::vector<T> operator+(const std::vector<T>&, const std::vector<T>&);

template<typename T>
std::vector<T> operator-(const std::vector<T>&, const std::vector<T>&);

#include "vector_ops.hpp"

#endif
