#!/bin/bash
found_str="An Exact Match Has Been Found"
while read -r line; do
  curl -s -S http://www.plates4less.co.uk/private-number-plates/${line}/ | tac | grep -q "${found_str}"
  if [ $? -eq 0 ]; then 
    echo "${line} Found"
  else
    printf "."
  fi
    
done < plates.txt
