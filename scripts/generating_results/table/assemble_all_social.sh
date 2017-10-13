benchs=( hmetis.csv zoltan.csv patoh.csv )

for b in "${benchs[@]}"
do
		cat "communities_plots/"$b "snap_plots/"$b > "all_social_plots/"$b
done
