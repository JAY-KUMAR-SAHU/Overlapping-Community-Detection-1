from sklearn import metrics
import community
from sklearn.metrics.cluster import normalized_mutual_info_score

#tested
def modularity(G, communities):
    m = G.number_of_edges()
    Q = 0
    for c in communities:
        for i in c:
            for j in c:
                if i != j:
                    Aij = 1 if G.has_edge(i,j) else 0
                    ki = G.degree(i)
                    kj = G.degree(j)
                    Q += (Aij - ki*kj/(2*m))
    return Q/(2*m)


# tested
def conductance(G, communities):
   
    cut_size = 0
    volume = 0

    for community in communities:
        for node_i in community:
            if node_i not in G:
                continue
            neighbors = set(G.neighbors(node_i))
            cut_size += len(neighbors.difference(community))
            volume += len(neighbors)

    if volume == 0:
        return 0

    conductance = cut_size / volume
    normalized_conductance = -1 * (conductance - 1)
    return normalized_conductance



#tested
def calculate_coverage(graph, communities):
   
    # Calculate the number of edges in the graph
    num_edges = graph.number_of_edges()

    # Calculate the number of edges within the communities
    intra_community_edges = 0
    for community in communities:
        intra_community_edges += graph.subgraph(community).number_of_edges()

    # Calculate the coverage
    coverage = intra_community_edges / num_edges if num_edges > 0 else 0

    # Normalize the coverage to be between 0 and 1
    coverage = max(0, min(1, coverage))

    return coverage


#tested
def cut_ratio(graph, communities):
    # Create a dictionary mapping nodes to their community IDs
    community_dict = {}
    for i, community in enumerate(communities):
        for node in community:
            community_dict[node] = i
    
    # Calculate the total number of edges and the number of cut edges
    total_edges = graph.number_of_edges()
    cut_edges = 0
    for edge in graph.edges():
        if edge[0] in community_dict and edge[1] in community_dict:
            if community_dict[edge[0]] != community_dict[edge[1]]:
                cut_edges += 1
    
    # Calculate and return the cut ratio
    return cut_edges / total_edges


#tested
def calculate_ari(graph, communities):
   
    # create a dictionary to map nodes to their corresponding community labels
    node2comm = {}
    for i, comm in enumerate(communities):
        for node in comm:
            node2comm[node] = i
    # generate the label lists
    ground_truth = community.best_partition(graph)
    predicted_labels = []
    true_labels = []
    i = 0
    for node in node2comm:
        j = i
        for node in node2comm:
            if(i==node):
                predicted_labels.append(node2comm.get(node))
                i += 1
        if(j==i):
            i += 1
    i = 0
    for node in ground_truth:
        j = i
        for node in ground_truth:
            if(i==node):
                true_labels.append(ground_truth.get(node))
                i += 1
        if(j==i):
            i += 1
    # calculate the Adjusted Rand Index (ARI) score
    ari_score = metrics.adjusted_rand_score(true_labels, predicted_labels)

    return ari_score


#tested
def calculate_nmi(graph, communities):
    
    # create a dictionary to map nodes to their corresponding community labels
    node2comm = {}
    for i, comm in enumerate(communities):
        for node in comm:
            node2comm[node] = i
    # generate the label lists
    ground_truth = community.best_partition(graph)
    predicted_labels = []
    true_labels = []
    i = 0
    for node in node2comm:
        j = i
        for node in node2comm:
            if(i==node):
                predicted_labels.append(node2comm.get(node))
                i += 1
        if(j==i):
            i += 1
    i = 0
    for node in ground_truth:
        j = i
        for node in ground_truth:
            if(i==node):
                true_labels.append(ground_truth.get(node))
                i += 1
        if(j==i):
            i += 1
    # calculate the Adjusted Rand Index (ARI) score
    nmi_score = metrics.normalized_mutual_info_score(true_labels, predicted_labels)

    return nmi_score
