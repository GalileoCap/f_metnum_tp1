import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import subprocess

def run(fpath, method):
	subprocess.run(f'../tp1.debug {fpath}.in {fpath}.debug.out {method}', shell = True, capture_output = True)

def get_data(fpath, ninst):
	data = [ #A: Each instance from the output
		inst.split(' ')[:-1] #NOTE: The last one is always empty
		for inst in subprocess.run(
			f'cat {fpath}.debug.out', shell = True, capture_output = True
		).stdout.decode('utf-8').split('\n')
	][:-1] #NOTE: The last line is always empty

	times = [int(x) for x in data[0]]
	if len(times) != ninst: #A: Split LU
		times = (times[0], times[1:])
	isos = [[float(x) for x in inst] for inst in data[1:ninst + 1]] #A: Skip times
	temps = [[float(x) for x in inst] for inst in data[ninst + 1:]] #A: The rest

	return times, isos, temps

def create_random_example(name, mp1, n, iso, ninst):
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

def plot_temp(fpath, mp1, n, ninst): #TODO: Plotlyze
	_, _, temps = get_data(fpath, ninst)

	for inst, temp in enumerate(temps):
		r = np.tile(np.linspace(0, 1, mp1), (n, 1))
		z = np.array(temp).reshape(mp1, n).transpose()

		fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

		# ax.set_title('Temperatura dentro del horno')
		ax.grid(False)
		ax.set_yticklabels([])

		grafico = ax.pcolor(
			np.tile(np.linspace(0, 2 * np.pi, n + 1)[:-1], (mp1, 1)).transpose(),
			r, z,
			cmap='jet'
		)
		fig.colorbar(grafico)

		plt.savefig(f'{fpath}.{inst}.png')

def plot_isotherm(fpath, mp1, n, ninst):
	_, isos, _ = get_data(fpath, ninst)

	for inst, iso in enumerate(isos):
		iso.append(iso[0]) #A: Para que la isoterma se "pegue" bien al dar la vuelta
		theta = np.linspace(0, 360, n + 1) #NOTE: Plotly expects angles

		fig = px.line_polar(
			r = iso, range_r = (1, 2),
			theta = theta, start_angle = 0, direction = 'counterclockwise'
		)
		# fig.update_layout(
			# title = 'Posición de la isoterma'
		# )
		fig.write_image(f'{fpath}.isotherm.{inst}.png')

def plot_times(reps, mp1_range, n_range, ninst):
	print('plot_times', reps, mp1_range, n_range, ninst)

	df = pd.DataFrame()
	for mp1 in mp1_range:
		print('plot_times mp1', mp1)
		for n in n_range:
			for _ in range(reps):
				fpath = create_random_example('times', mp1, n, 500, ninst)

				run(fpath, 0)
				_solve_gauss, _, _ = get_data(fpath, ninst)
				df = pd.concat([df, pd.DataFrame([{
					'mp1': mp1, 'n': n, 'size': mp1 * n,
					'method': 'Gauss', 'solve': _solve_gauss[0], #TODO: Save different instances
				}])], ignore_index = True)

				run(fpath, 1)
				(_lu, _solve_lu), _, _ = get_data(fpath, ninst)
				df = pd.concat([df, pd.DataFrame([{
					'mp1': mp1, 'n': n, 'size': mp1 * n,
					'method': 'LU', 'solve': _solve_lu[0], 'lu': _lu, 'ratio': _solve_lu[0] / _solve_gauss[0]
				}])], ignore_index = True)

	df['%lu'] = df['solve'] / df['lu']
	lu = df[df['method'] == 'LU']
	
	fig = px.box(df, x = 'size', y = 'solve', color = 'method', log_y = True) #TODO: Remove extreme outliers
	fig.update_layout(
		# title = f'Tiempo para resolver el sistema ({reps} reps)',
		legend_title = 'Método',
		xaxis_title = 'Tamaño de la matriz (elementos)',
		yaxis_title = 'Tiempo (ns, log)',
	)
	fig.write_image('../data/times.solve.png')

	fig = px.box(df, x = 'size', y = 'solve', color = 'method', log_y = True) #TODO: Remove extreme outliers
	fig.update_layout(
		# title = f'Tiempo para resolver el sistema ({reps} reps)',
		legend_title = 'Método',
		xaxis_title = 'Tamaño de la matriz (elementos)',
		yaxis_title = 'Tiempo (ns, log)',
	)
	fig.write_image('../data/times.solve.png')

	# fig = px.scatter_3d(solve, x = 'mp1', y = 'n', z = 'solve', color = 'method', log_z = True)
	# fig.update_layout(
		# title = 'Tiempo para resolver el sistema',
		# legend_title = 'Método',
		# xaxis_title = 'Cantidad de radios',
		# yaxis_title = 'Cantidad de ángulos',
		# zaxis_title = 'Tiempo promedio (ns, log)',
	# )
	# fig.write_image('../data/times.solve3d.png')
	# fig.write_html('../data/times.solve3d.html')

	fig = px.box(lu, x = 'size', y = 'ratio')
	fig.update_layout(
		# title = f'Relación entre LU y Gauss',
		xaxis_title = 'Tamaño de la matriz (elementos)',
		yaxis_title = 'Relación',
	)
	fig.write_image('../data/times.ratio_lu_gauss.png')

	fig = px.box(lu, x = 'size', y = 'solve', log_y = True)
	fig.update_layout(
		# title = f'Tiempo para calcular la factorización LU ({reps} reps)',
		xaxis_title = 'Tamaño de la matriz (elementos)',
		yaxis_title = 'Tiempo (ns, log)',
	)
	fig.write_image('../data/times.lu.png')

	fig = px.box(lu, x = 'size', y = '%lu')
	fig.update_layout(
		# title = f'Relación entre el tiempo resolver y el tiempo para calcular LU ({reps} reps)',
		xaxis_title = 'Tamaño de la matriz (elementos)',
		yaxis_title = 'Relación',
	)
	fig.write_image('../data/times.pct_lu.png')

	print('plot_times DONE')

def create_and_plot(name, mp1, n, ninst):
	print('create_and_plot', name, mp1, n, ninst)

	fpath = create_random_example(name, mp1, n, 500, ninst)
	run(fpath, 0)
	plot_temp(fpath, mp1, n, ninst)
	plot_isotherm(fpath, mp1, n, ninst)

	print('create_and_plot DONE')

def peligrosidad_example(ti, te, iso, mp1 = 100, n = 3):
	fpath = f'../data/peligrosidad'
	with open(f'{fpath}.in', 'w') as fout:
		fout.write(f'1 2 {mp1} {n} {iso} 1\n') #TODO: Change radii
		fout.write(f'{" ".join([str(ti)] * n + [str(te)] * n)}\n')

	return fpath

def peligrosidad(sti = 500, ste = 150, step = 1):
	distances = [0]
	ti, te = sti, ste
	while distances[-1] <= 0.90:
		fpath = peligrosidad_example(ti, te, 500)
		run(fpath, 0)
		_, isos, _ = get_data(fpath, 1)
		position = isos[0][0]
		distances.append(position / 2)
		ti += step

		# print('peligrosidad', ti, te, distances[-1], position)

	fig = go.Figure()
	fig.add_trace(go.Scatter(
		x = list(range(sti, ti, step)),
		y = [x * 100 for x in distances[1:]]
	))
	fig.update_layout(
		# title = 'Distancia de la isoterma (temperatura externa fija)',
		xaxis_title = 'Temperatura interna (ºC)',
		yaxis_title = 'Posición de la isoterma (% de la pared)',
	)
	fig.write_image('../data/peligrosidad.distance.png')

	print('peligrosidad DONE', ti, te)

if __name__ == '__main__':
	create_and_plot('test', 50, 50, 1)
	plot_times(1000, range(2, 50), [4], 1) #TODO: Multiple intances
	peligrosidad(step = 10) #TODO: step = 1
