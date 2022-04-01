#include "system.h"
#include "utils.h"

int main (int argc, char *argv[]) {
  //S: Processing arguments
  if (argc != 4) throw std::invalid_argument("Missing/Extra arguments");

  char *dataIn = argv[1],
       *dataOut = argv[2],
       *methodS = argv[3],
        method = methodS[0];

  if (strlen(methodS) != 1 || (method != '0' && method != '1')) throw std::invalid_argument("Invalid method, must be 0 or 1");

  printf("TP1 Metodos Numericos\nF. Galileo Cappella Lewi\ndataIn: %s, dataOut: %s, metodo: %c\n", dataIn, dataOut, method);

  //S: Setting up
  System sys = read_file(dataIn, method);

  //TODO: Measue time 
  if (method == '1') sys.calc_lu(); //A: If we're using LU factorization, we have to calculate it
  
  std::vector<std::vector<double>> T;
  for (uint i = 0; i < sys._ninst; i++) {
    //TODO: Measure time
    std::vector<double> t = sys.solve(i);

    T.push_back(t);
  }

  write_output(dataOut, T);

  return 0;
}
