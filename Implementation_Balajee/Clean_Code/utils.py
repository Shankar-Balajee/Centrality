import numpy as np

def calculate_versatility(localCentrality, globalCentrality):
    versatility = localCentrality + globalCentrality
    print("Versatility:")
    print(versatility)
    return versatility


def print_csr_supra_adjacency_matrix(supraAdjacencyMatrix):
    print("Supra-adjacency matrix in CSR format:")
    print(supraAdjacencyMatrix)
