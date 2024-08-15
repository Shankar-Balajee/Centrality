import math 
import numpy
from scipy.linalg import eig


numVertices = int(input())
adjacencyMatrix = numpy.zeros((numVertices, numVertices))
numEdges = int(input())
for i in range(numEdges):
    edge = input().split()
    adjacencyMatrix[int(edge[0])][int(edge[1])] = int(edge[2])

#Print the adjacency matrix
print("Adjacency Matrix:")
for i in range(numVertices):
    print(adjacencyMatrix[i])

#Page Rank Centrality, using the power iteration method

rho = float(input("Enter the value of rho: "))
epsilon = float(input("Enter the value of epsilon: "))

#Initialize the Page Rank Centrality vector
pageRankCentrality = numpy.ones((numVertices,1)) / numVertices
print("Initial Page Rank Centrality:")
print(pageRankCentrality)

#Calculate the Page Rank Centrality
num_iterations = 0
while True:
    newPageRankCentrality = numpy.dot(adjacencyMatrix, pageRankCentrality)
    newPageRankCentrality = rho * newPageRankCentrality + ((1 - rho) * numpy.ones((numVertices,1)) / numVertices)
    print("Iteration:",num_iterations)
    print("Current Page Rank Centrality:")
    #normalise newpageRankCentrality
    newPageRankCentrality = newPageRankCentrality / numpy.sum(newPageRankCentrality)
    print(newPageRankCentrality)
    num_iterations += 1
    if numpy.linalg.norm(newPageRankCentrality - pageRankCentrality) < epsilon:
        pageRankCentrality = newPageRankCentrality
        break
    pageRankCentrality = newPageRankCentrality

print("Page Rank Centrality:")
print(pageRankCentrality)
print("Number of iterations:",num_iterations)