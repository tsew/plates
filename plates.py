#!/usr/bin/python
import enchant
import string
import sys

from joblib import Parallel, delayed
import multiprocessing

num_cores = multiprocessing.cpu_count()
chars = string.uppercase[:26]
chars_rnd = chars.replace("I", "")
chars_rnd = chars_rnd.replace("Q", "")
chars_pre = chars_rnd.replace("Z", "")

nums = "OIZSB"
no_s = "01258"
nums_used = [ "SI", "OZ", "SZ", "OA", "SA", "0S", "SS", "OT", "ST", "OB", "SB", "OG", "SG", "IO", "GO", "II", "IZ", "GZ", "IA", "GA", "IS", "GS", "IG", "GG", "IT", "GG" ]
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
output = "plates.txt"
plates = open (output, "w")


def process_plate(c1):
  for c2 in chars_pre:
    for c34 in nums_used:
      for c5 in chars_rnd:
        for c6 in chars_rnd:
          for c7 in chars_rnd:
            plate = c1 + c2 + c34 + c5 + c6 + c7
            if dict.check(plate):
              new_plate = convert_plate(plate)
              print plate + " becomes " + new_plate
              plates.write(new_plate)
              plates.write("\n")

Parallel(n_jobs=num_cores)(delayed(process_plate)(i) for i in chars_pre)

plates.close()

print "Sorting alphabetically"

original = open(output, "r")
lineList = original.readlines()
original.close()
out = open(output, "w")

for line in sorted(lineList):
  print(line.rstrip())
  out.write("\n")

out.close()

print "All Done"