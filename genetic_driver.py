"""
AUTHOR: Patrick Callum O'Connell
Initial program written in November, 2020.

This is the driver for running the genetic algorithm with command line specifications.
The first argument specifies the population size, 
the 2nd specifies selection type (it can be "ts" meaning tournament selection, "bs" meaning Boltzmann selection, or "rs" meaning rank selection)
the 3rd specifies the probability (0 >= p >= 1) of crossover occurring when two individuals breed
the 4th specifies the probability of mutation occurring for any one gene during reproduction
the 5th indicates the maximum number of generations allowed
the 6th indicates how often the user is updated about the current population.

Once the Django GUI is done, this won't be used, but it will still be useful for debugging.

"""

import sys
from genetic_classes import individual, population

#initializes command line args as variables
population_size = int(sys.argv[1])
selection_type = str(sys.argv[2])
crossover_probability = float(sys.argv[3])
mutation_probability = float(sys.argv[4])
max_generations = int(sys.argv[5])
print_interval = int(sys.argv[6])

our_pop = population(population_size)
print("Beginning genetic algorithm...")
found_best = False

i = 0
while (i < max_generations):

    most_fit = our_pop.get_most_fit()
    if (most_fit.fitness == 1):
        found_best = True
        break

    #prints out generational updates every print interval
    if ((i % print_interval) == 0):
        print("Generation: " + str(i))
        print("Most fit individual: " + str(round(most_fit.fitness * 100, 2)) + "%" + " correct. String: " + most_fit.current_string)
    
    #selection based on type argument
    if (selection_type == "ts"):
        our_pop.get_probabilities_ts()
    else:
        if (selection_type == "rs"):
            our_pop.get_probabilities_rs()
        else: #if type is boltzmann
            our_pop.get_probabilities_bs()
        our_pop.pick_from_population()

    our_pop.recombination(crossover_probability, mutation_probability)
    our_pop.update_all_fitnesses()
    i += 1

print("")
print("Algorithm complete.")
if (found_best):
    print("Hit the target!")
else:
    print("Did not hit the target before generation " + str(max_generations))

print("Found max fitness individual at generation: " + str(i))
print("Target:          I think this is a reasonable medium sized string!!")
print("Best individual: " + most_fit.current_string)

num_correct = most_fit.fitness * population_size
formatted_score_frac = str(int(num_correct)) + "/" + str(population_size)
percent_correct = str(round(most_fit.fitness * 100, 2)) + "%"

print("Score = " + formatted_score_frac + " = " + percent_correct)
print("")
