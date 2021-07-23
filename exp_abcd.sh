expset_arr=("d" "c" "b" "a")
T="200"
plot_rate="0.5"
for expset in ${expset_arr[@]};do
    echo "Now doing \"python main.py --expset $expset --T $T --plot_rate $plot_rate\""
    python main.py --expset $expset --T $T --plot_rate $plot_rate &> /dev/null
    # stderr is closed that it will not show wich picture is drawing
done
