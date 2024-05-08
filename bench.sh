#!/usr/bin/bash

declare TESTDIR
declare -i CCOUNT

TESTDIR="${PWD}/runs/$(date +%s)"
mkdir -p "$TESTDIR"

cd "$TESTDIR" || exit 1

python -m python_benchmarking.cases >cases.csv

CCOUNT=$(($(wc -l cases.csv | cut -d " " -f 1) - 1))

echo "Running $CCOUNT test cases"

algorithms=(pure_python with_numpy with_njit)

for alg in "${algorithms[@]}"; do
	hyperfine --warmup 1 \
		--export-csv "$alg.hyp.csv" \
		-P C 0 $((CCOUNT - 1)) \
		"python -m python_benchmarking.$alg {C}"

	paste -d "," "cases.csv" "$alg.hyp.csv" >"$alg.full.csv"
done

python -m python_benchmarking.plot
