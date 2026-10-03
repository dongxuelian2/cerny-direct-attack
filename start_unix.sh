#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
python3 --version
python3 run.py demo
python3 run.py compare --n 8
python3 -m unittest discover -s tests -v
printf '\nSUCCESS. Open results/ and START_HERE.md.\n'
