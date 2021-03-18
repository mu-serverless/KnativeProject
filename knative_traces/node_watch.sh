for I in {1..14400}:
do
echo -e ">$(date +%s)\n$(kubectl top node)" >> nodes_log.txt
sleep .5
done

