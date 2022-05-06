import numpy as np

from utils import *
import plot

def example_uniform(data, ti_step, te_step, fpath):
	[_, _, mp1, n, _, _], _ = data

	T = [
		[1500 + i * ti_step for i in range(n)] + [250 + i * te_step for i in range(n)], #A: Caso 0
		[1500 + i * ti_step for i in range(n)] + [250 for i in range(n)], #A: Caso 1
		[1500 + i * ti_step for i in range(n)] + [250 - (n - i) * te_step for i in range(n)], #A: Caso 2
	]

	with open(in_fpath(fpath), 'w') as fout:
		fout.write(f'{" ".join([str(x) for x in data[0]])}\n')
		for inst in T:
			fout.write(f'{" ".join([str(t) for t in inst])}\n')

def uniform(ti_step, te_step, fpath, replace = True):
	data = [1, 3, 25, 25, 500, 3], None

	if replace:
		example_uniform(data, ti_step, te_step, fpath)
		run(in_fpath(fpath), out_fpath(fpath), 1, profiling = True)
	
	plot.complete(fpath)

if __name__ == '__main__':
	uniform(50, 50, '../data/uniform/uniform', True)
