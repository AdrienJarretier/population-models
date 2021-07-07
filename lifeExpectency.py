# Sources : ,,,,,,,,
# Espérance de vie ,,,,,,,,
# "1740-1809 : repris de Bourgeois-Pichat J., 1952, Note sur l'évolution générale de la population Française depuis de XVIIIe siècle, Population, vol.7, n°2, pp. 319–329.",,,,,,,,
# 1810-1945 : calculs par J. Vallin et F. Meslé - https://www.ined.fr/Xtradocs/cdrom_vallin_mesle/Fonctions-de-mortalite/Indicateurs-du-moment/Indic-moment.htm,,,,,,,,
# "1946-2019 : Insee, Espérance de vie à divers âges et taux de mortalité infantile, France métropolitaine - https://www.insee.fr/fr/statistiques/2554599?sommaire=1912926",,,,,,,,
# Taux de mortalité infantile et néo-natale ,,,,,,,,
# "1901-2018 : Insee, T70 – Évolution de la mortalité infantile et de ses diverses composantes - Séries depuis 1901 - https://www.insee.fr/fr/statistiques/4503155?sommaire=4503178&q=mortalit%C3%A9",,,,,,,,
# Survivants à 65 ans,,,,,,,,
# 1806-1945 : calculs par J. Vallin et F. Meslé - https://www.ined.fr/Xtradocs/cdrom_vallin_mesle/Fonctions-de-mortalite/Indicateurs-du-moment/Indic-moment.htm,,,,,,,,
# "1946-2018 : repris de Breton et al., 2019, L’évolution démographique récente de la France: une singularité en Europe?, Population,  vol.74, n°4, p. 409-497 (Tableau Annexe 11).",,,,,,,,


import csv

franceAccidentsMortalityRate = {}
with open('LifeExpectency.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        print(row)
        # startYear = int(row['période'].split('-')[0])
        # for year in range(startYear, startYear+3):
        #     franceAccidentsMortalityRate[year] = float(row['ttage_tot_taux'])/100000
        #     # print(franceAccidentsMortalityRate[year])