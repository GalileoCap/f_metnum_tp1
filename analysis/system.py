import numpy as np
import pandas as pd

from utils import *

def matrix(data):
	[ri, re, mp1, n, _, _], _ = data
	dr, dt = (re - ri) / mp1, 2 * np.pi / n

	radius = lambda i, ri=ri, dr=dr : ri + dr * i
	alpha = lambda i, ri=ri, dr=dr : (1 / dr**2) + (-1 / (radius(i) * dr))
	beta = lambda i, ri=ri, dr=dr : (-2 / dr**2) + (1 / (radius(i) * dr)) + (-2 / (radius(i) * dt)**2)
	gamma = lambda i, ri=ri, dr=dr : 1 / dr**2
	chi = lambda i, ri=ri, dr=dr : 1 / (radius(i) * dt)**2

	M = np.identity(mp1 * n)
	for i in range(1, mp1 - 1):
		for j in range(n):
			row = i * n + j

			#A: This angle/radius
			M[row, row] = beta(i)

			#A: Previous angle, same radius
			if (j > 0): M[row, row - 1] = chi(i) 
			else: M[row, row + n - 1] = chi(i)

			#A: Next angle, same radius
			if ((j+1) < n): M[row, row + 1] = chi(i) 
			else: M[row, row - n + 1] = chi(i)

			M[row, row - n] = alpha(i) #A: Same angle, previous radius
			M[row, row + n] = gamma(i) #A: Same angle, previous radius
			
	return M

def result(data):
	[_, _, mp1, n, _, ninst], temps = data

	return [
			np.array(temps[inst][:n] + [0] * ((mp1-2)*n) + temps[inst][-n:])
		for inst in range(ninst)
	]

def solve(M, b):
	return [
		np.around(np.linalg.solve(M, _b), 6)
		for _b in b
	]

def calc_isotherm(T, data):
	[ri, re, mp1, n, iso, _], _ = data
	dr = (re - ri) / mp1

	res = []
	for i in range(n): #A: For each angle
		j = 0
		while j < (mp1-1) and T[j * n + i] > iso: #A: Until I find it or run out of range 
			j += 1
		res.append(ri + j * dr)

	return res

def error_range(M, b, x, x_bar, data):
	[_, _, mp1, n, _, _], _ = data

	b = b.reshape((1, mp1*n))
	b_bar = M.dot(x_bar) 
	x = x.reshape((1, mp1*n)) 
	x_bar = x_bar.reshape((1, mp1*n))

	return (np.linalg.norm(x - x_bar) / np.linalg.norm(x)) <= (np.linalg.cond(M) * np.linalg.norm(b - b_bar) / np.linalg.norm(b))
