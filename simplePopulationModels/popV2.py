import csv
from functools import reduce

# Sources :,
# "Somme des taux par âge (p.100 femmes), ICF, âge moyen à la maternité - France métropolitaine",
# "1901-1945 : Calculs à partir de données Insee, T44 – Taux de fécondité générale par âge de la mère - Séries depuis 1901 - https://www.insee.fr/fr/statistiques/2045355?sommaire=2045470",
# "1946-2019 : Calculs à partir de données Insee, Taux de fécondité par âge détaillé de la mère, France métropolitaine - https://www.insee.fr/fr/statistiques/1892259?sommaire=1912926",
# "Somme des taux par âge (p.100 femmes), ICF, âge moyen à la maternité - France entière",
# "1994-2019 : Calculs à partir de données Insee, Taux de fécondité par âge détaillé de la mère, France, https://www.insee.fr/fr/statistiques/2381390 (Âge moyen de la mère à l’accouchement - https://www.insee.fr/fr/statistiques/1892259?sommaire=1912926",
# Âge moyen à la maternité - France métropolitaine,
# "1941-1999 : France métropolitaine -  calculs de L. Toulemon à partir des taux de primo-fécondité de deuxième catégorie (moyennes mobiles sur 5 ans), sur la base des données de l'Enquête Histoire Familiale (EHF) 1999 (Toulemon L., Pailhé A., Rossier C., 2008, France: High and stable fertility, Demographic Research, 19(16): 503–556).",
# 2000 : estimation d’après les statistiques de l’état civil.,
# "2004-2010 : France métropolitaine - repris de Davie E., Niel X., 2012, Mesurer et étudier la fécondité selon le rang de naissance: élaborer une statistique de nombre de naissances et d'âge à l'accouchement par rang, Insee, Document de travail F1205, tableau 3.",
# À partir de 2013 : Eurostat (fourni par l'Insee).,
# Naissances hors mariage et part dans la fécondité totale - France métropolitaine et entière,
# "1901-2019 : Insee, T34 – Nés vivants et enfants sans vie selon la situation matrimoniale des parents - Séries depuis 1901 pour la France métropolitaine - https://insee.fr/fr/statistiques/4190308?sommaire=4190525",
# "1994-2019 : Insee, T34 – Nés vivants et enfants sans vie selon la situation matrimoniale des parents - Séries depuis 1994 pour la France entière -https://insee.fr/fr/statistiques/4190308?sommaire=4190525",


# répartitiopn population en 1901 : "Source : Insee, état civil et recensement de population "

sum = 0
yearsCount = 0
with open('Donnees_annexes_FR_12122020_Annexe_4_Fecondite.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')

    for row in reader:
        fertilityRate = float(
            row['Indicateur conjoncturel de fécondité France métropolitaine'].replace(',', '.'))
        sum += fertilityRate
        yearsCount += 1
        # print(row['Année'], 'fertilityRate', fertilityRate)

FranceAverageFertilityRate = sum/yearsCount
# Average fertility rate in Metropolitan France from 1901 to 2019


INIT_POP = 38485925
LIFE_EXPECTANCY = int((45.4+49)/2)

CHILDREN_P_PERSON = FranceAverageFertilityRate/200
MATERNITY_AVERAGE_AGE = int(29.4)


# Load population count by age in 1901 in France
population = {}
with open('simplePopulationModels/population1901FranceMetropolitaine.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')

    for row in reader:
        rawAge = row['Age en années révolues']
        if rawAge == '100 ou plus ':
            age = 100
        else:
            age = int(rawAge)
        count = int(row['Les deux sexes'])
        population[age] = count


def addYear():

    global population

    newPopulation = {0: 0}

    # grow older
    for age in range(LIFE_EXPECTANCY+1):

        newPopulation[age+1] = population[age]

    # old people die
    print('{:,}'.format(newPopulation[LIFE_EXPECTANCY+1]), "people die")
    newPopulation[LIFE_EXPECTANCY+1] = 0

    # new adults have children
    newPopulation[0] = int(
        newPopulation[MATERNITY_AVERAGE_AGE]*CHILDREN_P_PERSON)

    print('{:,}'.format(newPopulation[0]), "children born")

    population = newPopulation


print()
totalPop = reduce(lambda v, e: v+e, population.values())
print('pop :', '{:,}'.format(totalPop))

for year in range(1901, 1903):

    print('---------------------------')
    print('year', year)

    # print(population)

    addYear()

    totalPop = reduce(lambda v, e: v+e, population.values())

    print('pop :', '{:,}'.format(totalPop))
