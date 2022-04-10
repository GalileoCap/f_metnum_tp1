#include "system.h"

void construct_system() { //U: Sets up the system to be solved
  A = Matrix(mp1 * n);

  dr = (re - ri) / mp1; dt = 2 * M_PI / n;
  auto calc_coefficient = [](uint c, double i) {
    double r = (ri + (dr * i)); //A: Radius

    if (c == 0) return (1 / pow(dr, 2)) + (-1 / (r * dr)); //A: Alpha
    else if (c == 1) return (-2 / pow(dr, 2)) + (1 / (r * dr)) + (-2 / pow(r * dt, 2)); //A: Beta
    else if (c == 2) return 1 / pow(dr, 2); //A: Gamma
    else if (c == 3) return 1 / pow(r * dt, 2); //A: Chi
    else throw std::invalid_argument("c is out of range");
  };

  //S: Build the matrix
  for (uint i = 1; i < (mp1 - 1); i++) { //A: For each unknown radius (skips over first and last radii)
    double alpha = calc_coefficient(0, i),
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

  b = std::vector<std::vector<double>> (ninst, std::vector<double> (mp1 * n, 0));
  for (uint i = 0; i < ninst; i++) {
    for (uint j = 0; j < n; j++) b[i][j] = T[i][j]; //A: Internal temperatures
    for (uint j = ((mp1 - 1) * n); j < (mp1 * n); j++) b[i][j] = T[i][j]; //A: External temperatures
  }
}

void calc_lu() { //U: Calculates the LU decomposition
  long start = get_time();

  L = Matrix(A._m.size());

  for (uint i = 0; i < A._m.size(); i++) { //A: For each row of A
    for (uint l = i + 1; l < A._m.size(); l++) { //A: Zeros under the diagonal for this col and save coefficient in L
      double c = A(l, i) / A(i, i); 

      A.get_row(l) = A.get_row(l) - c * A.get_row(i);
      L(l, i) = c; 
    }
  }

  times[0] = get_time() - start;
}

void solve(uint inst) { //U: Solves a specific time instance, may write the output
  long start = get_time();

  if (method == '0') _solve_gauss(inst);
  else _solve_lu(inst);

  times[(method == '1') + inst] = get_time() - start;
}

void _solve_gauss(uint inst) {
  Matrix _A = A; //A: Copy
  std::vector<double> _b = b[inst];

  for (uint i = 0; i < _A._m.size(); i++) { //A: For each row
    for (uint l = i + 1; l < _A._m.size(); l++) { //A: Zeros under the diagonal for this col 
      double c = _A(l, i) / _A(i, i); 

      _A.get_row(l) = _A.get_row(l) - c * _A.get_row(i);
      _b[l] = _b[l] - c * _b[i]; //A: Apply same operation to the result
    }
  }

  std::vector<double> &t = T[inst]; //A: Rename
  for (int i = (_b.size() - 1); i >= 0; i--) { //A: Solve for each t
    double foo = 0; for (int l = (i + 1); l < _b.size(); l++) foo += _A(i, l) * t[l]; //A: foo = sum from l = i+1 to n of (a[i][l] * t[l])
    t[i] = (_b[i] - foo) / _A(i, i);
  }
}

void _solve_lu(uint inst) {
  const std::vector<double>& _b = b[inst]; //A: Rename

  //S: First solve Ly = b
  std::vector<double> y (_b.size()); 
  for (int i = 0; i < y.size(); i++) { //A: Solve for each y
    double foo = 0; for (int l = 0; l < i; l++) foo += L(i, l) * y[l]; //A: foo = sum from l = i+1 to n of (a[i][l] * x[l])
    y[i] = (_b[i] - foo) / L(i, i);
  }

  //S: Solve Ut = y 
  std::vector<double> &t = T[inst]; //A: Rename
  for (int i = (y.size() - 1); i >= 0; i--) { //A: Solve for each t
    double foo = 0; for (int l = (i + 1); l < y.size(); l++) foo += A(i, l) * t[l]; //A: foo = sum from l = i+1 to n of (u[i][l] * t[l])
    t[i] = (y[i] - foo) / A(i, i);
  }
}

void find_iso(uint inst) { //U: Finds the isotherm by doing a linear interpolation between the two points around where the isotherm should be
  const std::vector<double> &t = T[inst]; //A: Rename
  for (uint i = 0; i < n; i++) { //A: For each angle
    uint j = 0; for(; j < (mp1 - 1); j++) if (t[(j + 1) * n + i] < iso) break; //A: Find the two points around where the isotherm is
    double m = (t[(j + 1) * n + i] - t[j * n + i]) / dr; //U: Slope of the line
    uint r = ri + j * dr;
    isotherm[inst][i] = r + (iso - t[(j * n + i)]) / m;
  }
  //TODO: Different behaviour when the isotherm doesn't exists
  //TODO: The temperature can come back up
}

//TODO: Optimize by taking advantage of "band" matrix and first and last n rows being 1's
