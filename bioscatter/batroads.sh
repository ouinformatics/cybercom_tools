for date in $(seq 20110408 20110430); do  
    for ts in $(g.mlist -r rast map=UNQC_CREF pat="^UNQC_CREF.${date}.\(00\|01\|02\|03\|04\|05\)\(00\|30\).*"); do
        echo -n "${ts} ->";
        r.mapcalc lin_${ts}="eval(lin=${ts} + 13.36697, if(lin >= 5, lin, 0) )"; 
    done; 
    echo ${date}; r.series --o input=$(g.mlist map=jduckles pat="lin_UNQC_CREF.${date}.*" sep=,) output=batroad_sum_${date} method=sum;
done
