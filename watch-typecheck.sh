#!/usr/bin/env bash
ls *.py | entr -rcs 'bash typecheck.sh'
