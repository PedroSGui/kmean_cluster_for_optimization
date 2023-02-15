import numpy as np
from sklearn.cluster import KMeans


class Clusterrer:
    """
    Function for performing the distance based kmean clustering procedure.

    A cluster é uma classe porque vai ser chamado na main como um objeto que tem atributos.
    A ideia é que esse script não tenha uma main porque tudo aqui são bases para o main que
    eu não queria colocar junto para o código não ficar muito grande
    """
    
    """
    parameters: É necessàrio passar a estrutura que deseja clusterizar
    n_cluster: Numero de dias que quer de output, precisa ser maior do que 0 e menor do que o tamanho da estrutura original
    intervals_in day: O numero de intervalos no dia é importante para a função entender a estrutura que esta a tratar
    *args: quantas string quiser, precisa estar contido na estrutura original
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
                # determina qual o tamanho do horizonte temporal a partir do tamanho de uma das componentes da estrutura original
                horizon_extended = len(self.estrutura_a_clusterizar[key_estrutura])
                # numero de dias que compõem o horizonte considendo que o periodo de simulação é de 1 hora
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

                    # ve se a posição é a ultima do dia e se for aumenta o numero de dias que já formou
                    if (
                        pos_elem_da_key_da_estrutura % periods_in_day
                    ) == periods_in_day - 1:
                        day_already_formed = day_already_formed + 1
                        if len(dist_total) < self.days:
                            # cria a distancia se ela ainda não existe, nesse exemplo é criado pelo primeiro vetor que é a distancia eletrica
                            dist_total.append(dist)
                        else:
                            # adiciona a distancia do dia existente, nesse caso a termica esta sendo adicionada a distancia eletrica, ams poderia ter outras distancias
                            dist_total[day_already_formed - 1] = (
                                dist_total[day_already_formed - 1] + dist
                            )
                        dist = 0

        # Aqui é uma mudança de estrutura de dados para que a informação da função instancia
        # caiba da forma correta no formato pedido pela biblioteca que uso para o Kmeans
        for i in range(int(self.days)):
            fitter.append([dist_total[i], 0])

        # Aplicação do Kmeans
        self.kmeans_results = KMeans(
            n_clusters=days_clustered, random_state=0, n_init="auto"
        ).fit(fitter)
        # print(dist_total) # descomenta para ver a distancia relativa de cada dia em ordem cronologica
        # print(self.kmeans_results.labels_) # descomenta pra ver que os dias com distancia semelhantes são agregados no mesmo dia

    def dict(self):
        final_estrutura_a_clusterizar = {}
        synthetized_freq = []
        soma_d = {}
        for key_estrutura in self.estrutura_a_clusterizar.keys():
            soma_d[key_estrutura] = []
            if type(self.estrutura_a_clusterizar[key_estrutura]) == list:
                for i in range(self.days_clustered):
                    if len(synthetized_freq) < self.days_clustered:
                        # armazena o tamanho do vetor com todas as posições que compõem o cluster
                        synthetized_freq.append(
                            len(np.where(self.kmeans_results.labels_ == i)[0])
                        )
                    for z in np.where(self.kmeans_results.labels_ == i)[0]:
                        # Aqui é onde eu crio o elemento representativo do cluster, escolhi fazer uma média dos vários inputs.
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

#Utilizado para planificar o dicionario disponibilizado de forma a poder receber qualquer estrutura de dicionario do usuario
def flatten_json(json):
    if type(json) == dict:
        for k, v in list(json.items()):
            if type(v) == dict:
                flatten_json(v)
                json.pop(k)
                for k2, v2 in v.items():
                    json[k + "." + k2] = v2
    return json

#processo reverso de restaurar a estrutura original
def unflatten_json(json):
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
