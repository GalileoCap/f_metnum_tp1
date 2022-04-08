#include "system.h"

System::System(
  double ri, double re, uint mp1, uint n, uint size, double iso, uint ninst, char method,
  const std::vector<std::vector<double>>& Ti,
  const std::vector<std::vector<double>>& Te
) : _method(method), _ninst(ninst), _Ti(Ti), _Te(Te), _b(ninst, std::vector<double> (size, 0)), _A(size), _L(size) { //U: Sets up the system to be solved

  double dr = (re - ri) / (mp1 - 1),
         dt = 2 * M_PI / n;

  auto calc_coefficient = [ri, dr, dt](uint c, double i) {
    double r = (ri + (dr * (i + 1))); //A: Radius

    if (c == 0) return (1 / pow(dr, 2)) + (-1 / (r * dr)); //A: Alpha
    else if (c == 1) return (-2 / pow(dr, 2)) + (1 / (r * dr)) + (-2 / pow(r * dt, 2)); //A: Beta
    else if (c == 2) return 1 / pow(dr, 2); //A: Gamma
    else if (c == 3) return 1 / pow(r * dt, 2); //A: Chi
    else throw std::invalid_argument("c is out of range");
  };

  //S: Build the matrix
  //_b = std::vector<std::vector<double>> (ninst , std::vector<double> (size, 0));
  for (uint i = 0; i < (mp1 - 2); i++) { //A: For each unknown radius
    double alpha = calc_coefficient(0, i),
           beta = calc_coefficient(1, i),
           gamma = calc_coefficient(2, i),
           chi = calc_coefficient(3, i);

    for (uint j = 0; j < n; j++) { //A: For each angle in this radius
      uint row = i * n + j;

      //A: This radius, and angle
      _A(row, row) = beta; 

      //A: Previous angle, same radius
      if (j > 0) _A(row, row - 1) = chi; //A: Not the first angle
      else _A(row, row + n - 1) = chi;

      //A: Next angle, same radius
      if ((j + 1) < n) _A(row, row + 1) = chi; //A: Not the last angle
      else _A(row, row - n + 1) = chi; 

      if ((i + 1) < (mp1 - 2)) _A(row, row + n) = gamma; //A: Same angle, previous radius; For every radius except the last one

      if (i > 0) _A(row, row - n) = alpha; //A: Same angle, next radius; For every radius except the first one
    }
  }

  //S: Build the resulting vector //TODO: This can be optimized and calc'd when needed
  for (uint i = 0; i < ninst; i++) 
    for (uint j = 0; j < n; j++) {
      _b[i][j] -= calc_coefficient(0, 0) * _Ti[i][j]; //A: The first radius is = -alpha * Ti
      _b[i][size - 1 - j] -= calc_coefficient(2, mp1 - 2) * _Te[i][n - 1 - j]; //A: The last radius is = -gamma * Te
      //A: The rest are = 0
    }
}

void System::calc_lu() { //U: Calculates the LU decomposition
  _L = Matrix(_A._m.size());

  for (uint i = 0; i < _A._m.size(); i++) { //A: For each row of _A
    for (uint l = i + 1; l < _A._m.size(); l++) { //A: Zeros under the diagonal for this col and save coefficient in _L
      double c = _A(l, i) / _A(i, i); 

      _A.get_row(l) = _A.get_row(l) - c * _A.get_row(i);
      _L(l, i) = c; 
    }
  }
}

std::vector<double> System::solve(uint inst) const { //U: Solves a specific time instance, may write the output
  if (_method == '0') return _solve_gauss(inst);
  else return _solve_lu(inst);
}

std::vector<double> System::_solve_gauss(uint inst) const {
  Matrix A = _A; //A: Copy
  std::vector<double> b = _b[inst];

  for (uint i = 0; i < A._m.size(); i++) { //A: For each row of A
    for (uint l = i + 1; l < A._m.size(); l++) { //A: Zeros under the diagonal for this col 
      double c = A(l, i) / A(i, i); 

      A.get_row(l) = A.get_row(l) - c * A.get_row(i);
      b[l] = b[l] - c * b[i]; //A: Apply same operation to the result
    }
  }

  std::vector<double> t (b.size());
  for (int i = (b.size() - 1); i >= 0; i--) { //A: Solve for each t
    double foo = 0; for (int l = (i + 1); l < b.size(); l++) foo += A(i, l) * t[l]; //A: foo = sum from l = i+1 to n of (a[i][l] * t[l])
    t[i] = (b[i] - foo) / A(i, i);
  }

  return t;
}

std::vector<double> System::_solve_lu(uint inst) const {
  const std::vector<double>& b = _b[inst];
  std::vector<double> y (b.size()); //A: First solve Ly = b
  for (int i = 0; i < y.size(); i++) { //A: Solve for each y
    double foo = 0; for (int l = 0; l < i; l++) foo += _L(i, l) * y[l]; //A: foo = sum from l = i+1 to n of (a[i][l] * x[l])
    y[i] = (b[i] - foo) / _L(i, i);
  }

  std::vector<double> t (y.size()); //A: Solve Ut = y
  for (int i = (y.size() - 1); i >= 0; i--) { //A: Solve for each t
    double foo = 0; for (int l = (i + 1); l < y.size(); l++) foo += _A(i, l) * t[l]; //A: foo = sum from l = i+1 to n of (a[i][l] * t[l])
    t[i] = (y[i] - foo) / _A(i, i);
  }

  return t;
}

System read_file(char* dataIn, char method) {
  std::ifstream fin(dataIn);

  uint mp1, n, ninst;
  double ri, re, iso;
  fin >> ri >> re >> mp1 >> n >> iso >> ninst; fin.ignore(); //A: Read parameters from file

  std::vector<std::vector<double>> Ti(ninst, std::vector<double> (n));
  std::vector<std::vector<double>> Te(ninst, std::vector<double> (n));
  for (uint i = 0; i < ninst; i++) {
    for (double& t : Ti[i]) fin >> t; fin.ignore(); //A: Internal temperature
    for (double& t : Te[i]) fin >> t; //A: External temperature
  }
  fin.close();

  uint size = (mp1 - 2) * n; 

  return System(ri, re, mp1, n, size, iso, ninst, method, Ti, Te);
}

//void find_iso(const System& s, double iso, uint inst) {
  //uint i = 0;
  //do {
    
    //double prevTemp =
  //} while (++i < (s._Ti[inst].size() + 2))
//}
