import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from utils import *

def temperature(result, data, fpath): #TODO: Plotlyze
	[_, _, mp1, n, _, _], _ = data
	
	r = np.tile(np.linspace(0, 1, mp1), (n, 1))
	z = np.array(result).reshape(mp1, n).transpose()

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

	plt.savefig(img_fpath(f'{fpath}.temperature'))

def isotherm(iso, data, fpath):
	[_, _, mp1, n, _, _], _ = data #TODO: Internal radius
	iso.append(iso[0]) #A: Para que la isoterma se "pegue" bien al dar la vuelta
	theta = np.linspace(0, 360, n + 1) #NOTE: Plotly expects angles

	fig = px.line_polar(
		r = iso, range_r = (1, 2),
		theta = theta, start_angle = 0, direction = 'counterclockwise'
	)
	# fig.update_layout(
		# title = 'Posición de la isoterma'
	# )
	#TODO: Peligrosidad
	fig.write_image(img_fpath(f'{fpath}.isotherm'))

def t_solve(df, fpath):
	fig = px.box(df, x = 'size', y = 'time', color = 'method', log_y = True) #TODO: Remove extreme outliers
	fig.update_layout(
		# title = f'Tiempo para resolver el sistema ({reps} reps)',
		legend_title = 'Método',
		xaxis_title = 'Tamaño de la matriz (elementos)',
		yaxis_title = 'Tiempo (ns, log)',
	)
	fig.write_image(img_fpath(f'{fpath}.t_solve'))

def t_solve_lu(df, fpath):
	gauss, lu = gauss_df(df), lu_df(df)

	fig = go.Figure()
	fig.add_trace(go.Box(name = 'Gauss', x = gauss['size'], y = gauss['time']))
	fig.add_trace(go.Box(name = 'LU', x = lu['size'], y = lu['time+lu']))
	fig.update_layout(
		# title = f'Tiempo para resolver el sistema teniendo en cuenta LU ({reps} reps)',
		legend_title = 'Método',
		xaxis_title = 'Tamaño de la matriz (elementos)',
		yaxis_title = 'Tiempo (ns, log)',
	)
	fig.write_image(img_fpath(f'{fpath}.t_solve_lu'))
	
def t_pct_lu(df, fpath):
	lu = lu_df(df)
	
	fig = px.box(lu, x = 'size', y = '%lu')
	fig.update_layout(
		# title = f'Relación entre el tiempo resolver y el tiempo para calcular LU ({reps} reps)',
		xaxis_title = 'Tamaño de la matriz (elementos)',
		yaxis_title = 'Relación',
	)
	fig.write_image(img_fpath(f'{fpath}.t_pct_lu'))

def peligrosidad(distances, x, fpath):
	# fig = px.scatter(x = x, y = distances)
	fig = go.Figure() 
	fig.add_trace(go.Scatter(
		x = x,
		y = distances
	))
	fig.update_layout(
		# title = 'Distancia de la isoterma (temperatura externa fija)',
		xaxis_title = 'Temperatura interna (ºC)',
		yaxis_title = 'Posición de la isoterma (% de la pared)',
	)
	fig.write_image(img_fpath(f'{fpath}'))

def complete(fpath):
	data = parse_input(in_fpath(fpath))
	_, isos, temps = parse_output(out_fpath(fpath), data, True)

	[_, _, _, _, _, ninst], _ = data
	for inst in range(ninst):
		_fpath = f'{fpath}.{inst}'
		temperature(temps[inst], data, _fpath)
		isotherm(isos[inst], data, _fpath)
