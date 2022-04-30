import numpy as np
import subprocess

def in_fpath(fpath):
	return f'{fpath}.in'

def out_fpath(fpath):
	return f'{fpath}.out'

def expected_fpath(fpath):
	return f'{fpath}.expected'

def pyout_fpath(fpath):
	return f'{fpath}.py.out'

def img_fpath(fpath):
	return f'{fpath}.png'

def html_fpath(fpath):
	return f'{fpath}.html'

def df_path(fpath):
	return f'{fpath}.csv.gz'

def gauss_df(df):
	return df[(df['method'] == 'Gauss')]

def lu_df(df):
	return df[(df['method'] == 'LU')]

def split(l, n):
	return [l[i*n:(i + 1)*n] for i in range(len(l) // n)]

def run(fpath_in, fpath_out, method, profiling = False, special = ''):
	subprocess.run(
		f'../tp1{".profiling" if profiling else ""}{special} {fpath_in} {fpath_out} {method}',
		shell = True, capture_output = True
	)

def parse_input(fpath):
	with open(fpath, 'r') as fin:
		data = [[float(x) for x in line.split()] for line in fin.read().split('\n')[:-1]]
	ri, re, mp1, n, iso, ninst = data[0]
	return [ri, re, int(mp1), int(n), iso, int(ninst)], data[1:]	

def parse_output(fpath, data, debug = False):
	[_, _, mp1, n, _, ninst], _ = data
	with open(fpath, 'r') as fin:
		data = fin.read().split('\n')[:-1]
	if not debug:
		times = None
		isos = None
		temps = [np.array(inst) for inst in split([float(x) for x in data], mp1 * n)]
	else: 
		times = [int(x) for x in data[0].split()]
		if len(times) != ninst: #A: Split LU
			times = (times[0], times[1:])
		else:
			times = (np.NaN, times)
		isos = [[float(x) for x in inst.split()] for inst in data[1:ninst+1]] #A: Skip times
		temps = [np.array(inst) for inst in split([float(x) for x in data[ninst+1:]], mp1*n)] #A: The rest
	return times, isos, temps

def compare_results(a, b):
	res = True
	for inst in range(len(a)):
		res = res and all(np.equal(a[inst], b[inst]))
	return res

def create_random_example(fpath, data, ti = 1500, te = 150):
	[ri, re, mp1, n, iso, ninst], _ = data

	inst = []
	for i in range(ninst):
		Ti = ' '.join([str(t) for t in (np.random.standard_normal(n) * 10 + ti)])
		Te = ' '.join([str(t) for t in (np.random.standard_normal(n) * 10 + te)])
		inst.append(' '.join([Ti, Te]))

	with open(in_fpath(fpath), 'w') as fout:
		fout.write(f'{ri} {re} {mp1} {n} {iso} {ninst}\n')
		for T in inst:
			fout.write(f'{T}\n')

	return fpath

