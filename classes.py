#AUTHOR: Patrick O'Connell
#DATE: 11/20/2020

import random
import math
import string
import copy
import numpy as np #going to start changing strings to char arrays to speed this up

class individual:
    """Holds relevant info of an individual: namely, its string and fitness"""
    
    def __init__(self, target_string):
        """initializes one individual"""
        self.target_string = target_string
        self.fitness = 0
        self.current_string = ""
        self.cum_prob = 0

        build_string = ""
        possible_chars = string.printable
        len = 0
        while (len < 50):
            j = random.randint(0, 94) #picks from printable characters not including newline, tabs (any whitespace char that isn't space)
            build_string = build_string + possible_chars[j]
            len += 1
        self.current_string = build_string

    def update_fitness(self):
        """(none) --> none
        updates the fitness of this individual by comparing the current string
        to the target string"""
        total_chars = len(self.current_string)
        correct_chars = 0

        i = 0
        while (i < total_chars):
            if (self.target_string[i] == self.current_string[i]):
                correct_chars += 1
            i += 1
        
        self.fitness = float(correct_chars) / float(total_chars)

    def change_string(self, new_str):
        """(string) --> none
        takes in a string, changes this individuals string to it"""

        self.current_string = new_str

    def mutate(self, mutation_prob):
        """for each char in the current_string, 0.01 chance to mutate the char"""

        str_len = len(self.current_string)
        possible_chars = string.printable

        i = 0
        while (i < str_len):
            mutate_chance = random.uniform(0, 1)

            if (mutate_chance <= mutation_prob):
                j = random.randint(0, 94)
                self.current_string = self.current_string[:i] + possible_chars[j] + self.current_string[(i + 1):]

            i += 1

    def true_fitness(self, pop_size):
        """(int) --> none
        returns fitness as number of characters correct instead of a percentage"""
        return self.fitness * pop_size

class population:
    """A class that holds a list of all individuals in the population. When first instantiated,
    starts with individuals with random character strings."""
    
    def __init__(self, pop_number):
        """initializes a population of char strings of specified pop number"""
        pop_range = range(pop_number)

        self.pop_size = pop_number
        #initializing these as lists of empty strings but we'll overwrite the objects later
        #this is just to ensure the correct length of the lists for indexing
        self.individuals = ["" for i in pop_range]
        self.breeding_pool = ["" for i in pop_range]

        #here's where we actually initialize the population
        i = 0 #keeps track of individual's number
        for item in self.individuals:
            item = individual("I think this is a reasonable medium sized string!!")
            self.individuals[i] = item
            self.individuals[i].update_fitness()
            i += 1
    
    def pick_from_population(self):
        """(none) --> none
        once cumulative probabilities for each individual, this function will actually choose from the population using
        those probabilities and put them in the breeding pool"""

        i = 0
        while (i < self.pop_size):
            prob = random.uniform(0, 1)

            #loop to go through all individuals cum. probabilities
            #to find the correct one according to the generated probability
            j = 0
            while (j < self.pop_size):
                if (prob <= self.individuals[j].cum_prob):
                    break
                j += 1

            #once we've found the correct individual according to gen. probability
            #puts it in breeding pool (COPYING it, not referencing it)
            self.breeding_pool[i] = copy.deepcopy(self.individuals[j])

            i += 1

    def get_probabilities_ts(self):
        """(none) --> none
        using tournament selection, fills the breeding pool
        note: also fills breeding pool, so do not need to use pick_from_population() after"""

        num_chosen = 0
        while (num_chosen < self.pop_size):
            
            #get two random numbers from 0 to 49 to represent the individuals
            #we choose for the tournament selection
            num_1 = random.randint(0, 49)

            #ensures second individual is not the same as the first
            same_num = True
            while (same_num):
                num_2 = random.randint(0, 49)
                if (num_2 != num_1):
                    same_num = False

            #now puts the more fit individual in the breeding pool
            fitness_1 = self.individuals[num_1].fitness
            fitness_2 = self.individuals[num_2].fitness

            if (fitness_1 > fitness_2):
                self.breeding_pool[num_chosen] = copy.deepcopy(self.individuals[num_1])
            else:
                self.breeding_pool[num_chosen] = copy.deepcopy(self.individuals[num_2])

            num_chosen += 1

    def get_probabilities_rs(self):
        """(none) --> none
        using ranked-based selection, gets cumulative probabilities for each individual"""

        self.individuals.sort(key=lambda x: x.fitness)

        #gets total probability sum for all ranks to normalize later
        rank_sum = 0
        i = 0
        while (i < self.pop_size):
            rank_sum += (i + 1)
            i += 1

        #they're already sorted, so the first one has rank 1
        #and so forth
        i = 1
        while (i < (self.pop_size + 1)):
            self.individuals[i - 1].cum_prob = i / rank_sum
            i += 1

        #now we just need to adjust to make the cumulative probability actually cumulative
        #the last loop just gives the probability for each one
        i = 1 #initialized at 1 because we don't actually have to alter the first probability
        while (i < self.pop_size):
            self.individuals[i].cum_prob += self.individuals[i - 1].cum_prob
            i += 1

    
    def get_probabilities_bs(self):
        """(none) --> none
        using Boltzmann selection, gets cumulative probabilities for each individual"""

        #find probability sum to normalize
        boltzmann_sum = 0
        i = 0
        while (i < self.pop_size):
            boltzmann_sum += math.exp(self.individuals[i].true_fitness(self.pop_size))
            i += 1

        #now find individual probabilities
        i = 0
        while (i < self.pop_size):
            self.individuals[i].cum_prob = (math.exp(self.individuals[i].true_fitness(self.pop_size))) / boltzmann_sum
            #print("Indv. fitness: " + str(self.individuals[i].fitness))
            #print("Indv. probability: " + str(self.individuals[i].cum_prob))
            i += 1
        
        #now adjust cum. probabilities
        i = 1
        while (i < self.pop_size):
            self.individuals[i].cum_prob += self.individuals[i - 1].cum_prob
            i += 1

    def update_all_fitnesses(self):
        """runs the update fitness method on each individual of the population,
        to be used after a breeding pool is used to make a new population"""
        i = 0
        while (i < self.pop_size):
            self.individuals[i].update_fitness()
            i += 1

    def recombination(self, crossover_prob, mutation_prob):
        """(float, float) --> none
        does crossover and mutation on all individuals of the breeding pool
        then, instead of copying them into the general population, we just change
        the value of the string held by each individual in the general population
        effectively copying the individuals in"""

        #first let's do crossover, we don't need to select random individuals from breeding pool
        #because they were already chosen randomly from the population
        #then, once we've copied them in, mutate them

        i = 0
        #pop_size - 1 because we're working in pairs
        while (i < (self.pop_size - 1)):
            individual_1 = self.breeding_pool[i]
            individual_2 = self.breeding_pool[i + 1]

            #does crossover if meets probability
            crossover_prob = random.uniform(0, 1)
            if (crossover_prob <= crossover_prob):
                crossover_point = random.randint(0, 49)

                new_str_1 = individual_1.current_string[:crossover_point] + individual_2.current_string[crossover_point:]
                new_str_2 = individual_2.current_string[:crossover_point] + individual_1.current_string[crossover_point:]

                self.individuals[i].change_string(new_str_1)
                self.individuals[i].mutate(mutation_prob)
                self.individuals[i + 1].change_string(new_str_2)
                self.individuals[i + 1].mutate(mutation_prob)

            #otherwise, just copies in the breeding pair
            else:
                self.individuals[i].change_string(individual_1.current_string)
                self.individuals[i].mutate(mutation_prob)
                self.individuals[i + 1].change_string(individual_2.current_string)
                self.individuals[i + 1].mutate(mutation_prob)

            i += 2 #moves iterator to next two individuals in breeding pool

    def get_most_fit(self):
        """(none) --> individual
        returns the most fit individual"""
        most_fit = self.individuals[0]

        i = 1
        while (i < self.pop_size):
            if (self.individuals[i].fitness > most_fit.fitness):
                most_fit = self.individuals[i]
            i += 1

        return most_fit

    def print_avg_fitness(self):

        i = 0
        fit_sum = 0
        while (i < self.pop_size):
            fit_sum += self.individuals[i].fitness
            i += 1

        avg_fitness = fit_sum / self.pop_size
        print("Average fitness: " + str(avg_fitness))

    def get_avg_fitness(self):

        i = 0
        fit_sum = 0
        while (i < self.pop_size):
            fit_sum += self.individuals[i].fitness
            i += 1

        return fit_sum / self.pop_size
