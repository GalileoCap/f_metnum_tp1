import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

def isotherms(isos, data, fpath):
	[ri, re, mp1, n, _, _], _ = data #TODO: Internal radius
	fig = go.Figure()
	theta = np.linspace(0, 360, n + 1) #NOTE: Plotly expects angles

	for name, iso in isos.items():
		# r = [x for x in iso if x >= ri and x <= re]
		r = iso
		# print(name, iso)
		if len(r) > 0: #A: Para que la isoterma se "pegue" bien al dar la vuelta
			r.append(r[0])
		fig.add_trace(go.Scatterpolar(
			r = r, 
			theta = theta,
			mode = 'lines',
			name = name
		))

	fig.update_polars(radialaxis = {'range': [ri, re]})
	fig.update_layout(
		# title = 'Posición de la isoterma',
		legend_title = 'Resultado'
	)
	#TODO: Peligrosidad
	fig.write_image(img_fpath(f'{fpath}.isotherm'))

def t_solve(df, fpath):
	fig = px.box(df, x = 'size', y = 'time', color = 'method', log_y = True) #TODO: Remove extreme outliers
	fig.update_layout(
		# title = f'Tiempo para resolver el sistema ({reps} reps)',
		legend_title = 'Método',
		xaxis_title = 'Tamaño de la matriz (elementos)',
		yaxis_title = 'Tiempo (μs, log)',
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
		yaxis_title = 'Tiempo (μs, log)',
	)
	fig.update_yaxes(type = 'log')
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

def peligrosidad(distances, x, fpath, radii = False, metals = False):
	# fig = px.scatter(x = x, y = distances)
	fig = go.Figure() 
	fig.add_trace(go.Scatter(
		x = x,
		y = distances,
		name="Isoterma"
	))
	fig.update_layout(
		# title = 'Distancia de la isoterma (temperatura externa fija)',
		xaxis_title = 'Temperatura interna (ºC)' if not radii else 'Cantidad de radios internos',
		yaxis_title = 'Porcentaje de la pared recorrida por la isoterma',
	)
	if metals:
		metals = {
			'Aluminio': 660,
			'Hierro': 1538,
			'Cobre': 1085,
			# 'Latón': 930,
			# 'Niquel': 1453,
			'Tungsteno': 3400
		}
		colors = ["green","blue","red","black"]
		k = 0
		for metal, temp in metals.items():
			fig.add_vline(x = temp,line_color=colors[k],annotation_text=metal, annotation_position="bottom left")#, annotation_text = metal, line_color=colors[k])
			k+=1
	# fig.update_layout(showlegend=True)
	fig.write_image(img_fpath(f'{fpath}'))

def complete(fpath):
	data = parse_input(in_fpath(fpath))
	_, isos, temps = parse_output(out_fpath(fpath), data, True)

	[_, _, _, _, _, ninst], _ = data
	for inst in range(ninst):
		_fpath = f'{fpath}.{inst}'
		temperature(temps[inst], data, _fpath)
		isotherms({'isotherm': isos[inst]}, data, _fpath)
