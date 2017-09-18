#!/usr/bin/env bash



BENCHMARK_DIR="benchmark-instances"
if [ ! -d $BENCHMARK_DIR ]; then
 echo "#-- Downloading benchmark instances --#"
 mkdir $BENCHMARK_DIR
 cd $BENCHMARK_DIR
 wget http://www.cse.unsw.edu.au/~dcoa057/benchmark-instances.tar.gz
 tar -xzf *.tar.gz
 rm *.tar.gz
 cd ../
fi

SUITES=(20 50 75 100)

benchmark() {
  echo "$@"
  echo ""  
  total_timeout=0
  total_timein=0
  total_total=0
  for s in "${SUITES[@]}"; do
    echo "$s variables"
    suite_benchmark $s $@
    total_timein=$((total_timein + timein))
    total_timeout=$((total_timeout + timeout))
    total_total=$(echo $total_total + $total | bc -l)
  done
  echo "### TOTALS ###"
  average=$(echo $total_total / $total_timein | bc -l)
  average=$(printf "%.3f" $average)
  echo "Instances solved [$total_timein] - Timed-out [$total_timeout] - Average time(s) [$average]"
  echo ""
}

suite_benchmark () {
 suite=$1
 shift
 timeout=0
 timein=0
 total=0
 n=$(ls -1q $BENCHMARK_DIR/uf$suite-*.cnf | wc -l)
 remaining=$n
 percent=0
 echo -ne "Instances solved [$timein] - Timed-out [$timeout] - Remaining [$remaining] ($percent%)         \r"
 for f in $BENCHMARK_DIR/uf$suite-*.cnf; do
   if output=$( (/usr/bin/time --quiet -f "%U" python3 solver.py $@ $f > /dev/null) 2>&1); then
     total=$(echo $total + $output | bc -l)
     timein=$((timein+1))
   else
     timeout=$((timeout+1))
   fi
   remaining=$((remaining-1))
   percent=$((100 - (100*remaining/n)))
   echo -ne "Instances solved [$timein], Timed-out [$timeout], Remaining [$remaining] ($percent%)        \r"
 done
 echo ""
 average=$(echo $total / $timein | bc -l)
 average=$(printf "%.3f" $average)
 echo "Average time(s) [$average]"
}


echo "Exhaustive UP & PL"
benchmark "--choose-type=dlis --UP-interval=1 --PL-interval=1"

echo "UP & PL every 2nd level"
benchmark "--choose-type=dlis --UP-interval=2 --PL-interval=2"

echo "UP & PL every 3rd level"
benchmark "--choose-type=dlis --UP-interval=3 --PL-interval=3"

echo "Only PL"
benchmark "--choose-type=dlis --UP-interval=0 --PL-interval=1"

echo "Only UP"
benchmark "--choose-type=dlis --UP-interval=1 --PL-interval=0"

echo "No UP, No PL"
benchmark "--choose-type=dlis --UP-interval=0 --PL-interval=0"

