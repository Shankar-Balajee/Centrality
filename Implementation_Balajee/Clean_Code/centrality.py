import numpy as np

def compute_local_centrality(intraLayerMatrix, rho, epsilon, numVertices):
    localCentrality = np.ones((numVertices, 1)) / numVertices
    print("Initial Local Centrality:")
    print(localCentrality)

    while True:
        newLocalCentrality = np.dot(intraLayerMatrix, localCentrality)
        newLocalCentrality = rho * newLocalCentrality + ((1 - rho) * np.ones((numVertices, 1)) / numVertices)
        newLocalCentrality = newLocalCentrality / np.sum(newLocalCentrality)
        if np.linalg.norm(newLocalCentrality - localCentrality) < epsilon:
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
    globalCentrality = np.ones((numVertices, 1)) / numVertices
    print("Entering global centrality computation for the dense case")
    print("Initial Global Centrality:")
    print(globalCentrality)

    iteration_counter = 0
    while True:
        iteration_counter += 1
        newGlobalCentrality = np.dot(supraAdjacencyMatrix, globalCentrality) + np.dot(interLayerMatrix, localCentrality)
        newGlobalCentrality = rho * newGlobalCentrality + ((1 - rho) * np.ones((numVertices, 1)) / numVertices)
        newGlobalCentrality = newGlobalCentrality / np.sum(newGlobalCentrality)
        if np.linalg.norm(newGlobalCentrality - globalCentrality) < epsilon:
            globalCentrality = newGlobalCentrality
            break
        globalCentrality = newGlobalCentrality

    return globalCentrality


def compute_global_centrality_csr(supraAdjacencyMatrix, interLayerMatrix, localCentrality, rho, epsilon, numVertices):
    globalCentrality = np.ones((numVertices, 1)) / numVertices
    print("Initial Global Centrality:")
    print(globalCentrality)

    iteration_counter = 0
    while True:
        iteration_counter += 1
        newGlobalCentrality = supraAdjacencyMatrix.dot(globalCentrality) + interLayerMatrix.dot(localCentrality)
        newGlobalCentrality = rho * newGlobalCentrality + ((1 - rho) * np.ones((numVertices, 1)) / numVertices)
        newGlobalCentrality = newGlobalCentrality / np.sum(newGlobalCentrality)
        if np.linalg.norm(newGlobalCentrality - globalCentrality) < epsilon:
            globalCentrality = newGlobalCentrality
            break
        globalCentrality = newGlobalCentrality

    return globalCentrality
