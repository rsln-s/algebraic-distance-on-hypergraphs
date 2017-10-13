# merges results for different partitioners and returns them as latex table or ratios for plotting
import csv
import sys
import os
import operator

bench_name = 'communities'

# prints latex table without the header
def print_in_latex_format(table):
	for line in table:
		try:
			cuts = [float(el) for el in line[6:]]
			minindex = cuts.index(min(cuts)) + 6
			line[minindex] = r"*" + line[minindex] + r"*" # highlight the largest value with bold font
		except:
			pass # ignore header
		line[0] = line[0].replace("_", r"\_")
		print(" | ".join(str(el) for el in line) + " \n")

# prints ratios in the format accepted by  ../plots/create_plots.py
def print_ratios(table, files):
	for i in range(1, len(files)):
		fname = files[i] + ".csv"
		with open(bench_name+'_plots'+'/'+fname, 'w') as f:
			w = csv.writer(f, delimiter=';')
			for line in table:
				if '-1' in line:
					print(line)
					continue
				try:
					#if float(line[6+i])/float(line[6]) > 5.0:
					#	print("Found a line with suspiciously high ratio", float(line[6+i])/float(line[6]), line)
					w.writerow([line[4], line[5], float(line[6+i])/float(line[6])])
				except IndexError:
					pass
					#print("Couldn't compute ratios for ", line) 



big_bench_files = sorted(os.listdir(bench_name))

first_file = True

big_bench_files = ["alg_dist", "zoltan", "patoh", "hmetis"]

for i in range(0, len(big_bench_files)):
	fname = big_bench_files[i] + ".csv"
	with open(bench_name+'/'+fname) as f:
		r = csv.reader(f, delimiter=';')
		if first_file:
			b_dict = {row[0]: row[1:] for row in r}
			first_file = False
		else:
			tmp_dict = {row[0]:row[-1] for row in r}
			for k, v in tmp_dict.items():
				if k in b_dict:
					b_dict[k].extend([v])
				else:
					pass
					#print("Can't find the key", k)

# output = sorted([b_dict[k] for k in b_dict.keys()], key=operator.itemgetter(0, 4, 5))
# print_ratios(output, big_bench_files)

with open('csvs/'+bench_name+'_merged.csv', 'w') as f:
	w = csv.writer(f, delimiter=';')
	header = ["Graph name", "|V|", "|E|", "|pins|", "Number of parts", "Imbalance"] + big_bench_files
	output = sorted([b_dict[k] for k in b_dict.keys()], key=operator.itemgetter(0, 4, 5))
	print_in_latex_format([header]+output)
#	w.writerow(header)
#	for line in output:
#		w.writerow(line)
