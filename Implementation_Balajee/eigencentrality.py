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


eigenValues, lefteigenVectors,righteigenVectors = eig(adjacencyMatrix, left=True, right=True)

#Print the eigenvalues
print("Eigenvalues:")
print(eigenValues)
#Print the eigenvectors
print("Eigenvectors:")
print(lefteigenVectors)

print("right eigenvectors:")
print(righteigenVectors)


#Calculate the eigencentrality using the left eigenvector corresponding to the largest eigenvalue
maxEigenValue = max(eigenValues)
maxEigenValueIndex = numpy.where(eigenValues == maxEigenValue)
print("Max EigenvalueIndex:",maxEigenValueIndex)
eigencentrality = lefteigenVectors[:,maxEigenValueIndex]
print("Step 1:",eigencentrality)
eigencentrality = numpy.absolute(eigencentrality)
print("Step 2:",eigencentrality)
eigencentrality = eigencentrality / numpy.sum(eigencentrality)
print("Eigencentrality:")
print(eigencentrality)

