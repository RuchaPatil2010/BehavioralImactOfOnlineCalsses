"""
Bayesian Belief Network
"""
import csv

LOC = ("/mnt/c/Users/patilru/Documents/MS/Spring_24/git/" +
       "BehavioralImactOfOnlineCalsses/data/Deidentified-Filtered Numeric "+
       "Data_Yes and No 3 Online Classes.csv")

def read_files():
  with open(LOC, 'r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    data = list(csv_reader)
  return header, data
