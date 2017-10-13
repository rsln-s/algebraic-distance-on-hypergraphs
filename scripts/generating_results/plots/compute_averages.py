import csv

partitioners = ['/patoh.csv', '/hmetis.csv', '/zoltan.csv']

folders = ['big_bench', 'all_social'] #, 'communities', 'snap']

overall = []
for partitioner in partitioners:
	ratios = []
	for folder in folders:
		file_name = folder+partitioner
		with open(file_name, 'r') as f:
			r = csv.reader(f, delimiter=';')
			for row in r:
				ratio = float(row[2])
				ratios.append(ratio)
				overall.append(ratio)
	print(partitioner, sum(ratios)/len(ratios))
print("overall", sum(overall)/len(overall))
