# Les données de la conjoncture démographique de la France, Institut national d'études démographiques (Ined)
# Revue Population (Ed.), 2020, "Base de données – Démographie de la France entière et métropolitaine". Paris, Ined. http://hdl.handle.net/20.500.12204/AXWs9WivkgKZhr-blhHr

# Sources :
# Population au 1er janvier France métropolitaine
# 1901-1945 : Insee, T6 – Population totale par sexe, âge et état matrimonial au 1er janvier - Séries depuis 1901 -  https://insee.fr/fr/statistiques/4135499?sommaire=4136000
# 1946-2020 : Insee, Composantes de la croissance démographique, France métropolitaine - https://www.insee.fr/fr/statistiques/1892117?sommaire=1912926
# Population au 1er janvier France entière
# 1982-2020 : Insee, Composantes de la croissance démographique, France - https://www.insee.fr/fr/statistiques/1892117?sommaire=1912926
# Naissances, décès, solde naturel, solde migratoire et solde total - France métropolitaine
# 1901-1945 Naissances, décès : Insee, T1 – Évolution générale de la situation démographique - Séries depuis 1901 - https://www.insee.fr/fr/statistiques/4135499?sommaire=4136000
# 1901-1945 Solde naturel et migratoire : Insee, Démographie - Décès de tous âges - France métropolitaine - https://insee.fr/fr/statistiques/4135499?sommaire=4136000
# 1946-2020 : Insee, Composantes de la croissance démographique, France métropolitaine - https://www.insee.fr/fr/statistiques/1892117?sommaire=1912926
# Naissances, décès, solde naturel, solde migratoire et solde total - France entière
# 1982-2020 : Insee, Composantes de la croissance démographique, France - https://www.insee.fr/fr/statistiques/1892117?sommaire=1912926
# Taux bruts de natalité, mortalité et d'accroissement naturel - France métropolitaine
# 1901-1945 : Insee, T1 – Évolution générale de la situation démographique - Séries depuis 1901 - https://www.insee.fr/fr/statistiques/4135499?sommaire=4136000
# 1946-2019 : Insee, Composantes de la croissance démographique, France métropolitaine - https://www.insee.fr/fr/statistiques/1892117?sommaire=1912926
# Taux bruts de natalité, mortalité et d'accroissement naturel - France entière
# 1982-2019 : Insee, Principaux taux, France - https://www.insee.fr/fr/statistiques/1892117?sommaire=1912926
# Taux accroissement total : Le taux de variation de la population une année donnée correspond à la somme du solde naturel et du solde migratoire divisée par la population au 1er janvier de cette année.


# cause de mortalités : http://cepidc-data.inserm.fr/inserm/html/index2.htm

import csv
from numpy import inf
from plotnine import *
import pandas as pd

FrancePopData = []

with open('Donnees_annexes_FR_12122020.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        FrancePopData.append(
            {'year': row['Année'],
             'pop': row['Population au 1er janvier(1) France métropolitaine'],
             'births': row['Naissance France métropolitaine'],
             'deaths': row['Décès(3) France métropolitaine']
             })

# removing 2020 as data is incomplete

FrancePopData.pop()

for row in FrancePopData:
    for k in row:
        v = row[k]
        if v == 'n.d.':
            row[k] = None
        else:
            row[k] = float(v.rstrip('*'))

FrancePopData[0]['computedPop'] = FrancePopData[0]['pop']
minBirthRate = inf
for i in range(1, len(FrancePopData)):
    yrow = FrancePopData[i]
    yrow['computedPop'] = (FrancePopData[i-1]['pop'] if FrancePopData[i-1]['pop'] is not None else FrancePopData[i-1]['computedPop']) + \
        FrancePopData[i-1]['births']-FrancePopData[i-1]['deaths']

    yrow['birthRatep1000'] = None if yrow['births'] is None else 1000 * \
        yrow['births']/(yrow['pop'] if yrow['pop']
                        is not None else yrow['computedPop'])

    if yrow['birthRatep1000']:
        minBirthRate = min(minBirthRate, yrow['birthRatep1000'])


franceAccidentsMortalityRate = {}
with open('tcs_evo.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        # print(row)
        startYear = int(row['période'].split('-')[0])
        for year in range(startYear, startYear+3):
            franceAccidentsMortalityRate[year] = float(
                row['ttage_tot_taux'])/100000
            # print(franceAccidentsMortalityRate[year])


# theoreticalFixedBirthRate = FrancePopData[-1]['birthRatep1000']/1000

# 2 enfants par couple, si on double l'esperence de vie
theoreticalFixedBirthRate = 1/(79.8+85.7)

# average mortality rate in france From 2014 to 2016 when accounting only for accidental deaths and not diseases
theoreticalFixedMortalityRate = 50.3/100000

FIRST_YEAR_WITHOUT_AGING = 1982

firstRow = FIRST_YEAR_WITHOUT_AGING-1902

FrancePopData[firstRow]['popNoDiseases'] = FrancePopData[firstRow]['pop']
FrancePopData[firstRow]['popNoDiseasesFixedMortality'] = FrancePopData[firstRow]['pop']
FrancePopData[firstRow]['popNoDiseasesControlledBirthRate'] = FrancePopData[firstRow]['pop']
for i in range(firstRow+1, len(FrancePopData)):
    previousYear = FIRST_YEAR_WITHOUT_AGING+i-firstRow-2
    yrow = FrancePopData[i]
    yrow['popNoDiseasesFixedMortality'] = FrancePopData[i-1]['popNoDiseasesFixedMortality'] + \
        FrancePopData[i-1]['births'] - \
        (FrancePopData[i-1]['popNoDiseasesFixedMortality']
         * theoreticalFixedMortalityRate)

    mortalityRate = franceAccidentsMortalityRate[
        previousYear] if previousYear in franceAccidentsMortalityRate else theoreticalFixedMortalityRate
    print(previousYear, mortalityRate, FrancePopData[i-1]['year'])
    yrow['popNoDiseases'] = FrancePopData[i-1]['popNoDiseases'] + \
        FrancePopData[i-1]['births'] - \
        (FrancePopData[i-1]['popNoDiseases'] * mortalityRate)

    birthsIfMinBirthRate = FrancePopData[i -
                                         1]['popNoDiseasesControlledBirthRate']*theoreticalFixedBirthRate

    yrow['popNoDiseasesControlledBirthRate'] = FrancePopData[i - 1]['popNoDiseasesControlledBirthRate'] + \
        birthsIfMinBirthRate - \
        (FrancePopData[i - 1]['popNoDiseasesControlledBirthRate']
         * theoreticalFixedMortalityRate)


for i in range(40):

    birthsIfMinBirthRate = FrancePopData[len(FrancePopData) -
                                         1]['popNoDiseasesControlledBirthRate']*theoreticalFixedBirthRate

    FrancePopData.append({

        'year': FrancePopData[len(FrancePopData) - 1]['year']+1,
        'popNoDiseasesControlledBirthRate': FrancePopData[len(FrancePopData) - 1]['popNoDiseasesControlledBirthRate'] +
        birthsIfMinBirthRate -
        (FrancePopData[len(FrancePopData) - 1]['popNoDiseasesControlledBirthRate']
         * theoreticalFixedMortalityRate)

    })


for row in FrancePopData[80:90]:
    print(row)

print('theoreticalFixedBirthRate', theoreticalFixedBirthRate)

data = pd.DataFrame(FrancePopData)


plot = (ggplot(aes(x='year'), data)
        + geom_line(aes(y='pop'))
        + geom_line(aes(y='popNoDiseases'), color='purple')
        + geom_line(aes(y='popNoDiseasesControlledBirthRate'), color='#e41a1c')
        + ylim(0, None)
        )


print(plot)
