import numpy as np
import pandas as pd
from scipy import stats

from utils import *
import plot
import system

def create_example(ti, mp1, fpath):
	with open(in_fpath(fpath), 'w') as fout:
		fout.write(f'1 3 {mp1} 3 500 1\n')
		fout.write(f'{ti} {ti} {ti} 150 150 150\n')

def isotherm_by_inner(ti_range, fpath):
	print(f'isotherm_by_inner ti_range {ti_range} fpath {fpath}')

	distances = []
	for ti in ti_range:
		create_example(ti, 100, fpath)
		run(in_fpath(fpath), out_fpath(fpath), 0, True)
		_, [[position, _, _]], _ = parse_output(out_fpath(fpath), [[1, 3, 100, 3, 500, 1], None], True)
		distances.append((position - 1) / 2)

	plot.peligrosidad(distances, list(ti_range), fpath)
	print('isotherm_by_inner DONE')

def isotherm_by_radii(mp1_range, fpath):
	print(f'isotherm_by_radii mp1_range {mp1_range} fpath {fpath}')

	distances = []
	for mp1 in mp1_range:
		create_example(1500, mp1, fpath)
		run(in_fpath(fpath), out_fpath(fpath), 0, True)
		_, [[position, _, _]], _ = parse_output(out_fpath(fpath), [[1, 3, mp1, 3, 500, 1], None], True)
		distances.append((position - 1) / 2)
	plot.peligrosidad(distances, list(mp1_range), fpath, True)
	print('isotherm_by_radii DONE')

if __name__ == '__main__':
	isotherm_by_inner(range(500, 7000, 10), '../data/isotherm/by_inner') 
	isotherm_by_radii(range(3, 50, 1), '../data/isotherm/by_radii')

#TODO: These two can be merged into one function
