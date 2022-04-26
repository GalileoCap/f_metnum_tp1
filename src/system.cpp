#include "system.h"

System::System(char *dataIn, char _method) : method(_method) {
  std::ifstream fin(dataIn);

  fin >> ri >> re >> mp1 >> n >> iso >> ninst; fin.ignore(); //A: Read parameters from file
  T = std::vector<std::vector<floating_t>> (ninst, std::vector<floating_t> (mp1 * n));
  for (uint i = 0; i < ninst; i++) {
    for (uint j = 0; j < n; j++) fin >> T[i][j]; //A: Internal temperatures
    for (uint j = ((mp1 - 1) * n); j < (mp1 * n); j++) fin >> T[i][j]; //A: External temperatures
    //TODO: Check if eof and throw error
  }

  fin.close();

  isotherm = std::vector<std::vector<floating_t>> (ninst, std::vector<floating_t> (n));
  times = std::vector<long> ((method == '1') + ninst, 0);

  A = Matrix(mp1 * n);

  dr = (re - ri) / mp1; dt = 2 * M_PI / n;
  auto calc_coefficient = [_ri=ri, _dr=dr, _dt=dt](uint c, floating_t i) {
    floating_t r = (_ri + (_dr * i)); //A: Radius

    if (c == 0) return (1 / pow(_dr, 2)) + (-1 / (r * _dr)); //A: Alpha
    else if (c == 1) return (-2 / pow(_dr, 2)) + (1 / (r * _dr)) + (-2 / pow(r * _dt, 2)); //A: Beta
    else if (c == 2) return 1 / pow(_dr, 2); //A: Gamma
    else if (c == 3) return 1 / pow(r * _dt, 2); //A: Chi
    else throw std::invalid_argument("c is out of range");
  };

  //S: Build the matrix
  for (uint i = 1; i < (mp1 - 1); i++) { //A: For each unknown radius (skips over first and last radii)
    floating_t alpha = calc_coefficient(0, i),
           beta = calc_coefficient(1, i),
           gamma = calc_coefficient(2, i),
           chi = calc_coefficient(3, i);

    for (uint j = 0; j < n; j++) { //A: For each angle in this radius
      uint row = i * n + j;

      //A: This angle/radius
      A(row, row) = beta; 

      //A: Previous angle, same radius
      if (j > 0) A(row, row - 1) = chi; //A: Not the first angle
      else A(row, row + n - 1) = chi;

      //A: Next angle, same radius
      if ((j + 1) < n) A(row, row + 1) = chi; //A: Not the last angle
      else A(row, row - n + 1) = chi; 

      A(row, row + n) = gamma; //A: Same angle, previous radius
      A(row, row - n) = alpha; //A: Same angle, next radius
    }
  }

  b = std::vector<std::vector<floating_t>> (ninst, std::vector<floating_t> (mp1 * n, 0));
  for (uint i = 0; i < ninst; i++) {
    for (uint j = 0; j < n; j++) b[i][j] = T[i][j]; //A: Internal temperatures
    for (uint j = ((mp1 - 1) * n); j < (mp1 * n); j++) b[i][j] = T[i][j]; //A: External temperatures
  }
}

void System::calc_lu() { //U: Calculates the LU decomposition
  long start = get_time();

  L = Matrix(A._m.size());

  for (uint i = 0; i < A._m.size(); i++) { //A: For each row of A
    for (uint l = i + 1; l < A._m.size(); l++) { //A: Zeros under the diagonal for this col and save coefficient in L
      floating_t c = A(l, i) / A(i, i); 

      A.get_row(l) = A.get_row(l) - c * A.get_row(i);
      L(l, i) = c; 
    }
  }

  times[0] = get_time() - start;
}

void System::solve_all() {
  for (uint i = 0; i < ninst; i++) {
    solve(i);
    find_iso(i);
  }
}

void System::solve(uint inst) { //U: Solves a specific time instance, may write the output
  long start = get_time();

  if (method == '0') _solve_gauss(inst);
  else _solve_lu(inst);

  times[(method == '1') + inst] = get_time() - start;
}

void System::_solve_gauss(uint inst) {
  Matrix _A = A; //A: Copy
  std::vector<floating_t> _b = b[inst];

  for (uint i = 0; i < _A._m.size(); i++) { //A: For each row
    for (uint l = i + 1; l < _A._m.size(); l++) { //A: Zeros under the diagonal for this col 
      floating_t c = _A(l, i) / _A(i, i); 

      _A.get_row(l) = _A.get_row(l) - c * _A.get_row(i);
      _b[l] = _b[l] - c * _b[i]; //A: Apply same operation to the result
    }
  }

  std::vector<floating_t> &t = T[inst]; //A: Rename
  uint i = (_b.size() - 1);
  while (true) {
    uint l_limit = ((i+n+1) > _b.size()) ? _b.size() : (i+n+1); //A: Min(i+n, _b.size())
    floating_t foo = 0; for (uint l = (i+1); l < l_limit; l++) foo += _A(i, l) * t[l]; //A: foo = sum from l = i+1 to n of (a[i][l] * t[l])
    t[i] = (_b[i] - foo) / _A(i, i);

    if (i-- == 0) break; //A: If I reached the end, break, else keep going with the next i
  }
}

void System::_solve_lu(uint inst) {
  const std::vector<floating_t>& _b = b[inst]; //A: Rename

  //S: First solve Ly = b
  std::vector<floating_t> y (_b.size()); 
  for (uint i = 0; i < y.size(); i++) { //A: Solve for each y
    uint l_base = (i < n) ? 0 : (i-n); //A: Max(i-n, 0)
    //uint l_base = 0;
    floating_t foo = 0; for (uint l = l_base; l < i; l++) foo += L(i, l) * y[l]; //A: foo = sum from l = i+1 to n of (a[i][l] * x[l])
    y[i] = (_b[i] - foo) / L(i, i);
  }

  //S: Solve Ut = y 
  std::vector<floating_t> &t = T[inst]; //A: Rename
  uint i = (y.size() - 1);
  while (true) {
    uint l_limit = ((i+n+1) > y.size()) ? y.size() : (i+n+1); //A: Min(i+n+1, y.size())
    floating_t foo = 0; for (uint l = (i+1); l < l_limit; l++) foo += A(i, l) * t[l]; //A: foo = sum from l = i+1 to n of (u[i][l] * t[l])
    t[i] = (y[i] - foo) / A(i, i);

    if (i-- == 0) break; //A: If I reached the end, break, else keep going with the next i
  }
}

void System::find_iso(uint inst) { //U: Finds the isotherm by doing a linear interpolation between the two points around where it should be
  const std::vector<floating_t> &t = T[inst]; //A: Rename
  for (uint i = 0; i < n; i++) { //A: For each angle
    isotherm[inst][i] = re + 1; //A: Default NOTE: Values outside of the furnace are invalid and thus should be ignored 
    uint j = 0; while(j < (mp1 - 1) && t[j * n + i] > iso && t[(j+1) * n + i] > iso) j++; //A: Find the two points around where the isotherm is
    floating_t m = (t[(j + 1) * n + i] - t[j * n + i]) / dr; //U: Slope of the line
    floating_t r = ri + j * dr;
    isotherm[inst][i] = r + (iso - t[(j * n + i)]) / m;
  }
  //TODO: The temperature can come back up
}

//TODO: Optimize by taking advantage of "band" matrix and first and last n rows being 1's
void System::write_output(char *dataOut) const {
  std::ofstream fout(dataOut);

  fout.precision(6);

#ifdef _PROFILING_
  for (const long& time : times) fout << time << ' '; fout << '\n';
  for (const std::vector<floating_t>& inst : isotherm) { 
    for (const floating_t& r : inst) fout << r << ' '; fout << '\n';
  }
#endif
  for (const std::vector<floating_t> inst : T) 
    for (const floating_t& t : inst)
      fout << std::fixed << t << ' ' << '\n';

  fout.close();
}
