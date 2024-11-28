from pyevolve import G1DList, GSimpleGA, Selectors, Mutators, Crossovers, Consts
import random

# Definindo os itens e a capacidade da mochila
items = [
    {'value': 10, 'weight': 5},
    {'value': 40, 'weight': 4},
    {'value': 30, 'weight': 6},
    {'value': 50, 'weight': 3},
    {'value': 35, 'weight': 8}
]
capacity = 10


# Função de avaliação (fitness) para a mochila
def knapsack_fitness(chromosome):
    total_value = 0
    total_weight = 0

    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            total_value += items[i]['value']
            total_weight += items[i]['weight']

    if total_weight > capacity:
        return 0  # Penalidade por exceder o peso

    return total_value


# Configuração do cromossomo
genome = G1DList.G1DList(len(items))
genome.setParams(rangemin=0, rangemax=1)  # Soluções binárias (0 ou 1)
genome.evaluator.set(knapsack_fitness)  # Definindo a função de fitness

# Operadores genéticos: Seleção, Cruzamento e Mutação
genome.mutator.set(Mutators.G1DListMutatorFlip)  # Mutação de flip
genome.crossover.set(Crossovers.G1DListCrossoverSinglePoint)  # Crossover de um ponto
genome.initializator.set(G1DList.G1DListInitializatorInteger)  # Inicializador de cromossomos

# Configuração do algoritmo genético
ga = GSimpleGA.GSimpleGA(genome)
ga.setGenerations(100)  # Número máximo de gerações
ga.setPopulationSize(20)  # Tamanho da população
ga.setMutationRate(0.01)  # Taxa de mutação
ga.setCrossoverRate(0.9)  # Taxa de crossover
ga.selector.set(Selectors.GRouletteWheel)  # Seleção por roleta

# Critério de parada: estagnação de 20 gerações sem melhoria
ga.setMinimax(Consts.minimaxType["maximize"])  # Maximizar a função de fitness
ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)

# Executa o algoritmo genético
ga.evolve(freq_stats=10)  # Gera estatísticas a cada 10 gerações

# Resultados
best_solution = ga.bestIndividual()
print(f'Melhor solução: {best_solution}')
print(f'Fitness da melhor solução: {best_solution.fitness}')
print(f'Itens escolhidos: {[i for i, x in enumerate(best_solution) if x == 1]}')
