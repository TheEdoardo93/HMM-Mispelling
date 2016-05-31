#coding utf-8

from tkinter import *

class Application(Frame):
    """GUI (Graphical User Interface)"""

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.label_insertText = Label(self, text = "Inserisci il testo:")
        self.label_insertText.grid(row = 0, column = 0, columnspan = 2, sticky = W)

        self.entry_text = Entry(self)
        self.entry_text.grid(row = 0, column = 3, sticky = W)

        self.button_submit = Button(self, text = "Correggi")
        self.button_submit["command"] = self.viterbi
        self.button_submit.grid(row = 1, column = 1, sticky = W)

        self.correct_text = Text(self, width = 20, height = 10, wrap = WORD)
        self.correct_text.grid(row = 3, column = 0, columnspan = 2, sticky = W)

        self.exit_button = Button(self, text = "Esci dall'Applicazione")
        self.exit_button["command"] = self.exitApplication
        self.exit_button.grid(row = 4, column = 0, sticky = W)

        self.bottone_prova = Button(self, text = "prova")
        self.bottone_prova["command"] = self.prova
        self.bottone_prova.grid(row = 5, column = 0, sticky = W)

    def prova(self):
        #exec(open("./prova.py").read()) #qua devo chiamare viterbi

    def viterbi(self):
        text = self.entry_text.get()
        message = "sequenza di stati piu' probabile"
        #message = dovra' esserci la stringa che coincide con la sequenza di stati piu' probabile

        #Cancello cio' che c'e' scritto nella text edit quando ho premuto il bottone "Correggi"
        self.correct_text.delete(0.0, END)
        #Scrivo la sequenza di stati piu' probabile nella text edit
        self.correct_text.insert(0.0, message)

    def exitApplication(self):
        sys.exit() #chiude il programma, quindi tutte le finestre aperte

root = Tk()
root.title("GUI Mispelling")
root.geometry("500x300")

app = Application(root)
root.mainloop()
