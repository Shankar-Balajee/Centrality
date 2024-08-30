import numpy 
import argparse
import math
from scipy.linalg import eig
import numpy as np
from scipy.sparse import csr_matrix,dok_matrix
from scipy.sparse import diags
import copy

debug = False



def input_adjacency_matrix(numVerticesEachLayer, numLayers):
    numVertices = numVerticesEachLayer * numLayers
    supraAdjacencyMatrix = numpy.zeros((numVertices, numVertices))

    for i in range(numLayers):
        adjacencyMatrix = numpy.zeros((numVerticesEachLayer, numVerticesEachLayer))
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

    supraAdjacencyMatrix =  csr_matrix((data, (row_indices, col_indices)), shape=(numVertices, numVertices))
    return supraAdjacencyMatrix




def add_across_layer_edges(supraAdjacencyMatrix, numVerticesEachLayer, numLayers):
    numEdges = int(input("Enter number of across-layer edges: "))
    for i in range(numEdges):
        edge = input().split()
        supraAdjacencyMatrix[(int(edge[0]) * numVerticesEachLayer) + int(edge[1])][(int(edge[2]) * numVerticesEachLayer) + int(edge[3])] = int(edge[4])


def add_across_layer_edges_csr(supraAdjacencyMatrix, numVerticesEachLayer, numLayers,intraLayerMatrix1):
    row_indices = []
    col_indices = []
    data = []

    numEdges = int(input("Enter number of across-layer edges: "))
    for i in range(numEdges):
        edge = input().split()
        row = (int(edge[0]) * numVerticesEachLayer) + int(edge[1])
        col = (int(edge[2]) * numVerticesEachLayer) + int(edge[3])
        weight = int(edge[4])
        row_indices.append(row)
        col_indices.append(col)
        data.append(weight)

    across_layer_matrix = csr_matrix((data, (row_indices, col_indices)), shape=supraAdjacencyMatrix.shape)
    if debug: print("Adding Across Layer Matrix",across_layer_matrix)
    supraAdjacencyMatrix += across_layer_matrix
    if debug: print("Modified SupraAdjacencyMatrix",supraAdjacencyMatrix)
    return supraAdjacencyMatrix




def compute_local_centrality(intraLayerMatrix, rho, epsilon, numVertices):
    localCentrality = numpy.ones((numVertices,1)) / numVertices
    print("Initial Local Centrality:")
    print(localCentrality)

    while True:
        newLocalCentrality = numpy.dot(intraLayerMatrix, localCentrality)
        newLocalCentrality = rho * newLocalCentrality + ((1 - rho) * numpy.ones((numVertices,1)) / numVertices)
        newLocalCentrality = newLocalCentrality / numpy.sum(newLocalCentrality)
        if numpy.linalg.norm(newLocalCentrality - localCentrality) < epsilon:
            localCentrality = newLocalCentrality
            break
        localCentrality = newLocalCentrality

    return localCentrality


def compute_local_centrality_csr(intraLayerMatrix, rho, epsilon, numVertices):
    localCentrality = np.ones((numVertices, 1)) / numVertices
    print("Initial Local Centrality:")
    print(localCentrality)

    while True:
        newLocalCentrality = intraLayerMatrix.dot(localCentrality)
        newLocalCentrality = rho * newLocalCentrality + ((1 - rho) * np.ones((numVertices, 1)) / numVertices)
        newLocalCentrality = newLocalCentrality / np.sum(newLocalCentrality)
        if np.linalg.norm(newLocalCentrality - localCentrality) < epsilon:
            localCentrality = newLocalCentrality
            break
        localCentrality = newLocalCentrality

    return localCentrality



def compute_global_centrality(supraAdjacencyMatrix, interLayerMatrix, localCentrality, rho, epsilon, numVertices):
    globalCentrality = numpy.ones((numVertices,1)) / numVertices
    print("Entering global centrality computation for the dense case")
    if debug: print("Local centrality being used for this case is ", localCentrality)
    print("Initial Global Centrality:")
    print(globalCentrality)
    if debug: print("Are the updates happening? ")
    iteration_counter = 0
    while True:
        iteration_counter += 1
        newGlobalCentrality = numpy.dot(supraAdjacencyMatrix, globalCentrality) + numpy.dot(interLayerMatrix, localCentrality)
        newGlobalCentrality = rho * newGlobalCentrality + ((1 - rho) * numpy.ones((numVertices,1)) / numVertices)
        newGlobalCentrality = newGlobalCentrality / numpy.sum(newGlobalCentrality)
        if debug: print("After the update number ", iteration_counter)
        if debug: print(newGlobalCentrality)
        if numpy.linalg.norm(newGlobalCentrality - globalCentrality) < epsilon:
            globalCentrality = newGlobalCentrality
            break
        globalCentrality = newGlobalCentrality

    return globalCentrality


def compute_global_centrality_csr(supraAdjacencyMatrix, interLayerMatrix, localCentrality, rho, epsilon, numVertices):
    if debug: print("Entering global centrality Computation for CSR case")
    if debug: print("Local Centrality being used for this is ", localCentrality)

    globalCentrality = np.ones((numVertices, 1)) / numVertices
    print("Initial Global Centrality:")
    print(globalCentrality)
    if debug: print("Are the updates happening? ")
    iteration_counter = 0
    while True:
        iteration_counter += 1
        newGlobalCentrality = supraAdjacencyMatrix.dot(globalCentrality) + interLayerMatrix.dot(localCentrality)
        newGlobalCentrality = rho * newGlobalCentrality + ((1 - rho) * np.ones((numVertices, 1)) / numVertices)
        newGlobalCentrality = newGlobalCentrality / np.sum(newGlobalCentrality)
        if debug:print("After the update number ", iteration_counter)
        if debug:print(newGlobalCentrality)
        if debug:print("-----------------------------")
        if np.linalg.norm(newGlobalCentrality - globalCentrality) < epsilon:
            globalCentrality = newGlobalCentrality
            break
        globalCentrality = newGlobalCentrality

    return globalCentrality


def calculate_versatility(localCentrality, globalCentrality):
    versatility = localCentrality + globalCentrality
    print("Versatility:")
    print(versatility)
    return versatility


def print_csr_supra_adjacency_matrix(supraAdjacencyMatrix):
    print("Supra-adjacency matrix in CSR format:")
    print(supraAdjacencyMatrix)




def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Compute centrality measures for a multilayer network.")
    parser.add_argument('--format', type=str, choices=['csr', 'dense'], default='dense', 
                        help="Specify the matrix format: 'csr' for sparse matrix in CSR format or 'dense' for normal dense matrix.")
    args = parser.parse_args()

    # Get user inputs for the network structure
    numVerticesEachLayer = int(input("Enter number of vertices in each layer: "))
    numLayers = int(input("Enter number of layers: "))
    
    # Based on the flag, use either dense or CSR format
    if args.format == 'csr':
        supraAdjacencyMatrix = input_adjacency_matrix_csr(numVerticesEachLayer, numLayers)
        intraLayerMatrix = supraAdjacencyMatrix.copy()
        supraAdjacencyMatrix=add_across_layer_edges_csr(supraAdjacencyMatrix, numVerticesEachLayer, numLayers,intraLayerMatrix)
    else:  # Use dense format
        supraAdjacencyMatrix = input_adjacency_matrix(numVerticesEachLayer, numLayers)
        intraLayerMatrix = supraAdjacencyMatrix.copy()
        add_across_layer_edges(supraAdjacencyMatrix, numVerticesEachLayer, numLayers)
    
    # Calculate the inter-layer matrix
    interLayerMatrix = supraAdjacencyMatrix - intraLayerMatrix
    print()
    if debug:
        if args.format=="csr":
            print("Intra Layer Matrix for the csr case", intraLayerMatrix)
        else :
            print("Intra Layer Matrix for the dense case ", intraLayerMatrix,"supra being ",supraAdjacencyMatrix)
    
    # Get user inputs for the centrality calculation parameters
    rho = float(input("Enter the value of rho: "))
    epsilon = float(input("Enter the value of epsilon: "))
    
    # Calculate local centrality based on the format
    if args.format == 'csr':
        localCentrality = compute_local_centrality_csr(intraLayerMatrix, rho, epsilon, numVerticesEachLayer * numLayers)
    else:
        localCentrality = compute_local_centrality(intraLayerMatrix, rho, epsilon, numVerticesEachLayer * numLayers)
    
    print("Final Local Centrality:")
    print(localCentrality)
    
    # Calculate global centrality based on the format
    if args.format == 'csr':
        globalCentrality = compute_global_centrality_csr(supraAdjacencyMatrix, interLayerMatrix, localCentrality, rho, epsilon, numVerticesEachLayer * numLayers)
    else:
        globalCentrality = compute_global_centrality(supraAdjacencyMatrix, interLayerMatrix, localCentrality, rho, epsilon, numVerticesEachLayer * numLayers)
    
    print("Final Global Centrality:")
    print(globalCentrality)
    
    # Calculate versatility
    versatility = calculate_versatility(localCentrality, globalCentrality)

    # _--------------------------------------# 
    if debug:
        if args.format == 'csr':
            print("Supra_Adjacenccy_inthecaseofcsr")
            print_csr_supra_adjacency_matrix(supraAdjacencyMatrix=supraAdjacencyMatrix)
            print("Intra Layer Matrix for the csr case\n", intraLayerMatrix)
        else : 
            print("Supra_Adjacenccy_inthecaseofdense")
            print("Supra-adjacency matrix:")
            print(supraAdjacencyMatrix)





if __name__ == "__main__":
    main()
