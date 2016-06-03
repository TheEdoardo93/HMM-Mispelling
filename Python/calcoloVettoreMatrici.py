#coding: utf-8
#another test
#conflitti
from numpy import character
import numpy
from array import *
from pomegranate import *
import json
import ast
import editdistance

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
    #T = matrix_to_json(matrice_T)
    O = matrix_to_json(matrice_O)

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
    return model
    
def delete__by_values(lst, values):
    values_as_set = set(values)
    return [ x for x in lst if x not in values_as_set ]
    
    
def inferenza(model, sequence):
    
    logp, path = model.viterbi(sequence[0:len(sequence)])
    #print("VITERBI")
    
    x=""
    for i in range(1, len(path)):
        if (json.loads(ast.literal_eval(json.dumps(str(path[i][1]), sort_keys= False))).get('name') == 'Space'):
            x = x+ " "
        else:
            x = x+""+json.loads(ast.literal_eval(json.dumps(str(path[i][1]), sort_keys= False))).get('name')
    
    #print x
    return x
   
def test(model):
    testing_sporchi = open("./PerturbazioneTweet/testing_sporchi.txt", "r")
    testing_puliti = open("./PerturbazioneTweet/testing_puliti.txt", "r")
    
     
    numchars = 0.0   
    for line in testing_puliti.readlines():
        print len(line)
        for i in range(0, len(line)):
            if(line[i].isalpha()):
                numchars = numchars + 1.0
    print numchars
    
    testing_puliti.close()
    testing_puliti = open("./PerturbazioneTweet/testing_puliti.txt", "r")    
    lines_pulite=testing_puliti.readlines()
    
    unlist = ['\x82', '\xac','\x87', '\xbd', '\xbe', '\xb6', '\xa4', '\xc5', '\x9f', '\xc4', '\xb1', '\xc3', '\xbc', '\xa3', '$', '\x98', '%', '\xa6', '\x9c', '\x9d', '|', ']', '[', '_', '\xc2', '\xa0', '\x99', ';', '+', '=', '*', '\xe2', '\x80', '\x94','?', '\n', ':', '\'', '/', '!', ',', '.', '-', '"', '(', ')', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    numLine=0   
    editDistance = 0.0
    for line in testing_sporchi.readlines(): 
        x=''.join(delete__by_values(list(line.lower()), unlist))
        y = ''.join(delete__by_values(lines_pulite[numLine].lower(), unlist))
        
        newL=len(x)-1      
        j = 0  
        for i in range(0, len(x)-1):
            if(newL > i):
                if(x[j].isspace() and x[j + 1].isspace()):                    
                    x = x[0:j]+x[j+2:len(x)]
                    y = y[0:j]+y[j+2:len(y)]
                    newL = newL -1
                else:
                    j = j + 1
                   
        x = inferenza(model, list(x))        
                                        
        editDistance += editdistance.eval(y, x)
        numLine += 1
    
    testing_sporchi.close()
    testing_puliti.close()
    print editDistance
    return (editDistance/numchars)
   
    
    
# Pipeline di trattamento dati e inferenza!

vettore_Pi = calcolo_vettore_pi()
matrice_T = calcolo_matrice_transizioni()
matrice_O = calcolo_matrice_osservazioni()
model = creazione_modello(matrice_T, matrice_O, vettore_Pi)
#inferenza(model, list("zs yoi see thwre ix a sea begween you abd mr"))
#inferenza(model, list("qe zll ljvr ih tue ywllow xubmarine"))
errore = test(model)
print errore
