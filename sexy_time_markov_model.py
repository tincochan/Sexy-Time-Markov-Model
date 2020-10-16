#!/bin/python

# python sexy_time_markov_model.py "initial_probs.csv" "transition_probs.csv" "arousal_rates.csv" "time_parameters.csv"

from scipy import stats
import csv
import numpy
import sys


# Import the probabilities for starting in different sexual positions.
def get_initial_probs(filename):
    positions = []
    initial_probs = []
    
    reader = csv.DictReader(open(filename))
    
    for row in reader:
        positions.append(row["Position"])
        initial_probs.append(float(row["p"]))
    
    return (positions, stats.rv_discrete(name = "initial_probs", values = (range(0, len(positions)), initial_probs)))


# Import the probabilities for transitioning between different sexual positions.
def get_transition_probs(filename):
    transition_probs = {}
    
    reader = csv.DictReader(open(filename))
    
    for row in reader:
        current_position = row["Position"]
        probs = []
        for i in range(1, len(reader.fieldnames)):
            next_position = reader.fieldnames[i]
            probs.append(float(row[next_position]))
        transition_probs[current_position] = stats.rv_discrete(name = "transition_probs", values = (range(0, len(reader.fieldnames) - 1), probs))
    
    return transition_probs


# Import the orgasm rate for each partner and sexual position.
def get_arousal_rates(filename):
    reader = csv.DictReader(open(filename))
    [position, partnerOne, partnerTwo] = reader.fieldnames
      
    arousal_rates = {partnerOne: {}, partnerTwo: {}}
    
    for row in reader:
        position = row["Position"]
        arousal_rates[partnerOne][position] = float(row[partnerOne])
        arousal_rates[partnerTwo][position] = float(row[partnerTwo])
    
    return arousal_rates


# Import the parameters used to determine the amount of time spent in each sexual position.
def get_time_parameters(filename):
    time_parameters = {}
    
    reader = csv.DictReader(open(filename))
    
    for row in reader:
        position = row["Position"]
        time_parameters[position] = {}
        time_parameters[position]["shape"] = float(row["Shape"])
        time_parameters[position]["scale"] = float(row["Scale"])
    
    return time_parameters

def main():
    (positions, initial_probs) = get_initial_probs(sys.argv[1])
    transition_probs = get_transition_probs(sys.argv[2])
    arousal_rates = get_arousal_rates(sys.argv[3])
    time_parameters = get_time_parameters(sys.argv[4])
    
    while True:
        simulate = input("Simulate sex (y/n)? ")
        # Simulate sex.
        if "y" in simulate.lower():
            total_time = 0.0
            position_count = 0
            partner_one_orgasms = 0.0
            partner_two_orgasms = 0.0
            pos = positions[initial_probs.rvs()]
            # while partner_one_orgasms < 1.0 or partner_two_orgasms < 1.0: # You know... if you're into being fair.
            while partner_two_orgasms < 1.0:
                shape = time_parameters[pos]["shape"]
                scale = time_parameters[pos]["scale"]
                time = numpy.random.gamma(shape, scale)
                total_time += time
                partner_one_orgasms += time * arousal_rates["partner_one"][pos]
                partner_two_orgasms += time * arousal_rates["partner_two"][pos]
                print("Position: {0}\tTime: {1:.2f} (s)/{2:.2f} (min)\tpartner_one Orgasms: {3:.2f}\tpartner_two Orgasms: {4:.2f}"
                      .format(pos, time, time / 60.0, partner_one_orgasms, partner_two_orgasms))
                pos = positions[transition_probs[pos].rvs()]
                position_count += 1
            
            print("Total Time: {0:.2f} (s)/{1:.2f} (min)\tPosition Count: {2}\tpartner_one Orgasms: {3}\tpartner_two Orgasms: {4}"
                  .format(total_time, total_time / 60.0, position_count, int(partner_one_orgasms), int(partner_two_orgasms)))
        else:
            break


if __name__ == "__main__":
    main()
