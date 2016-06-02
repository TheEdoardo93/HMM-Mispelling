#coding: utf-8
#another test
#conflitti
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
    training_sporchi = open("./PerturbazioneTweet/training_sporchi.txt", "r")
    training_puliti = open("./PerturbazioneTweet/training_puliti.txt", "r")
    matrice_O = numpy.zeros((27, 27))
    lines_pulite=training_puliti.readlines()
    numLine=0
    
    for line in training_sporchi.readlines() :
        for i in range(0, len(line)):
            char_dirty = line[i].lower()
            #print char_dirty
            char_clean = lines_pulite[numLine][i].lower() #rappresenta lo stato in cui sono
            #print char_clean
            if (char_dirty.isalpha() == True):
                matrice_O[(ord(char_clean) - ord('a'), ord(char_dirty) - ord('a'))] += 1
            else:
                if (char_dirty.isspace() == True): #questo if è inutile
                    matrice_O[26, 26] +=  1
        numLine += 1

    for i in range(0, matrice_O.shape[0]):
        matrice_O[i, 0:matrice_O.shape[1]] = matrice_O[i, 0:matrice_O.shape[1]] / matrice_O[i, 0:matrice_O.shape[1]].sum()

    training_sporchi.close()
    return (matrice_O)


def matrix_to_json(matrice):
    lista = list()
    for i in range(97, 124):
        for j in range(97, 124):
            if(j == 97):
                data=[{}]
            if (j != 123):
                data[0][chr(j)] = matrice[i-97, j-97]
            else:
                data[0][chr(32)] = matrice[i-97, j-97]
        lista.append(json.dumps(data, sort_keys = True))
    
    return (lista)


def creazione_modello(matrice_T, matrice_O, vettore_Pi):
    T = matrix_to_json(matrice_T)
    O = matrix_to_json(matrice_O)
    print T

    dists = list()
    for i in range(0, 27):
        dists.append(DiscreteDistribution(ast.literal_eval(O[i][1:len(O[i])-1])))
          
    states = list()
    for j in range(0, 27):
        if(j != 26):
            states.append(State(dists[j], name = ""+chr(j+97) ))
        else:
            states.append(State(dists[j], name = "Space" ))

    model = HiddenMarkovModel('mispelling')
    model.add_states(states)
    
    #pi = json.loads(pi.to_json())
    #pi = pi['parameters']  
    #print pi[0]['z']  
    
        
    for i in range(0, 27):
        for j in range(0, 27):
            model.add_transition(states[i], states[j], matrice_T[i, j])
    
    for i in range(0, 26):
        model.add_transition(model.start, states[i], vettore_Pi[chr(i+97)])
     
    model.bake()
    #model.draw()
    

    logp, path = model.viterbi(list("zs yoi see thrre ix a sea begween you abd mr"))
    print("VITERBI")
    
    x=""    
    for i in range(1, len(path)):
        if (json.loads(ast.literal_eval(json.dumps(str(path[i][1]), sort_keys= False))).get('name') == 'Space'):
            x = x+ " "
        else:
            x = x+""+json.loads(ast.literal_eval(json.dumps(str(path[i][1]), sort_keys= False))).get('name')
    
    print x
    
# Chiamate delle funzioni che calcolano il vettore pi, la matrice T e la matrice O

vettore_Pi = calcolo_vettore_pi()
matrice_T = calcolo_matrice_transizioni()
matrice_O = calcolo_matrice_osservazioni()
creazione_modello(matrice_T, matrice_O, vettore_Pi)
