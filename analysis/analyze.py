import numpy as np
import pandas as pd
from scipy import stats

from utils import *
import plot
import system

def times(reps, mp1_range, n_range, ninst_range, fpath, replace = False):
	for ninst in ninst_range:
		print('times', reps, mp1_range, n_range, ninst)

		_fpath = f'{fpath}.{ninst}'
		df = pd.DataFrame()
		if not replace:
			df = pd.read_csv(df_path(_fpath), index_col = 0)
			print('times read')
		else:
			for mp1 in mp1_range:
				print('times mp1', mp1)
				for n in n_range:
					for _ in range(reps):
						data = [[1, 2, mp1, n, 500, ninst], None]
						e_fpath = create_random_example(fpath, data)

						for method in ['Gauss', 'LU']:
							run(in_fpath(e_fpath), out_fpath(e_fpath), int(method == 'LU'), True)
							(lu, times), _, _ = parse_output(out_fpath(e_fpath), data, True)
							df = pd.concat([df, pd.DataFrame([{
								'mp1': mp1, 'n': n,
								'method': method,
								'time': np.sum(times), 'lu': lu
							}])], ignore_index = True)
			df.to_csv(df_path(_fpath))

		# print(df.describe())
		df = df[(np.abs(stats.zscore(df['time']))) < 3] #A: Remove extreme outliers
		# df = df[(np.abs(stats.zscore(df['lu']))) < 3]
		# print(df.describe())

		df['size'] = df['mp1'] * df['n']
		df['%lu'] = df['time'] / df['lu']
		df['time+lu'] = df['time'] + df['lu']

		plot.t_solve(df, _fpath)
		plot.t_solve_lu(df, _fpath)
		plot.t_pct_lu(df, _fpath)

	print('times DONE')

def peligrosidad_example(ti, te, fpath):
	with open(in_fpath(fpath), 'w') as fout:
		fout.write(f'1 2 100 3 500 1\n')
		fout.write(f'{" ".join([str(ti)] * 3 + [str(te)] * 3)}\n')

	return fpath

def peligrosidad(sti, ste, step, fpath):
	print('peligrosidad', sti, ste, step)
	distances = [0]
	ti, te = sti, ste
	while distances[-1] <= 0.90:
		_fpath = peligrosidad_example(ti, te, fpath)
		run(in_fpath(_fpath), out_fpath(_fpath), 0, True)
		_, [[position, _, _]], _ = parse_output(out_fpath(fpath), [[1, 2, 100, 3, 500, 1], None], True)
		distances.append(position / 2)
		ti += step

	plot.peligrosidad(distances[1:], list(range(sti, ti, step)), fpath)
	print('peligrosidad DONE')

def complete(params, fpath):
	fpath = create_random_example(fpath, [params, None])
	run(in_fpath(fpath), out_fpath(fpath), 0, True)
	plot.complete(fpath)

if __name__ == '__main__':
	complete([1, 2, 15, 15, 500, 1], '../data/complete.simple')
	times(100, [2, 3], [4], [1, 2, 9], f'../data/times.simple', replace = True) 
	peligrosidad(500, 150, 100, '../data/peligrosidad.simple')

	complete([1, 2, 50, 50, 500, 1], '../data/complete')
	times(1000, range(2, 50), [4], [1, 2, 9], f'../data/times', replace = True)
	peligrosidad(500, 150, 1, '../data/peligrosidad')