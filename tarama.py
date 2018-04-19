import math
import csv
import pants
import networkx as nx
import matplotlib.pyplot as plt

#Set du graphique
mapNantes = nx.Graph()
nx.draw(mapNantes)
plt.draw()

poids = 0

nodes = []
# Reading du csv
with open('/Users/banane/PycharmProjects/Fourmi/venv/VOIES_NM.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    i = 0
    for row in reader:
        i = i + 1
        # Attribution des variables
        label = row['COMMUNE'] + " " + row['LIBELLE']  # Ville + rue
        tenant = row['TENANT']
        aboutissant = row['ABOUTISSANT']
        nodes.append((row['BI_MIN'], row['BI_MAX']))
        bi_min = row['BI_MIN']
        bi_max = row['BI_MAX']
        bp_min = row['BP_MIN']
        bp_max = row['BP_MAX']
        statut = row['STATUT']
        #Gestion des rues sans BI ou BP
        if bi_min == "":
            bi_min = 1
        if bi_max == "":
            bi_max = bi_min
        if bp_min == "":
            bp_min = 2
        if bp_max == "":
            bp_max = bp_min

        #nx.draw_networkx_edge_labels(mapNantes, nx.circular_layout(mapNantes), edge_labels=label)

        poids = max(((int(bi_max) - int(bi_min))/2)+1,((int(bp_max) - int(bp_min))/2))
        if tenant != "" and aboutissant != "":
            print(tenant + " -> " + aboutissant)
            mapNantes.add_edge(tenant, aboutissant, weight=poids, label=label)
        if tenant != '' and aboutissant == "Impasse":
            print(tenant + aboutissant)
            mapNantes.add_edge(tenant, aboutissant, weight=poids, label=label)

# nx.draw_random(mapNantes)
#nx.draw_networkx_labels(mapNantes)
nx.draw_circular(mapNantes)
nx.shortest_path_length(mapNantes, "SAUTRON Rue de la Pépinière", "SAUTRON Rue de la Bastille", poids)
print(nx.shortest_path(mapNantes, "SAUTRON Rue de la Pépinière", "SAUTRON Rue de la Bastille", poids))
plt.show()  # affichage


def euclidean(a, b):
    return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))


world = pants.World(nodes, euclidean)
solver = pants.Solver()
solution = solver.solve(world)
print(solution)
solutions = solver.solutions(world)
for sol in solutions:
    print(sol)


# recupération de toutes les routes possibles
def find_path(graph, start, end, path=[]):
    path = path + [start]  # ajout de passage
    if start == end:  # arrivée
        return path
    if not graph.has_key(start):  # problème
        return None
    for node in graph[start]:  # bouclage de la fonction sur elle même
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return newpath
    return None


find_path(mapNantes, tenant, aboutissant)

