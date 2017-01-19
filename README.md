# Plates
A python script which finds UK car number plates that make words

## What is it

A simple python script that uses number representation of letters in UK numbers plates to make dictionary words.  The code works by iterating through every letter and number combination to make a legitimate 7 character number plate.  The plate is then checked in the dictionary and any that are valid are written to the `plates.txt` file.  The main python script is multi-threaded and will scale to the number of threads available on your host.  The `plates.txt` file is alphabetically sorted on completion towards the end of the python code.

There is a bash script that will check each line of the `plates.txt` file against a public website.  Don't expect there to be many valid combinations for purchase as many companies will have already reserved such interesting number plates.

The output of the script in the form of `plates.txt` is provided for reference.


