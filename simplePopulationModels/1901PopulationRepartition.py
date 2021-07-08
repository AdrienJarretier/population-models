import csv
import pandas as pd

from plotnine import ggplot, geom_col, aes, ylim

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


data = pd.DataFrame(population.items(), columns=['age', 'pop'])

print(data)

plot = (ggplot(data, aes('age'))
        + geom_col(aes(y='pop'))
        )


print(plot)
