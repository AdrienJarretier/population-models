

INIT_POP = 2
LIFE_EXPECTANCY = 20

CHILDREN_P_PERSON = 2
SEXUAL_MATURITY = 15


class Person:

    nextId = 0

    population = {}

    def __init__(self, age):
        self.age = age
        self.children = []

        self.id = Person.nextId
        Person.nextId += 1


        Person.population[self.id] = self

    def addYear(self, years):
        if self.alive():
            self.age += years

    def haveChildren(self):
        if self.alive() and self.age > SEXUAL_MATURITY:
            if len(self.children) < CHILDREN_P_PERSON:
                for i in range(len(self.children), CHILDREN_P_PERSON):
                    self.children.append(Person(0))

        return self.children

    def alive(self):

        return self.age <= LIFE_EXPECTANCY


def addYear():

    popWithoutDead = {}
    popWithChildren = {}

    for id, p in Person.population.items():
        p.addYear(1)

    for id, p in Person.population.items():
        if p.alive():
            popWithoutDead[p.id] = p

    for id, p in popWithoutDead.items():

        popWithChildren[p.id] = p
        for child in p.haveChildren():
            popWithChildren[child.id] = child

    Person.population = popWithChildren


for i in range(INIT_POP):
    Person(0)

for year in range(1000):

    print('---------------------------')
    # for i, p in enumerate(population):
    #     print('p' + str(i), p.age)
    print('year', year, 'pop :', len(Person.population))

    addYear()
