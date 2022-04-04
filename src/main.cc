#include "system.h"
#include "utils.h"
#include <chrono>

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

  auto start = std::chrono::steady_clock::now();
  std::vector<std::chrono::duration<double>> times;
  if (method == '1') {
    start = std::chrono::steady_clock::now();
    sys.calc_lu(); //A: If we're using LU factorization, we have to calculate it
    times.push_back(std::chrono::steady_clock::now() - start);
  }
  
  std::vector<std::vector<double>> T;
  for (uint i = 0; i < sys._ninst; i++) {
    start = std::chrono::steady_clock::now();
    std::vector<double> t = sys.solve(i);
    times.push_back(std::chrono::steady_clock::now() - start);

    T.push_back(t);
  }

  write_output(dataOut, T, times);

  return 0;
}
