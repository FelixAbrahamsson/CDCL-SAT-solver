#!/usr/bin/env bash

BENCHMARK_DIR="benchmark-instances"
if [ ! -d $BENCHMARK_DIR ]; then
  echo "#-- Downloading benchmark instances --#"
  mkdir $BENCHMARK_DIR
  cd $BENCHMARK_DIR
  wget http://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/RND3SAT/uf100-430.tar.gz
  tar -xzf *.tar.gz
  cd ../
fi

n=$(ls -1q $BENCHMARK_DIR | wc -l)

function benchmark {
  timeout=0
  timein=0
  total=0
  remaining=$n
  percent=0
  echo -ne "Instances solved [$timein] - Timed-out [$timeout] - Remaining [$remaining] ($percent%)         \r"
  for f in $BENCHMARK_DIR/*.cnf; do
    if output=$((/usr/bin/time --quiet -f "%U" python3 solver.py $1 $f > /dev/null) 2>&1); then
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
  average=$(printf "%.2f" $average)
  echo "Average time(s) [$average]"
  echo ""
}


echo "Benchmarking on $n instances..."

echo "Variable selection: DLIS"
benchmark "--choose-type=dlis"

echo "Variable selection: Jeroslow-Wang"
benchmark "--choose-type=jw"

