#INFO: Compara los resultados esperados con los obtenidos por nuestro programa

import numpy as np
import pandas as pd
from scipy import stats

from utils import *
import system
import plot

def analyze_expected(fpath, replace = False):
	print(f'analyze_expected fpath {fpath} replace {replace}')

	if replace:
		run(in_fpath(fpath), out_fpath(fpath), 0)

	data = parse_input(in_fpath(fpath))
	M = system.matrix(data)
	b = system.result(data)

	_, _, output = parse_output(out_fpath(fpath), data)
	_, _, expected = parse_output(expected_fpath(fpath), data)
	python = system.solve(M, b)

	if not system.compare_results(output, python):
		print('analyze_expected ERROR', i)

	[_, _, mp1, n, _, ninst], _ = data
	diffs = [np.abs((expected[inst] - python[inst]) / expected[inst]) for inst in range(ninst)]
	cond_n = np.linalg.cond(M)
	for inst in range(ninst):
		print(f'analyze_expected instance {inst} within range? {system.error_range(M, b[inst], python[inst], expected[inst], data)}')

		_fpath = f'{fpath}.{i}.{inst}'
		a_iso = system.calc_isotherm(python[inst], data)
		e_iso = system.calc_isotherm(expected[inst], data)
		plot.isotherms({'Expected': e_iso, 'Approximate': a_iso}, data, _fpath)
		
		plot.temperature(diffs[inst], data, _fpath, 'Diferencia (%)')
	
	print(f'analyze_expected fpath {fpath} replace {replace} DONE')
	#TODO: Reporte cuantificando errores

if __name__ == '__main__':
	for i in range(1, 4 + 1):
		analyze_expected(f'../data/tests_alu/test{i}', True)
