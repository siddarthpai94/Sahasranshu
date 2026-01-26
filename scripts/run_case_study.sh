#!/bin/bash
# Run a case study analysis

set -e

if [ -z "$1" ]; then
  echo "Usage: ./run_case_study.sh <case_study_name>"
  exit 1
fi

CASE_STUDY=$1
INPUT_DIR="examples/${CASE_STUDY}/inputs"
OUTPUT_DIR="results/${CASE_STUDY}"

mkdir -p "$OUTPUT_DIR"

echo "Running case study: $CASE_STUDY"
sahasranshu run --input "$INPUT_DIR" --output "$OUTPUT_DIR"

echo "Results saved to: $OUTPUT_DIR"
