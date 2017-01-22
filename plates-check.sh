#!/bin/bash
found_str="An Exact Match Has Been Found"
in_file="plates.txt"
out_file="plates-found.txt"
if [ -f "$out_file" ]; then
	rm -f $out_file
fi
while read -r line; do
  curl -s -S http://www.plates4less.co.uk/private-number-plates/${line}/ | tac | grep -q "${found_str}"
  if [ $? -eq 0 ]; then 
    echo -ne "\n${line} Found\n"
    echo $line >> $out_file
  else
    printf "."
  fi
    
done < $in_file
