"""
Supporting functions for BBN (Bayesian Belief Network).
"""

import csv
import pandas as pd


LOC = ("./data/Deidentified-Filtered Numeric "+
       "Data_Yes and No 3 Online Classes.csv")
FACTORS_LOC = "./factor.txt"

def read_files():
  """
  Read the csv files mentioned and divide it into header and data where header 
  contains the first two rows (row 1 contains the notations used for questions 
  and row 2 contains the questions asked in the survey) and rest of the data 
  contains the values.

  Returns:
    tuple of header and data
  """
  with open(LOC, 'r') as file:
    csv_reader = csv.reader(file)
    header = [next(csv_reader)]
    header.append(next(csv_reader))
    data = list(csv_reader)

  return header, data

def get_factors():
  """
  Factors are the factors we use to determine the Perceived Usefulness and the 
  Perceived Ease of Use which finally determines the Actual Use. These factors 
  are stored in "factor.txt".

  Returns:
    List of strings denoting the factors.
  """
  factors = []
  with open(FACTORS_LOC, 'r') as file:
    for line in file:
      factors.append(line.split('\n')[0])

  return factors

def get_col_nums(header, factors):
  """
  Based on each factors, get the columns which contains the data wrt each of the 
  factors.

  Returns:
    List where each element of the list denotes all the columns which contains 
    data for the respective factor.
  """
  cols = []
  for f in factors:
    cols.append([i for (i, val) in enumerate(header[0]) if (f+' ') in val])

  return cols

def get_dataframe(data, factors, cols):
  """
  Filter the data to return a table which contains the factors as column headers
  and average of each of the factor as row value for each of the respective 
  value in the original data.

  Args:
    data    : csv file data
    factors : list of all the factors
    cols    : list of column numbers of each factor

  Returns: 
    DataFrame containing the filtered data.
  """
  d = {}
  for (f,c) in zip(factors, cols):
    d[f] = []
    for row in data:
      d[f].append(round(sum([int(row[i]) for i in c])/len(c)))

  return pd.DataFrame(d)

def generate_network():
  """
  Generate the network as mentioned in the research paper. This network is used 
  to create the Bayesian Network Model.

  Returns:
    List of all the edges in the network.
  """
  factors = get_factors()
  graph = []

  # Bipartite graph for all the factors in level 0
  for i in range(4, 11):
    for j in [2, 3]:
      graph.append((factors[i], factors[j]))

  # Graph logic for all the other factors
  graph.append((factors[1], factors[0]))
  graph.append((factors[2], factors[1]))
  graph.append((factors[3], factors[1]))
  graph.append((factors[3], factors[2]))

  return graph
