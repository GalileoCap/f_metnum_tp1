#ifndef _UTILS_
#define _UTILS_

#include <math.h>
#include <vector>
#include <fstream>
#include <iostream>
#include <stdio.h>
#include <string.h>
#include <stdexcept>

typedef unsigned int uint;

template<typename T>
std::vector<T> operator*(std::vector<T>, double); //U: Scalar product

template<typename T>
std::vector<T> operator*(double, const std::vector<T>&); //U: Scalar product

template<typename T>
std::vector<T> operator*(const std::vector<T>&, const std::vector<T>&); //U: Dot product

template<typename T>
std::vector<T> operator+(const std::vector<T>&, const std::vector<T>&);

template<typename T>
std::vector<T> operator-(const std::vector<T>&, const std::vector<T>&);

void write_output(char* dataOut, const std::vector<std::vector<double>>& T);

#include "utils.hpp"

#endif
