import csv
import pandas as pd

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

print(population)
