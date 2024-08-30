import argparse
from input_matrix import input_adjacency_matrix, input_adjacency_matrix_csr
from edge_operations import add_across_layer_edges, add_across_layer_edges_csr
from centrality import compute_local_centrality, compute_local_centrality_csr
from centrality import compute_global_centrality, compute_global_centrality_csr
from utils import calculate_versatility, print_csr_supra_adjacency_matrix

debug = False

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
        supraAdjacencyMatrix = add_across_layer_edges_csr(supraAdjacencyMatrix, numVerticesEachLayer, numLayers, intraLayerMatrix)
    else:  # Use dense format
        supraAdjacencyMatrix = input_adjacency_matrix(numVerticesEachLayer, numLayers)
        intraLayerMatrix = supraAdjacencyMatrix.copy()
        add_across_layer_edges(supraAdjacencyMatrix, numVerticesEachLayer, numLayers)
    
    # Calculate the inter-layer matrix
    interLayerMatrix = supraAdjacencyMatrix - intraLayerMatrix
    
    if debug:
        if args.format == "csr":
            print("Intra Layer Matrix for the csr case", intraLayerMatrix)
        else:
            print("Intra Layer Matrix for the dense case", intraLayerMatrix, "supra being", supraAdjacencyMatrix)
    
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

    if debug:
        if args.format == 'csr':
            print("Supra_Adjacency in the case of CSR:")
            print_csr_supra_adjacency_matrix(supraAdjacencyMatrix=supraAdjacencyMatrix)
            print("Intra Layer Matrix for the CSR case\n", intraLayerMatrix)
        else:
            print("Supra_Adjacency in the case of dense:")
            print("Supra-adjacency matrix:")
            print(supraAdjacencyMatrix)


if __name__ == "__main__":
    main()
