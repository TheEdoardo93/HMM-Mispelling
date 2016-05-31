#coding: utf-8
import os
from numpy import character
from pprint import pprint
import random
import string

def perturbazione_tweets():

    #Leggo il file .txt contenente i tweet puliti
    tweets = open("../FileTestuali/tweet_puliti.txt", "r")
    #Apro il file .txt che conterrà i tweet perturbati
    write_file = open("../FileTestuali/tweet_sporchi.txt", "w")
    dict_neighbors = {"q": "qwsxz", "w": "qasde", "e": "wsdfr", "r": "edfgt", "t": "rfghy", "y": "tghju", "u": "yhjki", "i": "ujklo",
                  "o": "iklp", "p": "ol", "a": "qwsxz", "s": "qazxcdew", "d": "wsxcvfre", "f": "edcvbgtr", "g": "rfvbnhyt",
                  "h": "tgbnmjuy", "j": "yhnmkiu", "k": "ujmloi", "l": "poik", "z": "asx", "x": "zasdc", "c": "xsdfv",
                  "v": "cdfgb", "b": "vfghn", "n": "bghjm", "m": "nhjk"}

    #Per ogni tweet (cioè 'line'), perturbo il tweet (considerando il 10% di errori)
    for line in tweets.readlines():
        posizione = 0
        while (posizione < len(line)): #vado fino in fondo alla linea
            if (line[posizione].isalpha() == True): #è una lettera, quindi lancio moneta, etc
                selectedCharacter = line[posizione] #salvo la lettera che sto considerando (siccome non voglio sostituire la lettera con la stessa)
                u = random.random() #genero un numero casuale tra 0 (incluso) e 1 (escluso)
                if (u <= 0.1):
                    randomCharacter = random.choice(dict_neighbors[selectedCharacter.lower()])
                    while(randomCharacter == selectedCharacter):
                        randomCharacter = random.choice(dict_neighbors[selectedCharacter.lower()])
                    tempInitial = line[0:posizione] #substring da 0 fino a posizione (o posizione-1)
                    tempFinal = line[posizione+1:] #substring da posizione (o posizione+1) fino alla fine
                    line = tempInitial+randomCharacter+tempFinal #rimpiazzo "selectedCharacter" con "randomCharacter"
                posizione += 1 #considero il simbolo successivo
            else:
                posizione += 1 #considero il simbolo successivo
            #Salvo su file .txt il tweet perturbato
            if (posizione == len(line)): #se ho considerato tutto il tweet, lo salvo
                write_file.write(line)

    tweets.close() #chiusura del file .txt contenente i tweet puliti
    write_file.close() #chiusura del file .txt contenente i tweet perturbati

#----------------------------------------------------------------------------------------------------------#

def divisione_training_tweets_puliti():
    #80% dei tweets puliti (non perturbati) provenienti da tweet_puliti.txt

    tweets_puliti = open("../FileTestuali/tweet_puliti.txt", "r")
    training_file_puliti = open("../FileTestuali/training_puliti.txt", "w")

    num_lines = sum(1 for line in tweets_puliti)
    num_lines_training = int(0.8 * num_lines)

    number_of_line = 1
    for line in tweets_puliti.readlines():
        if (number_of_line <= num_lines_training):
            training_file_puliti.write(line)
        number_of_line += 1

    tweets_puliti.close()
    training_file_puliti.close()

    return (num_lines_training)

def divisione_testing_tweets_puliti():
    #20% dei tweets puliti (non perturbati) provenienti da tweet_puliti.txt

    tweets_puliti = open("../FileTestuali/tweets_puliti.txt", "r")
    testing_file_puliti = open("../FileTestuali/testing_puliti.txt", "w")

    num_lines = sum(1 for line in tweets_puliti)
    num_lines_training = int(0.8 * num_lines)

    number_of_line = 1
    for line in tweets_puliti.readlines():
        if ((number_of_line > num_lines_training) and (number_of_line <= num_lines)):
            testing_file_puliti.write(line)
        number_of_line += 1

    tweets_puliti.close()
    testing_file_puliti.close()

#Chiamate alle procedure

perturbazione_tweets()
divisione_training_tweets_puliti()
divisione_testing_tweets_puliti()
