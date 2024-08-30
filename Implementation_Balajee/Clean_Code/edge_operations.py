from scipy.sparse import csr_matrix

def add_across_layer_edges(supraAdjacencyMatrix, numVerticesEachLayer, numLayers):
    numEdges = int(input("Enter number of across-layer edges: "))
    for i in range(numEdges):
        edge = input().split()
        supraAdjacencyMatrix[(int(edge[0]) * numVerticesEachLayer) + int(edge[1])][(int(edge[2]) * numVerticesEachLayer) + int(edge[3])] = int(edge[4])


def add_across_layer_edges_csr(supraAdjacencyMatrix, numVerticesEachLayer, numLayers, intraLayerMatrix1):
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
    supraAdjacencyMatrix += across_layer_matrix
    return supraAdjacencyMatrix
