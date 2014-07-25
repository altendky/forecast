#!/bin/bash

clear

unoconv --server 127.0.0.1 --doctype spreadsheet --format csv --output budget.csv ../House/budget.ods
if [ $? == 0 ]
then
  ./cr.py
fi

