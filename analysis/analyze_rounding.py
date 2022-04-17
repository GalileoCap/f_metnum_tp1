import numpy as np
import pandas as pd
from scipy import stats

from utils import *
import plot
import system

def analyze_rounding(fpath, replace = False):
	print(f'analyze_rounding fpath {fpath} replace {replace}')

	data = parse_input(in_fpath(fpath))
	M = system.matrix(data)
	b = system.result(data)

	f_fpath = f'{fpath}.float'
	d_fpath = f'{fpath}.double'
	if replace:
		print(f'analyze_rounding fpath {fpath} run double')
		run(in_fpath(fpath), out_fpath(d_fpath), 0, False)
		print(f'analyze_rounding fpath {fpath} run float')
		run(in_fpath(fpath), out_fpath(f_fpath), 0, False, '.float')
	
	_, _, d_output = parse_output(out_fpath(d_fpath), data)
	_, _, f_output = parse_output(out_fpath(f_fpath), data)

	[_, _, mp1, n, _, ninst], _ = data
	diffs = [np.abs(d_output[inst] - f_output[inst]) for inst in range(ninst)]
	cond_n = np.linalg.cond(M)
	for inst in range(ninst):
		print(f'analyze_rounding within range? {system.error_range(M, b[inst], d_output[inst], f_output[inst], data)}')

		d_iso = system.calc_isotherm(d_output[inst], data)
		f_iso = system.calc_isotherm(f_output[inst], data)
		plot.isotherms({'Double': d_iso, 'Float': f_iso}, data, fpath)
		
		plot.temperature(diffs[inst], data, fpath)
	
	print('analyze_rounding DONE')
	#TODO: Better reporting

if __name__ == '__main__':
	fpath = f'../data/rounding/test'
	analyze_rounding(fpath, replace = True) #TODO: True
