from random import choices
import math


class Genetics_Algorithm_f6:
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

                population.append(elements)
                population_bit.append(elements_bit)

                create = self.create_genome()

        return population, population_bit





    def f6_function(self,x,y):
        x_y = float(x ** 2 + y ** 2)
        square = math.sqrt(x_y)
        sin = (math.sin(square) ** 2)
        fraction = (((sin) - (0.5))) / (((1 + (float(0.001) * (x_y)))) ** 2)
        result = (0.5) - fraction
        return result 
    
        



#datas

bits = 44
limit = [[-100,100],[-100,100]]
population = 100
generation = 40
f = Genetics_Algorithm_f6(bits,population_size=population,limit=limit,generation=40)
real,bit = f.convert()


lista = [ f.f6_function(element["x"], element["y"]) for element in real ]


print(lista)
from matplotlib import pyplot as plt
plt.plot(range(len(lista)), lista)
plt.grid(True, zorder=0)
plt.title("F6")
plt.xlabel("geration")
plt.ylabel("media value f6 function")
plt.show()