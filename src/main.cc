#include "utils.h"
#include "system.h"

char *dataIn, *dataOut, method; //U: Files, method 0 for Gauss 1 for LU
floating_t ri, re, iso, //U: Internal/External radius, isotherm temperature
       dr, dt; //U: Delta radius, delta theta
uint mp1, n, ninst; //U: m+1 radii, n angles, ninst time instances
std::vector<std::vector<floating_t>> //TODO: They could be lists
  T, //U: Solution vector for each instance
  b; //U: Resulting vector //TODO: This can be calc'd when needed
Matrix A, L;
std::vector<std::vector<floating_t>> isotherm; //U: Radii for the isotherm for each instance
std::vector<ulong> times; //U: Profiling times

int main (int argc, char *argv[]) {
  //S: Processing arguments
  if (argc != 4) throw std::invalid_argument("Missing/Extra arguments");

  dataIn = argv[1]; dataOut = argv[2];
  method = argv[3][0];

  if (strlen(argv[3]) != 1 || (method != '0' && method != '1')) throw std::invalid_argument("Invalid method, must be 0 or 1");

  printf("TP1 Metodos Numericos\nF. Galileo Cappella Lewi\ndataIn: %s, dataOut: %s, metodo: %c\n", dataIn, dataOut, method);

  //S: Setting up
  read_input();
  construct_system();
  if (method == '1') calc_lu(); //A: If we're using LU factorization, we have to calculate it

  //S: Solve each time instance
  for (uint i = 0; i < ninst; i++) {
    solve(i);
    find_iso(i);
  }

  //S: Output
  write_output();

  return 0;
}
