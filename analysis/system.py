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

def check_tests(replace = True):
	print('check_tests', replace)
	for i in range(1, 4 + 1):
		print('check_tests', i)
		fpath = f'../data/tests_alu/test{i}'

		if replace:
			run(in_fpath(fpath), out_fpath(fpath), 0)

		data = parse_input(in_fpath(fpath))
		M = matrix(data)
		b = result(data)

		_, _, output = parse_output(out_fpath(fpath), data)
		_, _, expected = parse_output(expected_fpath(fpath), data)
		python = solve(M, b)

		[_, _, _, _, _, ninst], _ = data

		cvspy = compare_results(output, python) 
		cvsexpected = compare_results(output, expected)
		pyvsexpected = compare_results(python, expected)

		print('check_tests cvspy cvsexpected pyvsexpected', cvspy, cvsexpected, pyvsexpected)
		#TODO: Check differences

if __name__ == '__main__':
	check_tests(False)
