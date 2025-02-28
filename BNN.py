"""
Bayesian Belief Network
"""

from itertools import product
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianNetwork
import utils

def get_data():
  """
  Using the supporting functions get the filtered data from the csv file in form
  of DataFrame.

  Returns:
    DataFrame containing filtered data.
  """
  header, data = utils.read_files()
  factors = utils.get_factors()
  columns = utils.get_col_nums(header, factors)
  df = utils.get_dataframe(data, factors, columns)

  return df

def generate_bayesian_model():
  """
  Returns:
    Bayesian Network Model defined in the paper.
  """
  return BayesianNetwork(utils.generate_network())

def get_probabilities(data, graph):
  """
  Generate the probabilities for the BBN

  Returns:
    List of all the CPDs in the BBN.
  """
  parent = set()
  child = set()
  cpds = []

  # Get set of all the parents and children of any given edge.
  for (p,c) in graph:
    parent.add(p)
    child.add(c)
  
  # Roots are the nodes without any parent, in other words they would not be 
  # child of any other node.
  roots = parent - child

  # For Level 0
  # Probabilities are defined as the P(x=k) = number of rows having value k 
  # divided by the total number of rows for each of the node in the roots.
  for label in roots:
    col = data[label]
    values = []
    for i in range(1, 6):
      values.append([len([v for v in col if v==i])/len(col)])
    cpds.append(TabularCPD(variable      = label, 
                           variable_card = 5, 
                           values        = values))

  # For other nodes which have parents:
  # Probabilities are defined as conditional probabilities P(x=k|y=l) = number 
  # of rows where value of x is k and y is l divided by total number of rows 
  # having value of y as l.
  for nodes in child:
    # pre_nodes are set of all the nodes which point to the current node.
    pre_nodes = set()
    for i,j in graph:
      if j == nodes:
        pre_nodes.add(i)
    
    # Store the count of all the rows where the value of current node is given 
    # and the pre_nodes form a specific tuple.
    count = {1:{},2:{},3:{},4:{},5:{}}
    # total stores the number of nodes containing the given tuple for pre_nodes.
    total = {}
    # For each row in the data, update the count and total nodes.
    for i in range(len(data)):
      now = data.iloc[i]

      # Store the data of all the prenodes in a tuple.
      val = tuple([int(now[v]) for v in pre_nodes])
      # Update the count of tuple.
      if val in count[now[nodes]].keys():
        count[now[nodes]][val]+=1
      else:
        count[now[nodes]][val] = 1

      # Update the value of row in the "total"
      if val in total.keys():
        total[val]+=1
      else:
        total[val] = 1

    # Calculate the values to add in the cpd.
    values = []
    # For each value for the current node.
    for val in range(1,6):
      now = []
      # For all the possible combinations of the value in all the pre_nodes
      for comb in product(range(1,6), repeat=len(pre_nodes)):
        if comb in count[val]:
          now.append(count[val][comb]/total[comb])
        elif comb in total:
          now.append(0)
        else:
          # If the given combination does not exist in the database, set a 
          # uniform value in the cpd so that it passes the check_model check. 
          now.append(1/5)
      values.append(now)
      
    cpds.append(TabularCPD(variable = nodes, variable_card = 5,
                           values = values,
                           evidence = list(pre_nodes), 
                           evidence_card = [5 for i in range(len(pre_nodes))]))

  return cpds

def main():
  data = get_data()
  graph = utils.generate_network()

  # Define the BBN model and its probabilities.
  model = generate_bayesian_model()
  cpds = get_probabilities(data, graph)
  for c in cpds:
    model.add_cpds(c)

  # Check the model
  print(model.check_model())

if __name__ == "__main__":
  main()