#!/bin/bash
# Check readiness for release

set -e

echo "Running release checks..."
echo "1. Linting..."
make lint

echo "2. Type checking..."
make type-check

echo "3. Testing..."
make test

echo "✓ All release checks passed!"
