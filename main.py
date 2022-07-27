from numpy.random import rand, randint
import numpy as np
import matplotlib.pyplot as plt
import math
from random import choices
import sys
from decimal import Decimal

# Gustavo Gomes de Lima
# Matricula: 202008058

# Parametros de entrada do Algoritmo Genetico
limites = [[-100, 100], [-100, 100]]
num_ger = 40
meio_genoma = 22
bits = 44  #numero de bits do Genoma
pop_size = 100
taxa_crossover = 0.65
taxa_mutaçao = 0.008
genoma = []

# Gera a função F6
def function_f6(I):
    x = I['x']
    y = I['y']
    x_y_pow = float(x ** 2 + y ** 2)
    square_of_pow = math.sqrt(x_y_pow)
    sin_pow = (math.sin(square_of_pow) ** 2)
    fraction = (((sin_pow) - (0.5))) / (((1 + (float(0.001) * (x_y_pow)))) ** 2)
    result = (0.5) - fraction
    return result

# Gera uma população mutada
def mutation(pop_bin, taxa_mutaçao):
    filhoX = list()
    filhoY = list()
    população_mutada = []
    for i in range(len(pop_bin)):
        p1x = pop_bin[i]['x'] # parent X
        p1y = pop_bin[i]['y'] # parent y
        c1x = meio_mutation(p1x, taxa_mutaçao, filhoX)
        c1y = meio_mutation(p1y, taxa_mutaçao, filhoY)
        individual_bit_mutaded = {
            "x": c1x[0],
            "y": c1y[0]
        }
        população_mutada.append(individual_bit_mutaded)

    return população_mutada

# Realiza mutação nos filhos
def meio_mutation(p1, taxa_mutaçao, filho):
    if rand() < taxa_mutaçao:
        cp = randint(0, len(p1))  # gera gene aleatorio
        c1 = p1
        c = list(c1)

        if c[cp] == "1":
            c[cp] = "0" # virar
        else:
            c[cp] = "1"
        c_aux = ''.join([str(elem) for elem in c])
        filho.append(c_aux)
    else:
        filho.append(p1)
    return filho

# Realiza o crossover nos filhos
def crossover(pop_bin, taxa_crossover):
    filho = []
    for i in range(int(len(pop_bin)/2)):
        p1x = pop_bin[2*i-1]['x']   # parent 1
        p2x = pop_bin[2*i]['x'] # parent 2
        p1y = pop_bin[2*i-1]['y']   # parent 1
        p2y = pop_bin[2*i]['y'] # parent 2
        rand_variable = rand()
        if rand_variable < taxa_crossover:
            #print("aleatorio",rand_variable)
            cp = randint(1, len(pop_bin)-1, size=2)
            #print(cp)

            while cp[0] == cp[1]:
                cp = randint(1, len(pop_bin)-1, size=2)
            cp = sorted(cp)
            c1 = p1x[:cp[0]] + p2x[cp[0]:cp[1]] + p1x[cp[1]:]
            c2 = p2y[:cp[0]] + p1y[cp[0]:cp[1]] + p2y[cp[1]:]
            c = {
                'x': c1,
                'y': c2
            }
            filho.append(c)

        else:
            c1 = {
                'x':p1x,
                'y':p1y
            }

            c2 = {
                'x':p2x,
                'y':p2y
            }
            filho.append(c1)
    return filho

# Seleção do metodo da roleta
def selection(pop_bin, fitness, pop_size):
    next_generation = list()
    elite = np.argmax(fitness)
    next_generation.append(pop_bin[elite])  # Mantem o melhor
    P = [f/sum(fitness) for f in fitness]   # Seleção da prob

    index = list(range(int(len(pop_bin))))

    index_selected = np.random.choice(index, size=pop_size-1, replace=False,)
    s=0

    print("POPBIN", pop_bin)

    for j in range(pop_size-1):
        next_generation.append(pop_bin[index_selected[s]])
        s+=1

    return next_generation

# Cria a população de 44 bits para real
def inicializa_pop(bounds, bits, genome):
    lower_x_boundary, upper_x_boundary = bounds[0]
    lower_y_boundary, upper_y_boundary = bounds[1]
    half_genome = bits/2
    population = []
    population_bit = []

    for i in range(pop_size):
        cromossomox = ""
        cromossomoy = ""

        for j in range(len(genome)):
            if j < half_genome:
                cromossomox += str(genome[j])
            else:
                cromossomoy += str(genome[j])
        individual_bit = {
            "x": cromossomox,
            "y": cromossomoy
        }
        if cromossomox != '' and cromossomoy != '':
            b = int(cromossomox, 2)
            cromossomox_float = float(b)
            c = (int(cromossomoy, 2))
            cromossomoy_float = float(c)
            if type(cromossomox_float) == float and type(cromossomoy_float) == float:
                cromossomox_decimal = cromossomox_float * float((upper_x_boundary - lower_x_boundary) / (pow(2, half_genome) - 1)) + float(lower_x_boundary)
                cromossomoy_decimal = cromossomoy_float * float((upper_y_boundary - lower_y_boundary) / (pow(2, half_genome) - 1)) + float(lower_y_boundary)
                individual = {
                    "x": cromossomox_decimal,
                    "y": cromossomoy_decimal
                }
                population.append(individual)
                population_bit.append(individual_bit)

                genome = gerar_genoma(bits)
            else:
                break

    return population, population_bit

# Gera o genoma
def gerar_genoma(length: int):
    choices_selected = choices([0, 1], k=length)
    return choices_selected

# Programa Principal

genoma = gerar_genoma(bits)
pop_real, pop_bin = inicializa_pop(limites, bits, genoma)
filhos_mutados = []
bits2 = 22
melhor_fitness = []
lista_genoma= []
lista_medias = []


for gen in range(num_ger):
    print(gen, "- Geração")
    filho = crossover(pop_bin, taxa_crossover)
    filho = mutation(filho, taxa_mutaçao)


    for p in filho:
        filhos_mutados.append(p)


    for _ in filhos_mutados:
        genoma = ''.join(str(_['x']) + str(_['y']))
        lista_genoma.append(genoma)

    # Chama a função inicializa para fazer a decodificação da lista mutada/com crossover dos 44 bits para reais
    for p in lista_genoma:
        real_chromossome, real_chromossome_bin = inicializa_pop(limites, bits, p)

    # Calcula os valores da função f6
    fitness = [function_f6(d) for d in real_chromossome]

    # Descobre o indice do melhor e do pior e seleciona o melhor em real e binario
    index = np.argmax(fitness)
    index_min = np.argmin(fitness)
    current_best = fitness[index]
    current_best_bin = real_chromossome_bin[index]
    current_worst_bin = real_chromossome_bin[index_min]

    # Seleciona o valor maximo em real
    melhor_fitness.append(max(fitness))

    # Faz a seleção na lista de população, adiciona o melhor binario anterior e deleta o pior
    pop_bin = selection(real_chromossome_bin, fitness, pop_size)
    pop_bin.append(current_best_bin) # Consertar - ( numero real na lista bin)
    del (pop_bin[index_min])

print("Lista dos melhores ->", melhor_fitness)
media = np.mean(melhor_fitness)
lista_medias.append(media)
print("Media dos valores ->", media)
