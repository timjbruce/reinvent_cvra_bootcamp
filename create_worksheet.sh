#!/usr/bin/env bash

echo "reInvent CVRA Bootcamp Worksheet" > worksheet.txt
echo "Work directory: " `pwd` >> worksheet.txt
echo "OS: " `uname -a` >> worksheet.txt
echo "Git: " `git --version` >> worksheet.txt
echo "AWS CLI: " `aws --version` >> worksheet.txt
echo "Python: " `python -c "import sys;print(sys.version)"` >> worksheet.txt
echo "Virtualenv:" `virtualenv --version` >> worksheet.txt
echo "Node: " `node --version` >> worksheet.txt
echo "NPM: " `npm --version` >> worksheet.txt
echo "--- To be completed during the workshop ---" >> worksheet.txt
echo "AWS region: " >> worksheet.txt
echo "AWS Account ID and signin url: " >> worksheet.txt
echo "HERE Maps app_code: " >> worksheet.txt
echo "HERE Maps app_id: " >> worksheet.txt
echo "VehicleTripTable: " >> worksheet.txt
echo "Name of your CVRA Cloudformation stack: " >> worksheet.txt
echo "Name of your vehicle simulator Cloudformation stack: " >> worksheet.txt