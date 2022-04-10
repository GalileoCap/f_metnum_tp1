import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import subprocess

def run(fpath, method, mode):
	subprocess.run(f'../tp1{mode} {fpath}.in {fpath}{mode}.out {method}', shell = True, capture_output = True)

def run_all(fpath, method):
	for mode in ['', '.isotherm', '.profiling']:
		run(fpath, method, mode)

def get_data(fpath, method, mode = ''):
	data = [ #A: Each instance from the output
		inst.split(' ')
		for inst in subprocess.run(
			f'cat {fpath}{mode}.out', shell = True, capture_output = True
		).stdout.decode('utf-8').split('\n')
	][:-1] #NOTE: The last line is always empty

	if mode == '':
		return [[float(x) for x in inst[:-1]] for inst in data]
	elif mode == '.profiling':
		if method == 0: #A: Gauss
			return [int(inst) for inst in data[0][:-1]] #A: Split resulting vector and time 
		else: #A: LU
			return int(data[0][0]), [int(inst) for inst in data[0][1:-1]] #A: Split LU
	else: #A: mode == '.isotherm'
		return [[float(x) for x in inst[:-1]] for inst in data]

def create_example(name, mp1, n, iso, ninst):
	inst = []
	for i in range(ninst):
		ti = ' '.join([str(t) for t in (np.random.standard_normal(n) * 10 + 1500)])
		te = ' '.join([str(t) for t in (np.random.standard_normal(n) * 10 + 150)])
		inst.append(' '.join([ti, te]))

	fpath = f'../data/{name}'
	with open(f'{fpath}.in', 'w') as fout:
		fout.write(f'1 2 {mp1} {n} {iso} {ninst}\n') #TODO: Change radii
		for t in inst:
			fout.write(f'{t}\n')

	return fpath

def plot_temp(fpath, mp1, n):
	results = get_data(fpath, 1)

	for inst, result in enumerate(results):
		r = np.tile(np.linspace(0, 1, mp1), (n, 1))
		z = np.array(result).reshape(mp1, n).transpose()

		fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

		ax.set_title('Alto horno')
		ax.grid(False)
		ax.set_yticklabels([])

		grafico = ax.pcolor(
			np.tile(np.linspace(0, 2 * np.pi, n + 1)[:-1], (mp1, 1)).transpose(),
			r, z,
			cmap='jet'
		)
		fig.colorbar(grafico)

		plt.savefig(f'{fpath}.{inst}.png')

def plot_isotherm(fpath, mp1, n):
	results = get_data(fpath, 1, '.isotherm')

	for inst, result in enumerate(results):
		result.append(result[0]) #A: Para que la isoterma se "pegue" bien al dar la vuelta
		theta = np.linspace(0, 2 * np.pi, n + 1)

		fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
		ax.set_title('Isoterma')
		ax.grid(True)
		ax.plot(theta, [x for x in result])
		ax.set_rticks(np.linspace(1, 2, 5))

		plt.savefig(f'{fpath}.isotherm.{inst}.png')

def plot_times(reps, mp1_range, n_range):
	print('plot_times', reps, mp1_range, n_range)

	x = []
	lu = []
	solve_lu = []
	solve_gauss = []
	for mp1 in mp1_range:
		print('plot_times mp1', mp1)
		for n in n_range:
			_lu = []
			_solve_lu = []
			_solve_gauss = []
			for _ in range(reps):
				fpath = create_example('times', mp1, n, 500, 1)

				run(fpath, 0, '.profiling')
				this_solve = get_data(fpath, 0, '.profiling')
				_solve_gauss.append(this_solve)

				run(fpath, 1, '.profiling')
				this_lu, this_solve = get_data(fpath, 1, '.profiling')
				_lu.append(this_lu)
				_solve_lu.append(this_solve[0])
			lu.append(np.log(np.mean(_lu)))
			solve_lu.append(np.log(np.mean(_solve_lu)))
			solve_gauss.append(np.log(np.mean(_solve_gauss)))
			x.append(mp1 * n)
		
	fig = go.Figure()
	fig.add_trace(go.Scatter(
		name = 'LU',
		x = x,
		y = solve_lu
	))
	fig.add_trace(go.Scatter(
		name = 'Gauss',
		x = x,
		y = solve_gauss
	))
	fig.update_layout(
		title = 'Tiempo para resolver el sistema',
		legend_title = 'Método',
		xaxis_title = 'Tamaño de la matriz (elementos)',
		yaxis_title = 'Tiempo promedio (ns, log)',
	)
	fig.write_image('../data/times.solve.png')

	fig = go.Figure()
	fig.add_trace(go.Scatter(
		x = x,
		y = lu
	))
	fig.update_layout(
		title = 'Tiempo para calcular la factorización LU',
		xaxis_title = 'Tamaño de la matriz (elementos)',
		yaxis_title = 'Tiempo promedio (ns, log)',
	)
	fig.write_image('../data/times.lu.png')

	print('plot_times DONE')

def create_and_plot(name, mp1, n, ninst):
	print('create_and_plot', name, mp1, n, ninst)

	fpath = create_example(name, mp1, n, 500, ninst)
	run_all(fpath, 1)
	plot_temp(fpath, mp1, n)
	plot_isotherm(fpath, mp1, n)

	print('create_and_plot DONE')

if __name__ == '__main__':
	create_and_plot('test', 15, 50, 1)
	plot_times(100, range(2, 10), range(4, 5))
