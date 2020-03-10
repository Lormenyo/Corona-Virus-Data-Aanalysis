import time
start = time.time()
import sys
import csv

script = sys.argv[0]
infection_dataset = sys.argv[1]
population_dataset = sys.argv[2]

class Corona:
    def __init__(self, infectionDataset, populationDataset):
        self.cases = []
        self.population = []
        self.population_dict = {}
        self.cases_dict = {}
        self.deaths_dict = {}
        self.infectionRates = {}
        self.deathRates = {}
        self.infectionPerDay = {}

        self.file = open('task1_solution-covid_data-population_data.txt', 'a')

        with open(populationDataset) as csvfile:
            p = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in p:
                self.population.append(row)
            

        with open('covid_data.csv') as csvfile:
            f = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in f:
                self.cases.append(row)

        for row in self.population[1:]:
            country = row[0]
            if len(row) > 4:
                row.remove(row[2])
                self.population_dict[country] = int(row[2])
            else:
                self.population_dict[country] = int(row[2])


        for row in self.cases[1:]:
            country = row[1]
            if country in self.cases_dict.keys():
                self.cases_dict[country] += int(row[2])
                self.deaths_dict[country] += int(row[3])
            else:
                self.cases_dict[country] = int(row[2])
                self.deaths_dict[country] = int(row[3])

        for country in self.population_dict.keys():
            if country not in self.cases_dict.keys():
                pass
            else:
                infectionRate = self.cases_dict[country]/self.population_dict[country]
                self.infectionRates[country] = infectionRate

   
        for country in self.cases_dict.keys():
            deathRate = self.deaths_dict[country]/self.cases_dict[country]
            self.deathRates[country] = deathRate

        
        for row in self.cases[1:]:
            country = row[1]
            if country not in self.infectionPerDay.keys():
                self.infectionPerDay[country] = [int(row[2])/6,1]
            elif country in self.infectionPerDay.keys() and self.infectionPerDay[country][1] !=7:
                new_slope = self.infectionPerDay[country][0] - int(row[2])/6
                self.infectionPerDay[country][0] += new_slope
                self.infectionPerDay[country][1] += 1
            else:
                pass

        # print(self.population[:5])
        # print(self.cases[:5])

    def getHighestInfection(self):
     
        infection_values = list(self.cases_dict.values())
        sorted_values = list(self.cases_dict.values())
        sorted_values.sort(reverse=True)
        
        # Country with the highest infection
        highestInfectionCountry = list(self.cases_dict.keys())[infection_values.index(sorted_values[0])]
        #number of infections in that country
        highestInfection = sorted_values[0]
        # print(highestInfectionCountry, highestInfection)

        # Country with the second highest infection
        secondHighestInfectionCountry = list(self.cases_dict.keys())[infection_values.index(sorted_values[1])]
        #number of infections in that country
        secondHighestInfection = sorted_values[1]
        # print(secondHighestInfectionCountry, secondHighestInfection)
        self.file.write('(a) %s, %d \n(b) %s, %d \n' %(highestInfectionCountry, highestInfection, secondHighestInfectionCountry,secondHighestInfection))

    def getHighestInfectionRate(self):
        infectionRate_values = list(self.infectionRates.values())
        sortedRates_values = list(self.infectionRates.values())
        sortedRates_values.sort(reverse=True)
       
        # Country with the Highest Infection rate(ratio of the number of infections to population)
        highestInfectionRateCountry = list(self.infectionRates.keys())[infectionRate_values.index(sortedRates_values[0])]
        #Infection Rate in that country
        highestInfectionRate = sortedRates_values[0]
        # print(highestInfectionRateCountry, highestInfectionRate)
        self.file.write('(c) %s, %f \n' %(highestInfectionRateCountry, highestInfectionRate))  
    
    def getOverallDeathRate(self):
        #overall death rate (ratio of number of deaths to number of infections) 
        overallDeathRate = sum(list(self.deaths_dict.values()))/sum(list(self.cases_dict.values()))
        self.file.write('(d) %f \n' %(overallDeathRate))

    def getHighestDeathRate(self):
        deathRate_values = list(self.deathRates.values())
        sortedDeathRates = list(self.deathRates.values())
        sortedDeathRates.sort(reverse=True)
        # Country with the Highest Death rate (ratio of number of deaths to number of infections)
        highestDeathRateCountry = list(self.deathRates.keys())[deathRate_values.index(sortedDeathRates[0])]
        #Infection Rate in that country
        highestDeathRate = sortedDeathRates[0]
        self.file.write('(e) %s, %f \n' %(highestDeathRateCountry, highestDeathRate))


    def getInfectionPerDay(self):
        negativeInfectionCountries = []
        positiveInfectionCountries = []
        maxIncrease = list(self.infectionPerDay.values())[0][0]
        maxDecrease = list(self.infectionPerDay.values())[0][0]
        for dailyInfection in list(self.infectionPerDay.values()):
            #   dailyInfectionValues.append(dailyInfection[0])
            country = list(self.infectionPerDay.keys())[list(self.infectionPerDay.values()).index(dailyInfection)]
            if dailyInfection[0] > 0.0:
                positiveInfectionCountries.append(country)
            # elif dailyInfection[0] == 0.0:
            #     pass
            else:
                negativeInfectionCountries.append(country)
        
    
            if dailyInfection[0] < 0.0 and dailyInfection[0] < float(maxDecrease):
                maxDecreaseCountry, maxDecrease = country, dailyInfection[0]

            elif dailyInfection[0] > 0.0 and dailyInfection[0] > float(maxIncrease):
                maxIncreaseCountry, maxIncrease = country, dailyInfection[0]
            else:
                pass
 
        self.file.write('(f) ')
        for s in set(positiveInfectionCountries):
            self.file.write(s + ',')
        self.file.write('\n')
        self.file.write('(g) %s \n'%(maxIncreaseCountry)) 

        self.file.write('(h) ')
        for s in set(negativeInfectionCountries):
            self.file.write(s + ',')
        self.file.write('\n')
        self.file.write('(i) %s \n'%(maxDecreaseCountry))
        # print("Negative Infection per Day ")
        # print(negativeInfectionCountries)

        # print("Positive Infection per Day ")
        # print(positiveInfectionCountries)
        # print("Max Increase = ", maxIncrease, maxIncreaseCountry)
        # print("Max Decrease = ", maxDecrease, maxDecreaseCountry)

    def closeFile(self):
        self.file.close()


corona = Corona(infection_dataset, population_dataset)
corona.getHighestInfection()
corona.getHighestInfectionRate()
corona.getOverallDeathRate()
corona.getHighestDeathRate()
corona.getInfectionPerDay()
corona.closeFile()
print("Runtime: ",time.time()-start)