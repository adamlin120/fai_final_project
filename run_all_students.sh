#!/bin/bash

# Function to run the test for a single student
run_test() {
    student_id=$1
    echo "Running test for student: $student_id"
    python test.py "$student_id"
}

export -f run_test

# Read student directories from student_src_info.csv and run tests in parallel
tail -n +2 student_src_info.csv | cut -d, -f1 | parallel -j 32 run_test