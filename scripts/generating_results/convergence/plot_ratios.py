import os
import numpy as np
import matplotlib.pyplot as plt

inp_files_all = os.listdir("ratios/")
inp_files = ["ratios/"+x for x in inp_files_all]

all_ratios = list()

for fname in inp_files:
	with open(fname, 'r') as f:
		r = [[],[]]
		for row in f:
			for i in range(2):
				r[i].append(float(row.split()[i]))
		all_ratios.append(r)

#plt.yscale('log')

plt.rcParams["figure.figsize"] = [10.0, 4.0]

for r in all_ratios:
	plt.plot(r[0][:50],r[1][:50],'-')

plt.savefig('convergence.png', figsize=(10, 4), dpi=300)
