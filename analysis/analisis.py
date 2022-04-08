# import numpy as np
# import pandas as pd
from subprocess import run

def call_process(path_in, path_out, method):
	tp1 = run('../tp1.debug %s %s %s' % (path_in, path_out, method), shell = True, capture_output = True)
	cat = run('cat %s' % (path_out), shell = True, capture_output = True)
	stdout = cat.stdout.decode('UTF-8')
	return [inst.split(', ') for inst in stdout.split('\n')][:-1]

fpath = '../data/example%s' % 0

call_process(f'{fpath}.in', f'{fpath}.out', 0)
