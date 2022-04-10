#include "utils.h"

long get_time() { //U: Returns the current time in milliseconds
  auto start = std::chrono::system_clock::now();
  return std::chrono::duration_cast<std::chrono::nanoseconds>(start.time_since_epoch()).count();
}

void read_input() {
  std::ifstream fin(dataIn);

  fin >> ri >> re >> mp1 >> n >> iso >> ninst; fin.ignore(); //A: Read parameters from file
  T = std::vector<std::vector<double>> (ninst, std::vector<double> (mp1 * n));
  for (uint i = 0; i < ninst; i++) {
    for (uint j = 0; j < n; j++) fin >> T[i][j]; //A: Internal temperatures
    for (uint j = ((mp1 - 1) * n); j < (mp1 * n); j++) fin >> T[i][j]; //A: External temperatures
    //TODO: Check if eof and throw error
  }

  fin.close();

  isotherm = std::vector<std::vector<double>> (ninst, std::vector<double> (n));
  times = std::vector<ulong> ((method == '1') + ninst, 0);
}

void write_output() {
  std::ofstream fout(dataOut);

#ifdef _PROFILING_
  for (const long& time : times) fout << time << ' '; fout << '\n';
#elif defined(_ISOTHERM_)
  for (const std::vector<double>& inst : isotherm) {
    for (const double& r : inst) fout << r << ' '; fout << '\n';
  }
#else
  for (uint i = 0; i < T.size(); i++) {
    for (const double& t : T[i]) fout << t << ' '; fout << '\n'; 
  }
#endif

  fout.close();
}
