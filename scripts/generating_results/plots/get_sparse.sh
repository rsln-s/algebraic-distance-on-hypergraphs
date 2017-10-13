#!/bin/bash

for i in */*.mtx;
do
	filename=$i

	readarray -t lines < "$filename"


	for line in "${lines[@]}"; do
		[[ $line == \%* ]] && continue
		# expecting 3 numbers: rows, columns, entries
		args=(${line// / })
		sparsity=$(echo "${args[2]} / (${args[0]} * ${args[1]})" | bc -l)
		is_sparse=$(echo $sparsity'>0.5' | bc -l)
		if [ -z "$is_sparse" ]
		then
			echo "Something went wrong with "$i
			break
		fi
		if [ $is_sparse -eq 1 ]
		then
			echo $i" is not sparse"
		fi
		break
	done
done
