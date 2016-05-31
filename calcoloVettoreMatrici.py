#coding: utf-8
# Belingheri Omar 761702
# Casiraghi Edoardo 762987
# Khayam Adam 761763

"""Progetto di Modelli Probabilistici per le Decisioni - Mispelling (4)"""

#-----------------------------------------------------------------------------------------------------------------------#

# CALCOLO DEL VETTORE PI (probabilità iniziali delle lettere)


from numpy import character
import numpy
from array import *
from pomegranate import *

def calcolo_vettore_pi():
    # inizializza vettore probabilit iniziali
    vettorePi = {"a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 0, "k": 0,
                 "l": 0, "m": 0, "n": 0, "o": 0, "p": 0, "q": 0, "r": 0, "s": 0, "t": 0, "u": 0, "v": 0,
                 "w": 0, "x": 0, "y": 0, "z": 0}
    tweets = open("./PerturbazioneTweet/training_puliti.txt", "r")  # apro il file dei tweet
    number = 0
    for line in tweets.readlines():  # itero su ogni riga del file
        number += 1
        x = 0  # carattere x-esimo
        while ((x < len(line)) and (line[x].isalpha() == False)):
            x += 1
        if ((x != len(line)) and (line[x].lower() in vettorePi)):  # il carattere dove mi sono fermato è nel dizionario?
            vettorePi[line[x].lower()] += 1  # aumenta il contatore della sua lettera
    # normalizzo
    for y in vettorePi:
        vettorePi[y] = (float(vettorePi[y]) / float(number))

    tweets.close()

    return (vettorePi)

#-----------------------------------------------------------------------------------------------------------------------#

# CALCOLO DELLA MATRICE DELLE TRANSIZIONI T (transizioni da uno stato all'altro)

def calcolo_matrice_transizioni():
    # Apro il file dei tweet puliti
    tweets = open("./PerturbazioneTweet/training_puliti.txt", "r")

    number = 0
    # Definisco una matrice di supporto 27x27
    matrice_T = numpy.zeros((27, 27))
    # Conto il numero di volte in cui da una lettera vado in un'altra lettera
    for line in tweets.readlines():  # per ogni tweets
        for i in range(1, len(line)):  # per ogni carattere del tweet considerato
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

    for i in range(0, matrice_T.shape[0]-1): #normalizzo per riga
        matrice_T[i, 0:matrice_T.shape[1]] = matrice_T[i, 0:matrice_T.shape[1]] / matrice_T[i, 0:matrice_T.shape[1]].sum()

    tweets.close()

    return (matrice_T)
#-----------------------------------------------------------------------------------------------------------------------#

# CALCOLO DELLA MATRICE DELLE OSSERVAZIONI O (probabilità di osservare qualcosa dato che sono in uno stato)

def calcolo_matrice_osservazioni():
    tweets = open("./PerturbazioneTweet/training_sporchi.txt", "r")
    # Definisco una matrice di supporto 27x27
    matrice_O = numpy.zeros((27, 27))
    # Conto il numero di volte in cui da una lettera vado in un'altra lettera
    for line in tweets.readlines():  # per ogni tweets
        for i in range(1, len(line)):  # per ogni carattere del tweet considerato
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

    for i in range(0, matrice_O.shape[0]-1): #normalizzo per riga
        matrice_O[i, 0:matrice_O.shape[1]] = matrice_O[i, 0:matrice_O.shape[1]] / matrice_O[i, 0:matrice_O.shape[1]].sum()

    tweets.close()

    return (matrice_O)

def creazione_modello(matrice_T, matrice_O, vettore_Pi):

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
    model.add_transition(s3, s2, matrice_T[2,0])
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
    print("transitions = ", transitions)

#-----------------------------------------------------------------------------------------------------------------------#

# Chiamate delle funzioni che calcolano il vettore pi, la matrice T e la matrice O
vettore_Pi = calcolo_vettore_pi()
matrice_T = calcolo_matrice_transizioni()
matrice_O = calcolo_matrice_osservazioni()
creazione_modello(matrice_T, matrice_O, vettore_Pi)
