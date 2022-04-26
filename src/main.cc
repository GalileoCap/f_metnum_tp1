#include "utils.h"
#include "system.h"

int main (int argc, char *argv[]) {
  //S: Processing arguments
  if (argc != 4) throw std::invalid_argument("Missing/Extra arguments");

  char *dataIn = argv[1],
       *dataOut = argv[2],
        method = argv[3][0];

  if (strlen(argv[3]) != 1 || (method != '0' && method != '1')) throw std::invalid_argument("Invalid method, must be 0 or 1");

  printf("TP1 Metodos Numericos\nF. Galileo Cappella Lewi\ndataIn: %s, dataOut: %s, metodo: %c\n", dataIn, dataOut, method);

  //S: Setting up
  System system(dataIn, method);
  if (method == '1') system.calc_lu(); //A: If we're using LU factorization, we have to calculate it
  system.solve_all();

  //S: Output
  system.write_output(dataOut);

  return 0;
}
