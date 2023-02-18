'''Exemplo DEAP. Tentamos desenvolver uma lista de dígitos para corresponder a uma lista de destino de
dígitos, que representa uma data.
'''
import random
from deap import algorithms
from deap import base
from deap import creator
from deap import tools

# Data, um alvo que queremos evoluir.
target = [2, 4, 0, 9, 2, 0, 1, 5]

# Nossa função de avaliação
def eval(individual):
    '''Avalie o indivíduo.
    
    Quanto mais próximo o indivíduo estiver do alvo, melhor será a aptidão.
    '''
    fit = 0
    for i in xrange(len(individual)):
        fit = fit + abs(individual[i] - target[i])
    
    # A função de avaliação deve retornar uma tupla, mesmo que haja apenas uma
    # critério de avaliação (por isso a vírgula).    
    return fit, 

# Criamos uma aptidão para os indivíduos, porque nossa função de avaliação nos dá
# Valores "melhores" quanto mais próximos estiverem de zero, daremos peso -1,0.
# Isso cria uma classe Creator.FitnessMin(), que agora pode ser chamada no
# código. (Pense nas fábricas de Java, etc.)
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

# Criamos uma classe Individual, que tem tipo base de lista, ela também utiliza nosso
# acabou de criar a classe Creator.FitnessMin().
creator.create("Individual", list, fitness=creator.FitnessMin)

# Criamos a caixa de ferramentas do DEAP. Que conterá nossas funções de mutação, etc.
toolbox = base.Toolbox()

# Criamos uma função chamada 'random_digit', que chama random.randint
# com parâmetros fixos, ou seja, chamar toolbox.random_digit() é o mesmo que
# chamando random.randint(0, 9)
toolbox.register('random_digit', random.randint, 0, 9)

# Agora, podemos fazer nosso código de criação individual (genótipo). Aqui fazemos a função para criar uma instância de
# criador.Individual (que tem lista do tipo base), com função tools.initRepeat. tool.initRepeat
# chama nossa função toolbox.random_digit recém-criada n vezes, onde n é o
# comprimento do nosso alvo. Isso é quase o mesmo que: [random.randint(0,9) for i in xrange(len(target))].
# No entanto, nosso indivíduo criado também terá uma aula de condicionamento físico anexada a ele (e
# possivelmente outras coisas não cobertas neste exemplo.)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.random_digit, n = len(target))

# Como agora temos nosso código de criação individual, podemos criar nosso código de população
# fazendo uma lista de toolbox.individual (que acabamos de criar na última linha).
# Aqui é bom saber que n (tamanho da população), não está definido neste momento
# (mas é necessário para a função initRepeat) e pode ser alterado ao chamar o
# toolbox.population. Isso pode ser alcançado por algo chamado funções parciais, verifique
# https://docs.python.org/2/library/functools.html#functools.partial se estiver interessado.
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Registramos nossa função de avaliação, que agora pode ser chamada como toolbox.eval(individual).
toolbox.register("evaluate", eval)

# Usamos estratégia de seleção simples onde selecionamos apenas os melhores indivíduos,
# agora pode ser chamado em toolbox.select.
toolbox.register("select", tools.selBest)

# Usamos o cruzamento de um ponto, agora chamado em toolbox.mate.
toolbox.register("mate", tools.cxOnePoint)

# Definimos nossa própria função de mutação que substitui um índice de um indivíduo
# com dígito aleatório.
def mutate(individual):
    i = random.randint(0, len(individual)-1)
    individual[i] = toolbox.random_digit()
    # A função de mutação do DEAP tem que retornar uma tupla, por isso tem vírgula
    # depois.
    return individual,

# Registramos nossa própria função de mutação como toolbox.mutate
toolbox.register("mutate", mutate)

# Agora definimos as funções básicas com as quais o algoritmo de evolução (EA) pode ser executado.
# Em seguida, definiremos alguns parâmetros que podem ser alterados entre as execuções do EA.

# Quantidade máxima de gerações para esta execução
generations = 100

# Cria população de tamanho 100 (agora definimos n, que faltou quando
# toolbox.population registrado).
pop = toolbox.population(n=100)

# Crie um hall da fama que armazena apenas o melhor indivíduo
hof = tools.HallOfFame(1)

# Obtenha algumas estatísticas da evolução em tempo de execução. Estes serão impressos para
# sys.stdout quando o algoritmo está em execução.
import numpy as np
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("std", np.std)
stats.register("min", np.min)
stats.register("max", np.max)

# Probabilidade de cruzamento
crossover_prob = 0.7

# Probabilidade de mutação
mutation_prob = 0.2

# Chame nosso algoritmo evolucionário atual que executa a evolução.
# eaSimple precisa de caixa de ferramentas para ter 'avaliar', 'selecionar', 'combinar' e 'mutar'
# funções definidas. Este é o algoritmo evolutivo mais básico. Aqui nós
# tem probabilidade de cruzamento de 0,7 e probabilidade de mutação de 0,2.
algorithms.eaSimple(pop, toolbox, crossover_prob, mutation_prob, generations, stats, halloffame=hof)

# Imprima o melhor indivíduo e sua aptidão
print hof[0], eval(hof[0])
