import numpy as np
from scipy.sparse import csr_matrix

def input_adjacency_matrix(numVerticesEachLayer, numLayers):
    numVertices = numVerticesEachLayer * numLayers
    supraAdjacencyMatrix = np.zeros((numVertices, numVertices))

    for i in range(numLayers):
        adjacencyMatrix = np.zeros((numVerticesEachLayer, numVerticesEachLayer))
        numEdges = int(input(f"Enter number of edges for layer {i}: "))
        for j in range(numEdges):
            edge = input().split()
            adjacencyMatrix[int(edge[0])][int(edge[1])] = int(edge[2])
        print(f"Adjacency Matrix for Layer {i}:")
        print(adjacencyMatrix)
        for j in range(numVerticesEachLayer):
            for k in range(numVerticesEachLayer):
                supraAdjacencyMatrix[(i * numVerticesEachLayer) + j][(i * numVerticesEachLayer) + k] = adjacencyMatrix[j][k]

    return supraAdjacencyMatrix


def input_adjacency_matrix_csr(numVerticesEachLayer, numLayers):
    numVertices = numVerticesEachLayer * numLayers

    row_indices = []
    col_indices = []
    data = []

    for i in range(numLayers):
        numEdges = int(input(f"Enter number of edges for layer {i}: "))
        for j in range(numEdges):
            edge = input().split()
            row = (i * numVerticesEachLayer) + int(edge[0])
            col = (i * numVerticesEachLayer) + int(edge[1])
            weight = int(edge[2])
            row_indices.append(row)
            col_indices.append(col)
            data.append(weight)

    supraAdjacencyMatrix = csr_matrix((data, (row_indices, col_indices)), shape=(numVertices, numVertices))
    return supraAdjacencyMatrix
