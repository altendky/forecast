#!/bin/bash

clear

unoconv --server 127.0.0.1 --doctype spreadsheet --format csv budget.ods
if [ $? == 0 ]
then
  ./cr.py
fi

