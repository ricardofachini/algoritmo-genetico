import random
import matplotlib.pyplot as plt
import numpy
from prettytable import PrettyTable
import pygad

# Define os itens (peso e valor) e a capacidade da mochila
items = [
    {'value': 10, 'weight': 5},
    {'value': 40, 'weight': 4},
    {'value': 30, 'weight': 6},
    {'value': 50, 'weight': 3},
    {'value': 35, 'weight': 8}
]
capacity = 10
pop_size = 500
num_generations = 100
mutation_rate = 0.05
convergence_threshold = 40  # Parar se não houver melhoria após X gerações


# Função de fitness
def fitness(solution, items, capacity):
    total_value = 0
    total_weight = 0
    for i in range(len(solution)):
        if solution[i] == 1:
            total_value += items[i]['value']
            total_weight += items[i]['weight']
    if total_weight > capacity:
        return 0  # Penaliza se o peso exceder a capacidade
    return total_value


# Gera uma população inicial
def generate_population(pop_size, num_items):
    return [[random.choice([0, 1]) for _ in range(num_items)] for _ in range(pop_size)]


# Seleção via roleta
def selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    pick = random.uniform(0, total_fitness)
    current = 0
    for i, individual in enumerate(population):
        current += fitness_scores[i]
        if current > pick:
            return individual


# Crossover de um ponto
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]


# Mutação
def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 if individual[i] == 0 else 0


# Algoritmo Genético com Critério de Convergência
def genetic_algorithm(items, capacity, pop_size, num_generations, mutation_rate, convergence_threshold):
    num_items = len(items)
    population = generate_population(pop_size, num_items)
    best_fitness_values = []  # Armazenar a melhor fitness em cada geração
    no_improvement_count = 0  # Contador de gerações sem melhoria
    best_overall_fitness = 0  # Melhor fitness já encontrado

    for generation in range(num_generations):
        fitness_scores = [fitness(individual, items, capacity) for individual in population]
        new_population = []

        best_fitness = max(fitness_scores)
        best_fitness_values.append(best_fitness)

        # Se a melhor solução não melhorar em X gerações, parar
        if best_fitness > best_overall_fitness:
            best_overall_fitness = best_fitness
            no_improvement_count = 0  # Reset contador de estagnação
        else:
            no_improvement_count += 1

        if no_improvement_count >= convergence_threshold:
            print(f"Convergência atingida na geração {generation} com fitness {best_fitness}")
            break

        for _ in range(pop_size // 2):
            # Seleciona dois pais
            parent1 = selection(population, fitness_scores)
            parent2 = selection(population, fitness_scores)

            # Cruzamento
            child1, child2 = crossover(parent1, parent2)

            # Mutação
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)

            new_population.extend([child1, child2])

        population = new_population
        print(f'Geração {generation}: Melhor fitness = {best_fitness}')

    # Melhor solução
    best_solution = max(population, key=lambda ind: fitness(ind, items, capacity))
    return best_solution, best_fitness_values


# Executa o algoritmo genético
best_solution, fitness_history = genetic_algorithm(items, capacity, pop_size, num_generations, mutation_rate,
                                                   convergence_threshold)

# Plots da execução
plt.plot(fitness_history)
plt.title('Convergência do Algoritmo Genético - Problema da Mochila')
plt.xlabel('Gerações')
plt.ylabel('Fitness (Valor Total)')
plt.show()

print(f'Melhor solução: {best_solution}')
print(f'Itens escolhidos: {[i for i, x in enumerate(best_solution) if x == 1]}')

