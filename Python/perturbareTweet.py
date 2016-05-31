#coding: utf-8
import os
from numpy import character
from pprint import pprint
import random
import string

#Leggo il file .txt contenente i tweet puliti
tweets = open("tweet_puliti.txt", "r")
#Apro il file .txt che conterrà i tweet perturbati
write_file = open("tweet_sporchi.txt", "w")
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
            #print("sc = ", selectedCharacter)
            u = random.random() #genero un numero casuale tra 0 (incluso) e 1 (escluso)
            if (u <= 0.1):
                randomCharacter = random.choice(dict_neighbors[selectedCharacter.lower()])
                #print("rc = ", randomCharacter)
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

#Dividere i testi in training (80%) e in testing (20%)

tweets_puliti = open("tweet_puliti.txt", "r")
tweets_sporchi = open("tweet_sporchi.txt", "r")

#Conto il numero di tweet presenti nel file .txt
num_lines = sum(1 for line in open('tweet_puliti.txt'))

#Calcolo l'80% di num_lines e calcolo il 20% di num_lines
num_lines_training = int(0.8 * num_lines)
num_lines_testing = (num_lines - num_lines_training)


#Divido in base al seguente criterio: 80% di num_lines va in training.txt e 20% rimanente di num_lines va in testing.txt

training_file_puliti = open("training_puliti.txt", "w")
testing_file_puliti = open("testing_puliti.txt", "w")
training_file_sporchi = open("training_sporchi.txt", "w")
testing_file_sporchi = open("testing_sporchi.txt", "w")

number_of_line = 1
for line in tweets_puliti.readlines():
    if (number_of_line <= num_lines_training): #se sto considerando un tweet nel primo 80% del totale, il tweet lo metto in training.txt
        training_file_puliti.write(line)
        training_file_sporchi.write(line)
    else: #il tweet lo metto in testing.txt
        testing_file_puliti.write(line)
        testing_file_sporchi.write(line)
    number_of_line = (number_of_line + 1)
