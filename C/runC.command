#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "Compiling..."
clang main.c
echo "Compiled!"
echo "Program running below..."
echo "=================================================="
echo ""
./a.out
echo ""
echo ""
echo "=================================================="
echo "Program finished!"

