from hashlib import new
from random import choices,randint
import math

import numpy


class Genetics_Algorithm_f6:
    population = []
    population_bit = []
    fitness = []

    def __init__(self,bits,limit,population_size,generation,*args,**kwargs):
        # parameters
        self.bits = bits
        self.population_size = population_size
        self.value = ""
        self.limit = limit
        self.generation = generation
        

    
    def create_genome(self):
        self.value = choices([0,1],k=self.bits)
        return self.value

    def decimal(self,base ,max,min,k):
        calcul =  base * (max - min)/(2**k - 1) + min
        return calcul

    def convert(self):
        self.create_genome()
        half_genome = self.bits/2

        maxX,minX = self.limit[0]
        maxY,minY = self.limit[1]
        population = []
        population_bit = []

        for i in range(self.population_size):
            cromosso_x = ""
            cromosso_y = ""
            for index in range(len(self.value)):
                if index < half_genome:
                    cromosso_x += str(self.value[index])
                else:
                    cromosso_y += str(self.value[index])
            elements_bit = {
                "CX":cromosso_x,
                "CY":cromosso_y
            }

            if cromosso_x != "" and cromosso_y != "":
                cromosso_x_number_type = float(int(cromosso_x, 2))
                cromosso_y_number_type = float(int(cromosso_y, 2))

                decimal_x = self.decimal(cromosso_x_number_type,maxX,minX,half_genome)
                decimal_y = self.decimal(cromosso_y_number_type,maxY,minY,half_genome)

                elements = {
                    "x":decimal_x,
                    "y":decimal_y,
                }


                elements_bit_convert = cromosso_x + cromosso_y

                population.append(elements)
                population_bit.append(elements_bit_convert)
                
                create = self.create_genome()

        self.population = population
        self.population_bit_dentro = population_bit

        return population, population_bit





    def f6_function(self,x,y):
        x_y = float(x ** 2 + y ** 2)
        square = math.sqrt(x_y)
        sin = (math.sin(square) ** 2)
        fraction = (((sin) - (0.5))) / (((1 + (float(0.001) * (x_y)))) ** 2)
        result = (0.5) - fraction
        return result 

    
    def selection(self,population_bit,fitness,population_size):
        new_generation = []
        index = list(range(len(population_bit)))
        probability = [f/sum(fitness) for f in fitness]
        number_random = numpy.random.choice(index,size=population_size, p=probability)

        for z in number_random:
            new_generation.append(population_bit[z])
        return new_generation

    def crossover(self,rate,couples):
        sons = []
        number_rand = numpy.random.rand()
        if number_rand < rate:
            contador = 0
            while contador < len(couples):
                point = randint(2,44)
                
                cb_pai1 = couples[contador][:point - 1]
                cd_pai1 = couples[contador][point - 1:]
                cb_pai2 = couples[contador + 1][:point - 1]
                cd_pai2 = couples[contador + 1 ][point - 1:]
                son1 = cb_pai1 + cd_pai2
                son2 = cb_pai2 + cd_pai1
                sons.append(son1)
                sons.append(son2)
        
                contador += 2
        else:
            sons = couples        
        return sons

    def fitness(self,real):
        fitness = [ self.f6_function(element["x"], element["y"]) for element in real ]
        return fitness

            
        
    def mutation(self,sons,rate,population_bit,fitness):
        new_sons = []
        for son in sons:
            random_number_rate = numpy.random.rand()
            random_index = numpy.random.randint(0,44)
            if random_number_rate < rate:
                list_transform = [z for z in son]
                son_temp = ""
                if list_transform[random_index] == "0":
                    list_transform[random_index] = "1"
                else:
                    list_transform[random_index] = "0"

                for x in list_transform:
                    son_temp += x
                
                new_sons.append(son_temp)
            else:
                new_sons.append(son)

        number_random_son = numpy.random.randint(1,100)
        pai = numpy.argmax(fitness)
        elitism = population_bit[pai]

        new_sons[number_random_son] = elitism

        return new_sons
    
    def convert_real(self,bit):

        half_genome = int(self.bits/2)
        maxX,minX = self.limit[0]
        maxY,minY = self.limit[1]
        population = []
        for i in bit:
            cromosso_x = i[:half_genome]
            cromosso_y = i[half_genome:]

            if cromosso_x != "" and cromosso_y != "":
                cromosso_x_number_type = float(int(cromosso_x, 2))
                cromosso_y_number_type = float(int(cromosso_y, 2))

                decimal_x = self.decimal(cromosso_x_number_type,maxX,minX,half_genome)
                decimal_y = self.decimal(cromosso_y_number_type,maxY,minY,half_genome)

                elements = {
                    "x":decimal_x,
                    "y":decimal_y,
                }


                population.append(elements)



        return population




    def start_generation(self):
        real, bit = self.convert()
        fitness = self.fitness(real)
        list_best_fitness = []

        for ger in range(self.generation):
            selection = self.selection(bit, fitness, self.population_size)
            crossover = self.crossover(0.98, selection)
            mutation = self.mutation(crossover,0.08,bit,fitness)
            bit = mutation
            real = self.convert_real(bit)
            fitness = self.fitness(real)


            best_fitness = numpy.argmax(fitness)
            list_best_fitness.append(fitness[best_fitness])

            if ger == generation - 1:
                from matplotlib import pyplot as plt
                plt.plot(range(len(fitness)), list_best_fitness)
                plt.grid(True, zorder=0)
                plt.title("F6")
                plt.xlabel("geration")
                plt.ylabel("media value f6 function")
                plt.show()

            print(f"Geração - {ger} || fitness={fitness[best_fitness]} || X={} ")










    
        



#datas

bits = 44
limit = [[-100,100],[-100,100]]
population = 100
generation = 100




f = Genetics_Algorithm_f6(bits,population_size=population,limit=limit,generation=500)
real,bit = f.convert()





lista = [ f.f6_function(element["x"], element["y"]) for element in real ]
# z = f.selection(population_bit=bit, population_size=population,fitness=lista)

# p = f.crossover(100,z)
# m = f.mutation(p, 0.05)

# print(len(m))

# print(f.create_genome())



print(f.start_generation())

