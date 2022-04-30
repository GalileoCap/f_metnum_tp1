import numpy as np
import pandas as pd
from scipy import stats

from utils import *
import plot
import system

def ninst_fpath(fpath, ninst):
	return f'{fpath}.{ninst}'

def times_run_one(mp1, n, ninst, reps, fpath):
	print('times_run_one mp1 n ninst reps', mp1, n, ninst, reps)
	df = pd.DataFrame()
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
	return df

def times_run_ninst(reps, mp1_range, n_range, ninst, fpath, replace = False):
	print('times_run', reps, mp1_range, n_range, ninst)

	df = pd.DataFrame()
	if not replace:
		df = pd.read_csv(df_path(ninst_fpath(fpath, ninst)), index_col = 0)
		print('times read')
	else:
		for mp1 in mp1_range:
			for n in n_range:
				df = pd.concat([df, times_run_one(mp1, n, ninst, reps, fpath)])
	df.to_csv(df_path(ninst_fpath(fpath, ninst)))
	return df

def times(reps, mp1_range, n_range, ninst_range, fpath, replace = False):
	for ninst in ninst_range:
		print('times', reps, mp1_range, n_range, ninst)

		df = times_run_ninst(reps, mp1_range, n_range, ninst, fpath, replace)

		# print(df.describe())
		df = df[(np.abs(stats.zscore(df['time']))) < 3] #A: Remove extreme outliers
		# df = df[(np.abs(stats.zscore(df['lu']))) < 3]
		# print(df.describe())

		df['time'] /= 1000 #A: Nanoseconds to microseconds
		df['lu'] /= 1000

		df['size'] = df['mp1'] * df['n']
		df['%lu'] = df['time'] / df['lu']
		df['time+lu'] = df['time'] + df['lu']

		plot.t_solve(df, ninst_fpath(fpath, ninst))
		plot.t_solve_lu(df, ninst_fpath(fpath, ninst))
		plot.t_pct_lu(df, ninst_fpath(fpath, ninst))

	print('times DONE')

if __name__ == '__main__':
	times(100, range(2, 10), range(3, 10), [1, 2, 9], f'../data/times/simple', replace = False) 
