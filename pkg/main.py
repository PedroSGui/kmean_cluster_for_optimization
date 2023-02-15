"""
Example procedure for computing the clustering of time-series data.
"""
import json
from cluster import Clusterrer
from pprint import pprint


def optimization(parameters: dict, n_clusters: int) -> None:
    """
    Test function for performing the distance based kmean clustering procedure.
    """
    print("\nInitial parameters:\n")
    pprint(parameters, indent=2, compact=True, width=100)
    print("")
    
    
    """
    parameters: É necessàrio passar a estrutura que deseja clusterizar
    n_cluster: Numero de dias que quer de output, precisa ser maior do que 0 e menor do que o tamanho da estrutura original
    intervals_in day: O numero de intervalos no dia é importante para a função entender a estrutura que esta a tratar
    *args: quantas string quiser, precisa estar contido na estrutura original
    """
    intervals_in_day = 24
    compressed_cluster = Clusterrer(
        parameters,
        n_clusters,
        intervals_in_day,
        "prosumer.p_e_load",
        "prosumer.p_t_load",
    )
    parameters = compressed_cluster.dict()

    # how many elements a cluster represents
    cluster_freq = parameters["cluster_freq"]
    #o horizonte precisa ser ajustado manualmente porque não é possivel saber qual nome ou onde o usuario configurou esse parâmetro, mas basta arrumar isso como fiz na linha seguinte
    parameters["general"]["horizon"] = len(cluster_freq) * intervals_in_day

    print("\n\n\n\n\nFimal parameters:\n")
    pprint(parameters, indent=2, compact=True, width=100)

    print(f"\nCluster concluded! Number of elements per cluster: {cluster_freq}")


if __name__ == "__main__":
    # Ficheiro JSON com os dados a serem clusterizados
    INPUT_PATH = "input_example.json"
    with open(INPUT_PATH) as json_file:
        params = json.load(json_file)

    #define o numero de clusters que serão criados
    n_clusters = 2

    # Usar estas duas proximas linhas para obter resultados e por em graficos
    outputs1 = optimization(params, n_clusters)
    
