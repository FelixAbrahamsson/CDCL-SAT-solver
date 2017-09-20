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

python3.6 solver.py benchmark-instances/uf100-01.cnf

