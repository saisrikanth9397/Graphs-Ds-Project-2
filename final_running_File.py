import networkx as nx
import pandas as pd
import os
import numpy as np
import time
import glob

startTime = time.time()
data = '/home/scratch1/cs5413/ethereum/transactions/'


print('Reading files')
allData = pd.DataFrame()
for file in os.listdir(data):
    with open(os.path.join(data, file)) as f:
      print('Reading file: ',file)
      graph = pd.read_csv(f, usecols= ['from_addr','to_addr','tx_hash','gas_price'])
      allData = allData.append(graph)
print('Read all 32 files')
allData = allData.reset_index()



allData['from_node_id'] = (allData['from_addr']).astype('category').cat.codes
allData['to_node_id'] = (allData['to_addr']).astype('category').cat.codes

print('-----------------------Output for question 1----------------please wait -----------')
#Question1
allData = allData.rename(columns={'from_addr': 'source', 'to_addr': 'target'})
DG = nx.from_pandas_edgelist(allData, edge_attr=True ,create_using=nx.DiGraph())
dfsDG = nx.dfs_tree(DG)
print("dfsDG formed with len:: " + str(len(list(dfsDG))))
topoDG = nx.topological_sort(dfsDG)
print("topoDG formed with len: " + str(len(list(topoDG))))
longDFSpath = nx.dag_longest_path(dfsDG)
print("longDFSpath formed with length: " + str(len(longDFSpath)))
longDG = nx.DiGraph(nx.dfs_edges(dfsDG, source=longDFSpath[0]))
print("longDG formed ")
print(longDG)
firstOp = []

for i in list(longDG.edges()):
  row = (i[0], DG[i[0]][i[1]]['from_node_id'], i[1], DG[i[0]][i[1]]['to_node_id'], DG[i[0]][i[1]]['tx_hash'], DG[i[0]][i[1]]['gas_price'])
  firstOp.append(row)

longestDFSPath = pd.DataFrame(firstOp, columns = ['from_addr','from_node_id', 'to_addr', 'to_node_id', 'tx_hash','gas_price'])
print("longestDFSPath")
print(longestDFSPath)
endTime = time.time()
print("Time taken for question 1: " + str(endTime - startTime))

print('-----------------------Question 1 ----------------Completed -----------')


print('-----------------------Output for question 3----------------please wait -----------')
#Question 3
startTime = time.time()
allNodes = list(DG.nodes)
print("list of nodes " + str(len(allNodes)))
length, path = nx.single_source_dijkstra(DG, allNodes[0])
allPathList = []
for i in path:
  allPathList.append('Path to Node '+str(i)+'is: '+ str(path[i]))
print('\n\n printing only first 100 shortest path from sorce ',allNodes[0], ' to other nodes in the graph\n\n')
for i in allPathList[:100]:
  print(i,'\n\n')
endTime = time.time()

print("Time taken for question 3: ", str(endTime - startTime))

print('-----------------------Question 3 ----------------Completed -----------')

print('-----------------------Output for question 2----------------please wait -----------')

#Question 2
#getting all strongly connected components from DFS tree


dict_files = {}
ind = 0
for file in glob.glob(data + "*"):
    ind = ind + 1
    dict_files[str(ind)] = file
for key, value in dict_files.items():
    print(key,':',value)
file_number = input("\nEnter one number between 1-32 to choose between files:")

all_Data = pd.read_csv(dict_files[file_number], usecols= ['from_addr','to_addr','tx_hash','gas_price'])
all_Data = all_Data.reset_index()

all_Data = all_Data.rename(columns={'from_addr': 'source', 'to_addr': 'target'})
DG_2 = nx.from_pandas_edgelist(all_Data, edge_attr=True ,create_using=nx.DiGraph())

print("starting question 2 execution \n Please wait for a few minutes")
startTime = time.time()
for component in nx.strongly_connected_components(DG_2):
  if len(component) > 10:
    print('No. of elements in component: ', len(component),'Elements in component: ',component,'\n\n')

#converting to directed graph to directed graph
G = DG_2.to_undirected()
T=nx.minimum_spanning_tree(G)
TDF = pd.DataFrame(list(T),columns=['Nodes'])
print('Minimum Spanning Tree Path Order in DataFrame:')
print(TDF)
endTime = time.time()
print("Timetaken for question 2: " + str(endTime - startTime))

print('-----------------------Question 2 ----------------Completed -----------')

print('-----------------------Program Executed Succesfully -----------------------')
