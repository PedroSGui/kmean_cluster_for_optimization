import numpy as np
from sklearn.cluster import KMeans


class Clusterrer:
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
    def __init__(self, parameters, days_clustered, intervals_in_day, *args) -> None:
        self.args = args
        self.intervals_in_day = intervals_in_day 
        self.estrutura_a_clusterizar = flatten_json(parameters)
        self.days_clustered = days_clustered

        dist = 0
        dist_total = []
        fitter = []
        for key_estrutura in self.estrutura_a_clusterizar.keys():
            if key_estrutura in args:
                day_already_formed = 0
                # The code is examining the length of a specific component within the original data structure. By determining the number of elements or data points in this component, it infers the extent or duration of the temporal horizon. This information is crucial for subsequent steps in the clustering procedure.
                horizon_extended = len(self.estrutura_a_clusterizar[key_estrutura])
                # The code is calculating the number of days that make up the time horizon based on a simulation period of 1 hour. It takes into account the duration of the simulation and calculates the corresponding number of days. This information is used in subsequent computations or operations related to the clustering procedure.
                self.days = int(horizon_extended / self.intervals_in_day)
                periods_in_day = int(horizon_extended / self.days)
                for pos_elem_da_key_da_estrutura in range(
                    len(self.estrutura_a_clusterizar[key_estrutura])
                ):
                    dist = (
                        (
                            self.estrutura_a_clusterizar[key_estrutura][
                                pos_elem_da_key_da_estrutura
                            ]
                        )
                        + dist
                        - (
                            self.estrutura_a_clusterizar[key_estrutura][
                                pos_elem_da_key_da_estrutura - 1
                            ]
                        )
                    )

                    # The code is examining whether the current position represents the last position of a day. If it is indeed the last position of the day, the code increments the count of formed days. This check allows the code to keep track of the progress in forming complete days within the temporal data structure being processed.
                    if (
                        pos_elem_da_key_da_estrutura % periods_in_day
                    ) == periods_in_day - 1:
                        day_already_formed = day_already_formed + 1
                        if len(dist_total) < self.days:
                            # The code is responsible for creating the distance if it doesn't already exist. This step is necessary to initialize the distance calculation process. In the given example, the distance is created using the first vector, which specifically represents the electrical distance. This initialization ensures that the distance calculation starts from a valid reference point or initial value.
                            dist_total.append(dist)
                        else:
                            # The code is responsible for adding the distance of the current day to the existing distance. In this case, the thermal distance is being combined with the electrical distance. However, it is noted that there could be other types of distances involved in the calculation. The specific distances being added may vary depending on the context or requirements of the clustering procedure.
                            dist_total[day_already_formed - 1] = (
                                dist_total[day_already_formed - 1] + dist
                            )
                        dist = 0

        # The code snippet is describing a modification made to the data structure to ensure compatibility with the K-means clustering library being used. The specific data structure is being transformed or adapted to meet the format requirements of the library. This adjustment is crucial to successfully apply the K-means algorithm to the data and obtain the desired clustering results.
        for i in range(int(self.days)):
            fitter.append([dist_total[i], 0])

        self.kmeans_results = KMeans(
            n_clusters=days_clustered, random_state=0, n_init="auto"
        ).fit(fitter)
        # Another print statement is available in the code, which, when uncommented, displays the labels assigned by the K-means clustering algorithm to each day. This print statement illustrates that days with similar distances are grouped together within the clustering results. It allows you to observe the clustering outcome and the grouping of days based on their similarity in terms of the calculated distances.
        # print(dist_total) 
        # print(self.kmeans_results.labels_) 


    def dict(self):
        final_estrutura_a_clusterizar = {}
        synthetized_freq = []
        soma_d = {}
        for key_estrutura in self.estrutura_a_clusterizar.keys():
            soma_d[key_estrutura] = []
            if type(self.estrutura_a_clusterizar[key_estrutura]) == list:
                for i in range(self.days_clustered):
                    if len(synthetized_freq) < self.days_clustered:
                        # The code is responsible for storing the size or length of the vector that represents the cluster. It keeps track of the number of positions or elements that belong to a specific cluster. This information can be useful for further analysis or evaluation of the clustering results, as it provides an understanding of the composition and size of each cluster.
                        synthetized_freq.append(
                            len(np.where(self.kmeans_results.labels_ == i)[0])
                        )
                    for z in np.where(self.kmeans_results.labels_ == i)[0]:
                        # At this point in the code, the representative element of the cluster is being created. The chosen approach for creating the representative element is to compute the average of the various inputs within the cluster. By taking the average, the code generates a single representative value that captures the central tendency or typical behavior of the data points within the cluster. This representative element is used to summarize the characteristics of the cluster and aids in interpreting the results of the clustering process.
                        for period in range(self.intervals_in_day):
                            if i*self.intervals_in_day + period >= len(soma_d[key_estrutura]):
                                soma_d[key_estrutura].append(0)
                            
                            soma_d[key_estrutura][i*self.intervals_in_day + period] = (soma_d[key_estrutura][i*self.intervals_in_day + period]+ self.estrutura_a_clusterizar[key_estrutura][z * self.intervals_in_day + period]/ synthetized_freq[i]) 
        for key_estrutura in self.estrutura_a_clusterizar.keys():
            if key_estrutura in self.args:
                final_estrutura_a_clusterizar[f"{key_estrutura}"] = [
                    round(x, 4) for x in soma_d[key_estrutura]
                ]
            elif (
                type(self.estrutura_a_clusterizar[key_estrutura]) == list
                and key_estrutura not in self.args
            ):
                final_estrutura_a_clusterizar[key_estrutura] = [
                    round(x, 4) for x in soma_d[key_estrutura]
                ]
            else:
                final_estrutura_a_clusterizar[
                    key_estrutura
                ] = self.estrutura_a_clusterizar[key_estrutura]

        final_estrutura_a_clusterizar["cluster_freq"] = synthetized_freq
        return unflatten_json(final_estrutura_a_clusterizar)


def flatten_json(json):
    """
    Utility function to flatten a nested JSON dictionary structure.

    This function recursively iterates over the dictionary and flattens it by
    concatenating nested keys with a dot ('.') separator.

    Parameters:
        - json: The JSON dictionary to be flattened.

    Returns:
        The flattened JSON dictionary.

    Example:
    ```
    data = {
        'key1': {
            'nested1': 1,
            'nested2': 2
        },
        'key2': {
            'nested3': 3
        }
    }
    flattened_data = flatten_json(data)
    # Result: {
    #     'key1.nested1': 1,
    #     'key1.nested2': 2,
    #     'key2.nested3': 3
    # }
    ```
    """
    if type(json) == dict:
        for k, v in list(json.items()):
            if type(v) == dict:
                flatten_json(v)
                json.pop(k)
                for k2, v2 in v.items():
                    json[k + "." + k2] = v2
    return json

def unflatten_json(json):
    """
    Utility function to unflatten a flattened JSON dictionary structure.

    This function reverses the process of flattening by splitting the concatenated
    keys and reconstructing the original nested structure.

    Parameters:
        - json: The flattened JSON dictionary to be unflattened.

    Returns:
        The unflattened JSON dictionary.

    Example:
    ```
    flattened_data = {
        'key1.nested1': 1,
        'key1.nested2': 2,
        'key2.nested3': 3
    }
    unflattened_data = unflatten_json(flattened_data)
    # Result: {
    #     'key1': {
    #         'nested1': 1,
    #         'nested2': 2
    #     },
    #     'key2': {
    #         'nested3': 3
    #     }
    # }
    ```
    """
    if type(json) == dict:
        for k in sorted(json.keys(), reverse=True):
            if "." in k:
                key_parts = k.split(".")
                json1 = json
                for i in range(0, len(key_parts) - 1):
                    k1 = key_parts[i]
                    if k1 in json1:
                        json1 = json1[k1]
                        if type(json1) != dict:
                            conflicting_key = ".".join(key_parts[0 : i + 1])
                            raise Exception(
                                'Key "{}" conflicts with key "{}"'.format(
                                    k, conflicting_key
                                )
                            )
                    else:
                        json2 = dict()
                        json1[k1] = json2
                        json1 = json2
                if type(json1) == dict:
                    v = json.pop(k)
                    json1[key_parts[-1]] = v
    return json
