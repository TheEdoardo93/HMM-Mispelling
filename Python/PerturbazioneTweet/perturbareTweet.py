#coding: utf-8
#just another test
import os
from numpy import character
from pprint import pprint
import random
import string

def perturbazione_tweets():
    tweets = open("./tweet_puliti.txt", "r")
    write_file = open("./tweet_sporchi.txt", "w")
    dict_neighbors = {"q": "wsa", "w": "qasde", "e": "wsdfr", "r": "edfgt", "t": "rfghy", "y": "tghju", "u": "yhjki", "i": "ujklo", "o": "iklp",
                      "p": "ol", "a": "qwsxz", "s": "qazxcdew", "d": "wsxcvfre", "f": "edcvbgtr", "g": "rfvbnhyt", "h": "tgbnmjuy", "j": "yhnmkiu",
                      "k": "ujmloi", "l": "poik", "z": "asx", "x": "zasdc", "c": "xsdfv", "v": "cdfgb", "b": "vfghn", "n": "bghjm", "m": "nhjk"}

    for line in tweets.readlines():
        posizione = 0
        while (posizione < len(line)):
            if (line[posizione].isalpha() == True):
                selectedCharacter = line[posizione]
                u = random.random()
                if (u <= 0.1):
                    randomCharacter = random.choice(dict_neighbors[selectedCharacter.lower()])
                    while(randomCharacter == selectedCharacter):
                        randomCharacter = random.choice(dict_neighbors[selectedCharacter.lower()])
                    tempInitial = line[0:posizione]
                    tempFinal = line[posizione+1:]
                    line = tempInitial+randomCharacter+tempFinal
                posizione += 1
            else:
                posizione += 1

            if (posizione == len(line)):
                write_file.write(line)

    tweets.close()
    write_file.close()

def dividere_tweets():
    tweets_puliti = open("./tweet_puliti.txt", "r")
    tweets_sporchi = open("./tweet_sporchi.txt", "r")

    num_lines = sum(1 for line in open('./tweet_puliti.txt'))
    num_lines_training = int(0.8 * num_lines)

    training_file_puliti = open("./training_puliti.txt", "w")
    testing_file_puliti = open("./testing_puliti.txt", "w")

    number_of_line = 1
    for line in tweets_puliti.readlines():
        if (number_of_line <= num_lines_training):
            training_file_puliti.write(line)
        else:
            testing_file_puliti.write(line)
        number_of_line = (number_of_line + 1)

    testing_file_sporchi = open("./testing_sporchi.txt", "w")
    training_file_sporchi = open("./training_sporchi.txt", "w")

    number_of_line = 1
    for line in tweets_sporchi.readlines():
        if (number_of_line <= num_lines_training):
            training_file_sporchi.write(line)
        else:
            testing_file_sporchi.write(line)
        number_of_line = (number_of_line + 1)

    training_file_puliti.close()
    training_file_sporchi.close()
    testing_file_puliti.close()
    testing_file_sporchi.close()

#Chiamate alle procedure

perturbazione_tweets()
dividere_tweets()
