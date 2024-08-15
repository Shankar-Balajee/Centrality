import numpy 
import math
from scipy.linalg import eig

numVerticesEachLayer = int(input())
numLayers = int(input())
numVertices = numVerticesEachLayer * numLayers

supraAdjacencyMatrix = numpy.zeros((numVertices, numVertices))

for i in range(numLayers):
    adjacencyMatrix = numpy.zeros((numVerticesEachLayer, numVerticesEachLayer))
    numEdges = int(input())
    for j in range(numEdges):
        edge = input().split()
        adjacencyMatrix[int(edge[0])][int(edge[1])] = int(edge[2])
    print("Adjacency Matrix for Layer",i)
    print(adjacencyMatrix)
    for j in range(numVerticesEachLayer):
        for k in range(numVerticesEachLayer):
            supraAdjacencyMatrix[(i * numVerticesEachLayer) + j][(i * numVerticesEachLayer) + k] = adjacencyMatrix[j][k]

intraLayerMatrix = supraAdjacencyMatrix.copy()
    
#Across layer edges
numEdges = int(input())
for i in range(numEdges):
    #Each edge is given as layer_number_1 vertex_number_1 layer_number_2 vertex_number_2 weight 
    edge = input().split()
    supraAdjacencyMatrix[(int(edge[0]) * numVerticesEachLayer) + int(edge[1])][(int(edge[2]) * numVerticesEachLayer) + int(edge[3])] = int(edge[4])

#Decomposition of the supra adjacency matrix

#We need a diagonal matrix with only the inter layer edges
interLayerMatrix =  supraAdjacencyMatrix - intraLayerMatrix

#Local centrality measure 
rho = float(input("Enter the value of rho: "))
epsilon = float(input("Enter the value of epsilon: "))

#Initialize the local centrality vector
localCentrality = numpy.ones((numVertices,1)) / numVertices
print("Initial Local Centrality:")
print(localCentrality)

while True:
    newLocalCentrality = numpy.dot(intraLayerMatrix, localCentrality)
    newLocalCentrality = rho * newLocalCentrality + ((1 - rho) * numpy.ones((numVertices,1)) / numVertices)
    print("Current Local Centrality:")
    #normalise newLocalCentrality
    newLocalCentrality = newLocalCentrality / numpy.sum(newLocalCentrality)
    print(newLocalCentrality)
    if numpy.linalg.norm(newLocalCentrality - localCentrality) < epsilon:
        localCentrality = newLocalCentrality
        break
    localCentrality = newLocalCentrality

print("Local Centrality:")
print(localCentrality)