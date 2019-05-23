#Alex Greenman
#873392313
#given a group of n people, this python script tells you what the probability
#that at least two of those people share the same birthday. This is accomplished
#by repeatedly randomly assigning birthdays to a group of people and
#checking whether or not one of those birthdays is shared.

import random
import sys
from collections import Counter

def single_trial(people, days):
    '''This function takes two integer parameters. It randomly assigns each
    person a birthday, returns true if at least two people share the same
    birthday, false if every person was assigned a different day'''
    empty_list = []
    #assign each person a birthday, append those birthdays to empty_list
    i = 0
    while i < people:
        persons = random.randint(1, int(days)+1)
        empty_list.append(persons)
        i+=1
    #remove duplicate from empty_list by creating a set
    empty_set=set(empty_list)
    #if length of set is equal to list, this implies no duplicate birthdays
    if len(empty_set) == len(empty_list):
        return False
    #if length of set isn't equal to list, this implies duplicate birthdays
    else:
        return True

def probability(people, days, trials):
    ''' This function approximates the probability that at least two people
    share the same birthday (called a "success") by performing requested
    number of trials and returning the ratio of successes to total trials'''
    #call single trial and run it the requested number of times
    result = [single_trial(people, days) for k in range(1,int(trials)+1)]
    #count instances in which a duplicate birthday occured in trials
    true_count=result.count(True)
    #divide count duplicate instances by total number of trials
    ratio_of_successes=true_count/len(result)
    return ratio_of_successes


def main():
    '''This function parses command line arguments. The command line arguments are
    processed, the desired trials or days are updated, and the number of people
    and the accompanying probability that at least two of those people
    share a birthday are printed in CSV format'''
    #set default parameters
    people = 1
    days = 365
    trials = 100
    #process the arguments
    argi=1
    while argi < len(sys.argv):
        #extract an argument
        arg=sys.argv[argi]
        #if argument does not start with '-', then break out of while loop
        if arg[0] != '-':
            break
        if arg=='-d':
            #increment argi by one and update days parameter based on user input
            days=int(sys.argv[argi+1])
            argi+=1
        elif arg=='-t':
            #increment argi by one and update trials parameter based on user input
            trials=int(sys.argv[argi+1])
            argi+=1
        else:
            #if flag is unrecognized, make user aware, print to standard error
            print(f'Unrecognized Flag \'{arg}\'', file=sys.stderr)
            argi+=1
        argi+=1

    #call probability and run as many times (based on days) as the user requests
    while people < int(days)+1:
        prob=probability(people, days, trials)
        print(f'{people},{prob}')
        people+=1
#if imported by the user, do nothing
#if executed by the user, run the main function
if __name__ == "__main__":
    main()
