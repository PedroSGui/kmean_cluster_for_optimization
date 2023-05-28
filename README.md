# kmean_cluster_for_optimization

Acording to (Xu and Wunsch 2005), “Every day, people encounter a large amount of information and store or represent it as data, for further analysis and management. One of the vital means in dealing with these data is to classify or group them into a set of categories or clusters”. The objective of clustering is, then, to reduce the data, without losing its meaning considerably.

The clustering of the data must result in data that correspond to the initial system with a rigor less than or equal to the original data, and must also have a transfer function that defines the way in which the grouping of elements was carried out.

Several clustering algorithms were analyzed in the context of this work, where the main features that are useful in deciding which algorithm is interesting to use, is how to measure the proximity between elements, and how to choose the number of clusters.

Principal contribuição:

"""
    Class for performing the distance-based k-means clustering procedure.

    This class is designed to be instantiated and called from a main program.
    The main program should provide the necessary parameters and data structure
    for clustering.

    Parameters:
        - parameters: The data structure to be clustered.
        - days_clustered: The number of output days required. It should be greater than 0
          and smaller than the size of the original data structure.
        - intervals_in_day: The number of intervals in a day. It helps the function
          understand the structure of the data.
        - *args: Any number of additional string arguments that need to be present
          in the original data structure.

    Usage:
    ```
    # Create an instance of Clusterrer
    clusterer = Clusterrer(parameters, days_clustered, intervals_in_day, *args)

    # Access the clustered data
    clustered_data = clusterer.dict()
    ```

    The `__init__` method initializes the clustering procedure. It takes the provided
    parameters and performs the following steps:

    1. Flatten the original data structure using the `flatten_json` function.
    2. Calculate the distance between consecutive elements in the data structure and
       aggregate the distances by day.
    3. Convert the aggregated distances into a suitable format for the KMeans algorithm.
    4. Apply the KMeans algorithm to cluster the distances into `days_clustered` clusters.

    The `dict` method returns the clustered data in a structured format. It performs the
    following steps:

    1. Initialize variables and data structures.
    2. Iterate over the keys of the original data structure.
    3. For each key, calculate the representative element for each cluster by averaging
       the corresponding elements from the original data structure.
    4. Store the representative elements in a new data structure.
    5. Return the final clustered data structure.

    The `flatten_json` function is used to flatten the original data structure to fit the
    expected input format of the clustering algorithm.

    The `unflatten_json` function is the reverse process of restoring the original
    structure from the clustered data.
    """

