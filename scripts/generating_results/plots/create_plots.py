import csv
import sys
from collections import defaultdict
import matplotlib
import matplotlib.pyplot as plt
import math
import numpy as np

#folder = 'all_social'
folder = 'big_bench'

def read_file_into_dict(file_name, dict):
	with open(file_name, 'r') as f:
		r = csv.reader(f, delimiter=';')
		for row in r:
			try:
				ratio = float(row[2])
#				if folder == 'big_bench':
				if ratio < 1.5:
					key = row[0]+row[1]+'small'
				else:
					key = row[0]+row[1]+'large'
#				else:
#					key = row[0]+row[1]
				dict[key].append(ratio)
			except ValueError:
				print('Couldnt convert to float:', row[2])


patoh_file_name = folder + '/patoh.csv'
hmetis_file_name = folder + '/hmetis.csv'
zoltan_file_name = folder + '/zoltan.csv'

patoh = defaultdict(list)
hmetis = defaultdict(list)
zoltan = defaultdict(list)

parts = ['2', '4', '8', '16', '32', '64', '128']
imbals = ['1.03', '1.05', '1.1']

read_file_into_dict(patoh_file_name, patoh)
read_file_into_dict(hmetis_file_name, hmetis)
read_file_into_dict(zoltan_file_name, zoltan)

matplotlib.rcParams.update({'font.size': 8})

#if folder == 'big_bench':
vals = ['small', 'large']
#else:
#	vals = ['']

for val in vals:
	f, axarr = plt.subplots(len(parts), len(imbals), figsize=(8,11))
	for i in range(len(parts)):
		for j in range(len(imbals)):
			key = parts[i]+imbals[j]+val
			axarr[i,j].plot(sorted(patoh[key]), 'b.')
			axarr[i,j].plot(sorted(hmetis[key]), 'r.')
			axarr[i,j].plot(sorted(zoltan[key]), 'g.')
			if val != 'large':
				patoh_improvement = float(len(list(filter(lambda x: x >= 1.0, patoh[key]))))/float(len(patoh[key]))
				hmetis_improvement = float(len(list(filter(lambda x: x >= 1.0, hmetis[key]))))/float(len(hmetis[key]))
				zoltan_improvement = float(len(list(filter(lambda x: x >= 1.0, zoltan[key]))))/float(len(zoltan[key]))
				axarr[i,j].annotate('Fraction improved: ', xy=(1, 0), xycoords='axes fraction', xytext=(-290, 20), textcoords='offset pixels', horizontalalignment='right', verticalalignment='bottom')
				axarr[i,j].annotate('{:.2f}'.format(patoh_improvement), xy=(1, 0), color='blue', xycoords='axes fraction', xytext=(-200, 20), textcoords='offset pixels', horizontalalignment='right', verticalalignment='bottom')
				axarr[i,j].annotate('{:.2f}'.format(hmetis_improvement), xy=(1, 0), color='red', xycoords='axes fraction', xytext=(-110, 20), textcoords='offset pixels', horizontalalignment='right', verticalalignment='bottom')
				axarr[i,j].annotate('{:.2f}'.format(zoltan_improvement), xy=(1, 0), color='green', xycoords='axes fraction', xytext=(-20, 20), textcoords='offset pixels', horizontalalignment='right', verticalalignment='bottom')
			num_els = max(len(hmetis[key]), len(patoh[key]), len(zoltan[key]))
			axarr[i,j].plot((0.0,num_els), (1.0,1.0), 'k-')
			axarr[i,j].set_title('Num parts: '+parts[i]+' Imbalance: '+imbals[j])
			if round(int((num_els - 1) / 4.0), -1) != 0:
				x_ticks_step = round(int((num_els - 1) / 4.0), -1)
			else:
				x_ticks_step = 1
			try:
				y_min = round(min(hmetis[key] + patoh[key] + zoltan[key]), 1)
				y_max = round(max(hmetis[key] + patoh[key] + zoltan[key]), 1)
			except ValueError:
				print('Error with min(), key:', key, hmetis[key], patoh[key], zoltan[key])
				sys.exit(-1)
			y_ticks_step = (y_max - y_min) / 5.0
			y_ticks_list = np.arange(y_min, y_max + 0.1, y_ticks_step)
			y_ticks_list = np.append(y_ticks_list[(y_ticks_list < (1.0 - (y_ticks_step / 2.0))) | (y_ticks_list > (1.0 + (y_ticks_step / 2.0)))], 1.0)
			try:
				axarr[i,j].xaxis.set_ticks(np.arange(0, num_els, x_ticks_step))
			except ZeroDivisionError:
				print('Encountered ZeroDivisionError: num_els ', num_els, ' x_ticks_step: ', x_ticks_step, 'i = ', i, ' j = ', j)
				sys.exit(-1)
			axarr[i,j].yaxis.set_ticks(y_ticks_list)
			if num_els > 20:
				axarr[i,j].set_xlim([-2,num_els+2])
			else:
				axarr[i,j].set_xlim([-0.5,num_els+0.5])
	f.subplots_adjust(hspace=0.2)
	f.subplots_adjust(wspace=0.05)
	f.subplots_adjust(right=0.98)
	f.subplots_adjust(top=0.98)
	f.subplots_adjust(left=0.05)
	f.subplots_adjust(bottom=0.02)

	for i in range(0,len(parts)):
		plt.setp([a.get_xticklabels() for a in axarr[i, :]], visible=False)
	for j in range(1,3):
		plt.setp([a.get_yticklabels() for a in axarr[:, j]], visible=False)
	if folder == 'all_social':
		outfname = 'soc_'
	else:
		outfname = ''
	outfname += 'out_'+val+'.png'
	plt.savefig(outfname, dpi=300)
