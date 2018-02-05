#!/usr/bin/python
import enchant
import glob
import os
import string
import sys
import uuid

from joblib import Parallel, delayed
import multiprocessing

num_cores = multiprocessing.cpu_count()
chars = string.uppercase[:26]
chars_rnd = chars.replace("I", "")
chars_rnd = chars_rnd.replace("Q", "")
chars_pre = chars_rnd.replace("Z", "")

nums = "OIZSB"
no_s = "01258"
nums_used = [ "SI", "OZ", "SZ", "OA", "SA", "0S", "SS", "OT", "ST", "OB", "SB", "OG", "SG", "IO", "GO", "II", "IZ", "GZ", "IA", "GA", "IS", "GS", "IG", "GG", "IT", "GT" ]
nums_conv = [ "51", "02", "52", "04", "54", "05", "55", "07", "57", "08", "58", "06", "56", "10", "60", "11", "12", "62", "14", "64", "15", "65", "16", "66", "17", "67" ]

def convert_plate(plate):
  for idx, used in enumerate(nums_used):
    real_plate = plate[:2] + plate[2:4].replace(used, nums_conv[idx]) + plate[4:]
    if real_plate != plate:
      break
  return real_plate

print "Welcome to plate finder (running with " + str(num_cores) + " cores)"

dict = enchant.Dict("en_GB")
count = 0
found = 0
output = "plates"
ext = ".txt"

def process_plate(c1):
  out = open(output + "-" + str(uuid.uuid4()) + ext, "w")
  for c2 in chars_pre:
    for c34 in nums_used:
      for c5 in chars_rnd:
        for c6 in chars_rnd:
          for c7 in chars_rnd:
            plate = c1 + c2 + c34 + c5 + c6 + c7
            if dict.check(plate):
              new_plate = convert_plate(plate)
              print plate + " becomes " + new_plate
              new_plate+="\n"
              out.write(new_plate)
  out.close()

def process_short(c1):
  out = open(output + "-" + str(uuid.uuid4()) + ext, "w")
  for c2 in chars_pre:
    for c34 in nums_used:
      for c5 in chars_rnd:
        for c6 in chars_rnd:
          for c7 in chars_rnd:
            plate1 = c1 + c2 + c34
            plate2 = c5 + c6 + c7
            if dict.check(plate1) and dict.check(plate2):
              new_plate = convert_plate(plate1)
              print plate1 + " " + plate2  + " becomes " + new_plate + " " + plate2
              out.write(new_plate + plate2 + "\n")
  out.close()

content = Parallel(n_jobs=num_cores)(delayed(process_plate)(i) for i in chars_pre)
content = Parallel(n_jobs=num_cores)(delayed(process_short)(i) for i in chars_pre)

filenames = glob.glob(output + "-*" + ext)
print filenames
with open(output + ext, 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

for file in filenames:
  os.remove(file)

print "Sorting alphabetically"
original = open(output + ext, "r")
lineList = original.readlines()
original.close()
out = open(output + ext, "w")

for line in sorted(lineList):
  print line
  out.write(line.rstrip())
  out.write("\n")

out.close()

print "All Done"
