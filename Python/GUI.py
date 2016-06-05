#coding utf-8

from Tkinter import *

#Importo lo script .py dove ci sono le funzioni che servono
import calcoloVettoreMatrici

class Application(Frame):
    """GUI (Graphical User Interface)"""

    #Initialize the GUI
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    #Procedura che carica i vari oggetti sulla GUI (e.g. bottoni, edit-text)
    def createWidgets(self):
        self.label_insertText = Label(self, text = "Inserisci il testo:")
        self.label_insertText.grid(row = 0, column = 0, columnspan = 2, sticky = W)

        self.entry_text = Entry(self)
        self.entry_text.grid(row = 1, column = 0, sticky = W)

        self.button_submit = Button(self, text = "Correggi", command = self.viterbiAlgorithm)
        self.button_submit.grid(row = 2, column = 0, sticky = W)
        
        self.button_deleteText = Button(self, text = "Cancella il Testo Inserito", command = self.deleteText)
        self.button_deleteText.grid(row = 1, column = 2, sticky = W)

        self.correct_text = Text(self, width = 23, height = 1)
        self.correct_text.grid(row = 3, column = 0, sticky = W)

        self.exit_button = Button(self, text = "Esci dall'Applicazione", command = self.exitApplication)
        self.exit_button.place(relx = 1, rely = 1, anchor = "se")

    #Procedura che permette di cancellare il contenuto della edit-text dove l'utente inserisce il testo
    def deleteText(self):
        self.entry_text.delete(0, END)

    #Procedura che permette di eseguire l'algoritmo di Viterbi sul testo inserito dall'utente
    def viterbiAlgorithm(self):
        sequenza = calcolatore.inferenza(modello, self.entry_text.get().lower())
        #Cancello cio' che c'e' scritto nella text edit quando ho premuto il bottone "Correggi"
        self.correct_text.delete(0.0, END)
        #Scrivo la sequenza di stati piu' probabile nella text edit
        self.correct_text.insert(0.0, sequenza)

    def exitApplication(self):
        sys.exit() #chiude il programma, quindi tutte le finestre aperte

#Chiamate alle procedure per calcolare il vettore pi, le matrici T e O e per creare il modello
calcolatore = calcoloVettoreMatrici.calcoloVettoreMatrici()
pi = calcolatore.calcolo_vettore_pi()
matrice_T = calcolatore.calcolo_matrice_transizioni()
matrice_O = calcolatore.calcolo_matrice_osservazioni()
modello = calcolatore.creazione_modello(matrice_T, matrice_O, pi)

#Settaggi della GUI (e.g. nome della finestra della GUI e la sua dimensione)
root = Tk()
root.title("GUI Misspelling")
root.geometry("350x200")

app = Application(root)
root.mainloop()
