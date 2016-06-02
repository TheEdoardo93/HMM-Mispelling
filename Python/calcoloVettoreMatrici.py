#coding: utf-8
#this is a test
from numpy import character
import numpy
from array import *
from pomegranate import *
import json
import ast

def calcolo_vettore_pi():
    vettorePi = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 0, "k": 0,
                 "l": 0, "m": 0, "n": 0, "o": 0, "p": 0, "q": 0, "r": 0, "s": 0, "t": 0, "u": 0, "v": 0,
                 "w": 0, "x": 0, "y": 0, "z": 0}
    tweets = open("./PerturbazioneTweet/training_puliti.txt", "r")
    number = 0
    for line in tweets.readlines():
        number += 1
        x = 0
        while ((x < len(line)) and (line[x].isalpha() == False)):
            x += 1
        if ((x != len(line)) and (line[x].lower() in vettorePi)):
            vettorePi[line[x].lower()] += 1

    for y in vettorePi:
        vettorePi[y] = (float(vettorePi[y]) / float(number))

    tweets.close()

    return (vettorePi)

def calcolo_matrice_transizioni():
    tweets = open("./PerturbazioneTweet/training_puliti.txt", "r")

    number = 0
    matrice_T = numpy.zeros((27, 27))

    for line in tweets.readlines():
        for i in range(1, len(line)):
            previous_character = line[i - 1].lower()
            character = line[i].lower()
            if ((character.isalpha() == True) and (previous_character.isalpha() == True)):
                matrice_T[(ord(previous_character) - ord('a'), ord(character) - ord('a'))] += 1
            else:
                if ((previous_character.isalpha() == True) and (character.isspace() == True)):
                    matrice_T[(ord(previous_character) - ord('a'), 26)] +=  1
                else:
                    if ((previous_character.isspace() == True) and (character.isalpha() == True)):
                        matrice_T[(26, ord(character) - ord('a'))] += 1

    for i in range(0, matrice_T.shape[0]):
        matrice_T[i, 0:matrice_T.shape[1]] = matrice_T[i, 0:matrice_T.shape[1]] / matrice_T[i, 0:matrice_T.shape[1]].sum()

    tweets.close()

    return (matrice_T)

def calcolo_matrice_osservazioni():
    tweets = open("./PerturbazioneTweet/training_sporchi.txt", "r")
    matrice_O = numpy.zeros((27, 27))

    for line in tweets.readlines():
        for i in range(1, len(line)):
            previous_character = line[i - 1].lower()
            character = line[i].lower()
            if ((character.isalpha() == True) and (previous_character.isalpha() == True)):
                matrice_O[(ord(previous_character) - ord('a'), ord(character) - ord('a'))] += 1
            else:
                if ((previous_character.isalpha() == True) and (character.isspace() == True)):
                    matrice_O[(ord(previous_character) - ord('a'), 26)] +=  1
                else:
                    if ((previous_character.isspace() == True) and (character.isalpha() == True)):
                        matrice_O[(26, ord(character) - ord('a'))] += 1

    for i in range(0, matrice_O.shape[0]):
        matrice_O[i, 0:matrice_O.shape[1]] = matrice_O[i, 0:matrice_O.shape[1]] / matrice_O[i, 0:matrice_O.shape[1]].sum()

    tweets.close()

    return (matrice_O)

"""def creazione_modello(matrice_T, matrice_O, vettore_Pi):

    d1 = DiscreteDistribution({
        'A':matrice_O[0,0], 'B':matrice_O[0,1], 'C':matrice_O[0,2], 'D':matrice_O[0,3], 'E':matrice_O[0,4],
        'F':matrice_O[0,5], 'G':matrice_O[0,6], 'H':matrice_O[0,7], 'I':matrice_O[0,8], 'J':matrice_O[0,9],
        'K':matrice_O[0,10], 'L':matrice_O[0,11], 'M':matrice_O[0,12], 'N':matrice_O[0,13], 'O':matrice_O[0,14],
        'P':matrice_O[0,15], 'Q':matrice_O[0,16], 'R':matrice_O[0,17], 'S':matrice_O[0,18], 'T':matrice_O[0,19],
        'U':matrice_O[0,20], 'V':matrice_O[0,21], 'W':matrice_O[0,22], "X":matrice_O[0,23], 'Y':matrice_O[0,24],
        'Z':matrice_O[0,25], 'Space':matrice_O[0,26]})

    d2 = DiscreteDistribution({
        'A':matrice_O[1,0], 'B':matrice_O[1,1], 'C':matrice_O[1,2], 'D':matrice_O[1,3], 'E':matrice_O[1,4],
        'F':matrice_O[1,5], 'G':matrice_O[1,6], 'H':matrice_O[1,7], 'I':matrice_O[1,8], 'J':matrice_O[1,9],
        'K':matrice_O[1,10], 'L':matrice_O[1,11], 'M':matrice_O[1,12], 'N':matrice_O[1,13], 'O':matrice_O[1,14],
        'P':matrice_O[1,15], 'Q':matrice_O[1,16], 'R':matrice_O[1,17], 'S':matrice_O[1,18], 'T':matrice_O[1,19],
        'U':matrice_O[1,20], 'V':matrice_O[1,21], 'W':matrice_O[1,22], "X":matrice_O[1,23], 'Y':matrice_O[1,24],
        'Z':matrice_O[1,25], 'Space':matrice_O[1,26]})

    d3 = DiscreteDistribution({
        'A':matrice_O[2,0], 'B':matrice_O[2,1], 'C':matrice_O[2,2], 'D':matrice_O[2,3], 'E':matrice_O[2,4],
        'F':matrice_O[2,5], 'G':matrice_O[2,6], 'H':matrice_O[2,7], 'I':matrice_O[2,8], 'J':matrice_O[2,9],
        'K':matrice_O[2,10], 'L':matrice_O[2,11], 'M':matrice_O[2,12], 'N':matrice_O[2,13], 'O':matrice_O[2,14],
        'P':matrice_O[2,15], 'Q':matrice_O[2,16], 'R':matrice_O[2,17], 'S':matrice_O[2,18], 'T':matrice_O[2,19],
        'U':matrice_O[2,20], 'V':matrice_O[2,21], 'W':matrice_O[2,22], "X":matrice_O[2,23], 'Y':matrice_O[2,24],
        'Z':matrice_O[2,25], 'Space':matrice_O[2,26]})

    #dichiaro gli stati
    s1 = State(d1, name = "Stato Lettera A")
    s2 = State(d2, name = "Stato Lettera B")
    s3 = State(d3, name = "Stato Lettera C")

    #aggiungo il modello e gli stati al modello
    model = HiddenMarkovModel('HMM Mispelling')
    model.add_states([s1, s2, s3])

    #aggiungo transizioni tra stati
    model.add_transition(model.start, s1, vettore_Pi.get('a'))
    model.add_transition(model.start, s2, vettore_Pi.get('b'))
    model.add_transition(model.start, s3, vettore_Pi.get('c'))

    model.add_transition(s1, s1, matrice_T[0,0])
    model.add_transition(s1, s2, matrice_T[0,1])
    model.add_transition(s1, s3, matrice_T[0,2])
    model.add_transition(s2, s1, matrice_T[1,0])
    model.add_transition(s2, s2, matrice_T[1,1])
    model.add_transition(s2, s3, matrice_T[1,2])
    model.add_transition(s3, s1, matrice_T[2,0])
    model.add_transition(s3, s2, matrice_T[2,1])
    model.add_transition(s3, s3, matrice_T[2,2])

    model.bake()

    #predict - viterbi
    matrix = model.forward(list('AAA'))
    print("PREDICT")
    print("matrix = ", matrix)

    #viterbi algorithm
    logp, path = model.viterbi(list('AAA'))
    print("VITERBI")
    print("logp = ", logp)
    print("path = ", path)

    #forward backward algorithm
    emissions, transitions = model.forward_backward(list('CAB'))
    print("FORWARD BACKWARD")
    print("emissions = ", emissions)
    print("transitions = ", transitions)"""

def matrix_to_json(matrice):
    lista = list()
    for i in range(97, 124): #a,z in ascii
        for j in range(97, 124):
            if(j == 97):
                data=[{}]
            if (j != 123):
                data[0][chr(j)] = matrice[i-97, j-97]
            else:
                data[0]['space'] = matrice[i-97, j-97]
        lista.append(json.dumps(data, sort_keys = True))

    return (lista)

def creazione_modello(matrice_T, matrice_O, vettore_Pi):
    T = matrix_to_json(matrice_T)
    O = matrix_to_json(matrice_O)

    d = list()
    for i in range(0, 27):
        d.append(DiscreteDistribution(ast.literal_eval(O[i][1:len(O[i])-1])))

    s = list()
    for j in range(0, 27):
        if(j != 26):
            s.append(State(d[j], name = "Stato Lettera " + chr(j+97) ))
        else:
            s.append(State(d[j], name = "Stato Lettera Space" ))

    model = HiddenMarkovModel('Prova')
    model.add_states(s)
    for i in range(0, 26):
        model.add_transition(model.start, s[i], vettore_Pi.get(chr(i+97)))

    for i in range(0, 27):
        for j in range(0, 27):
            model.add_transition(s[i], s[j], matrice_T[i, j])

    print s[0]

# Chiamate delle funzioni che calcolano il vettore pi, la matrice T e la matrice O

vettore_Pi = calcolo_vettore_pi()
matrice_T = calcolo_matrice_transizioni()
matrice_O = calcolo_matrice_osservazioni()
creazione_modello(matrice_T, matrice_O, vettore_Pi)
