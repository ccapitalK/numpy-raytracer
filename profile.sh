#!/bin/bash

python -m cProfile -o profile.prof ./main.py
flameprof profile.prof -o profile.svg
