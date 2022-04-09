#include "utils.h"

void read_input() {
  std::ifstream fin(dataIn);

  fin >> ri >> re >> mp1 >> n >> iso >> ninst; fin.ignore(); //A: Read parameters from file
  T = std::vector<std::vector<double>> (ninst, std::vector<double> (mp1 * n));
  for (uint i = 0; i < ninst; i++) {
    for (uint j = 0; j < n; j++) {
        fin >> T[i][j]; //A: Internal temperatures
    }
    for (uint j = ((mp1 - 1) * n); j < (mp1 * n); j++) fin >> T[i][j]; //A: External temperatures
    //TODO: Check if eof and throw error
  }

  fin.close();

  times = std::vector<double> ((method == '1') + ninst, 0);
}

void write_output() {
  std::ofstream fout(dataOut);

#ifndef _PROFILING_
  for (uint i = 0; i < T.size(); i++) {
    for (const double& t : T[i]) fout << t << ' '; fout << '\n'; 
  }
#else
  if (method == '1') fout << times[0] << '\n'; //A: LU
  for (uint i = 0; i < T.size(); i++) {
    for (const double& t : T[i]) fout << t << ' '; 
    fout << times[i + (method == '1')] << ' '; //NOTE: Skip over LU
    fout << '\n'; 
  }
#endif

  fout.close();
}
